from neo4j import GraphDatabase
from config import uri, username, password
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from neo4j.exceptions import TransientError, ServiceUnavailable

driver = GraphDatabase.driver(uri, auth=(username, password))

def get_driver():
    return driver

def close_driver():
    driver.close()

def create_relationships(tx, batch):
    query = (
        "UNWIND $batch as row "
        "MERGE (c:Category {name: row.category}) "
        "MERGE (s:Category {name: row.subcategory}) "
        "MERGE (c)-[:HAS_SUBCATEGORY]->(s)"
    )
    tx.run(query, batch=batch)

def create_unique_constraint(tx):
    query = (
        "CREATE CONSTRAINT unique_category_name IF NOT EXISTS "
        "FOR (c:Category) REQUIRE c.name IS UNIQUE"
    )
    tx.run(query)

def create_index(tx):
    query = (
        "CREATE INDEX IF NOT EXISTS FOR (c:Category) ON (c.name)"
    )
    tx.run(query)

def process_batch(batch):
    with driver.session() as session:
        session.write_transaction(create_relationships, batch)

def delete_nodes_batch(tx, batch_size):
    query = (
        "MATCH (n:Category) "
        "WITH n LIMIT $batch_size "
        "DETACH DELETE n "
        "RETURN count(n) as deleted_count"
    )
    result = tx.run(query, batch_size=batch_size)
    return result.single()["deleted_count"]

def delete_batch_with_retries(driver, batch_size, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            with driver.session() as session:
                return session.write_transaction(delete_nodes_batch, batch_size)
        except (TransientError, ServiceUnavailable) as e:
            retries += 1
            time.sleep((2 ** retries) * 0.5)
            if retries == max_retries:
                print(f"Failed to delete batch after {max_retries} retries. Error: {e}")
    return 0

def delete_all_nodes_in_batches(batch_size=5000, num_threads=3, max_retries=3):
    total_deleted = 0
    progress = tqdm(desc="Deleting nodes", unit="batch")
    driver = get_driver()
    try:
        while True:
            future_results = []
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                for _ in range(num_threads):
                    future = executor.submit(delete_batch_with_retries, driver, batch_size, max_retries)
                    future_results.append(future)

                deleted_counts = [future.result() for future in as_completed(future_results)]
            
            batch_total_deleted = sum(deleted_counts)
            total_deleted += batch_total_deleted
            progress.update(1)
            
            if batch_total_deleted < batch_size * num_threads:
                break
    finally:
        close_driver()
        progress.close()

    print(f"Finished deleting nodes. Total nodes deleted: {total_deleted}")

def node_exists(tx, node_name):
    query = (
        "MATCH (n:Category {name: $node_name}) "
        "RETURN n.name AS name"
    )
    result = tx.run(query, node_name=node_name)
    return len(list(result)) > 0
