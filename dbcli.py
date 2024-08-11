import sys
import asyncio
import time
from neo4j import GraphDatabase
from utils import get_driver, close_driver, node_exists, delete_all_nodes_in_batches
from goals import (
    find_root_node,
    find_nodes_with_most_children, find_nodes_with_least_children, rename_node,
    find_all_paths, find_all_children, count_all_children, find_all_grandchildren,
    find_all_parents, count_all_parents, find_all_grandparents, count_unique_nodes, find_shortest_path
)

def find_child_nodes(tx, start_node):
    query = (
        "MATCH (start:Category {name: $start_node})-[:HAS_SUBCATEGORY]->(child) "
        "RETURN child.name AS name"
    )
    result = tx.run(query, start_node=start_node)
    return [record["name"] for record in result]

def find_paths_sync(driver, start_node, end_node, search_depth, root_node):
    try:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                total_paths = 0
                for path in find_all_paths(tx, start_node, end_node, search_depth):
                    path_str = ' --> '.join([str(node) for node in path])
                    print(f"Path: {root_node} -->  {path}\n")
                    total_paths += 1
                return total_paths
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

async def find_paths_async(driver, start_node, end_node, search_depth, root_node):
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, find_paths_sync, driver, start_node, end_node, search_depth, root_node)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

async def main():
    if len(sys.argv) < 2:
        print("Usage: python dbcli.py <goal_number> [args]")
        sys.exit(1)

    goal = int(sys.argv[1])
    args = sys.argv[2:]

    driver = get_driver()
    start_time = time.time()

    try:
        if goal == 12:
            if len(args) < 2 or len(args) > 3:
                print("Usage: dbcli 12 <start_node> <end_node> [search_depth]")
                sys.exit(1)
            start_node = args[0]
            end_node = args[1]
            search_depth = int(args[2]) if len(args) == 3 else 10

            if search_depth == 0:
                print(f"Searching at depth 0 is not possible.")
                print("Operation aborted.")
                sys.exit(1)

            if search_depth > 10:
                confirm = input(f"Searching all paths at a depth of {search_depth} can be time-consuming.\nDo you want to continue? (Y/n): ")
                start_time = time.time()
                if confirm.lower() != 'y':
                    print("Operation aborted.")
                    sys.exit(1)

            with driver.session() as session:
                with session.begin_transaction() as tx:
                    if not node_exists(tx, start_node):
                        print(f"Node '{start_node}' does not exist in the database.")
                        sys.exit(1)
                    if not node_exists(tx, end_node):
                        print(f"Node '{end_node}' does not exist in the database.")
                        sys.exit(1)
                    child_nodes = find_child_nodes(tx, start_node)

            print("")
            search_depth -= 1
            tasks = [find_paths_async(driver, child, end_node, search_depth, start_node) for child in child_nodes]
            total_paths = sum(await asyncio.gather(*tasks))
            found_all_path_time = time.time()
            if total_paths == 0:
                print(f"No Paths found within search depth of {search_depth+1}.")
                for shortest_path in find_shortest_path(driver, start_node, end_node):
                    print(f"\nOne Shortest Path: {shortest_path}\n")
            search_depth += 1
            print(f"Total Paths Found: {total_paths}")
            print(f"Search Depth: {search_depth}")

            if len(args) == 2:
                print(f"To increase Search Depth, Usage: dbcli 12 <start_node> <end_node> [search_depth]")

        else:
            with driver.session() as session:
                node_goals = [1,2,3,4,5,6]

                if goal in node_goals:
                    if len(args) != 1:
                        print(f"Usage: python dbcli.py {goal} <node_name>")
                        sys.exit(1)
                    node_name = args[0]
                    with session.begin_transaction() as tx:
                        if not node_exists(tx, node_name):
                            print(f"Node '{node_name}' does not exist in the database.")
                            sys.exit(1)

                        if goal == 1:
                            for child in find_all_children(tx, node_name):
                                print(f"Child [{node_name}]: {child}")

                        elif goal == 2:
                            count = count_all_children(tx, node_name)
                            print(f"Total children of '{node_name}':", count)

                        elif goal == 3:
                            for grandchild in find_all_grandchildren(tx, node_name):
                                print(f"Grandchild [{node_name}]: {grandchild}")

                        elif goal == 4:
                            for parent in find_all_parents(tx, node_name):
                                print(f"Parent [{node_name}]: {parent}")

                        elif goal == 5:
                            count = count_all_parents(tx, node_name)
                            print(f"Total parents of '{node_name}':", count)
                        elif goal == 6:
                            for grandparent in find_all_grandparents(tx, node_name):
                                print(f"Grandparent [{node_name}]: {grandparent}")

                elif goal == 7:
                    with session.begin_transaction() as tx:
                        count = count_unique_nodes(tx)
                        print("Total unique nodes:", count)
                elif goal == 8:
                    with session.begin_transaction() as tx:
                        for root in find_root_node(tx):
                            print("Root node:", root)
                elif goal == 9:
                    with session.begin_transaction() as tx:
                        for node in find_nodes_with_most_children(tx):
                            print("Node with the most children:", node)
                elif goal == 10:
                    least_count = 0
                    with session.begin_transaction() as tx:
                        for node in find_nodes_with_least_children(tx):
                            print("Node with the least children:", node)
                            least_count += 1
                        print(f"Count : {least_count}")
                elif goal == 11:
                    if len(args) != 2:
                        print("Usage: python dbcli.py 11 <old_name> <new_name>")
                        sys.exit(1)
                    old_name, new_name = args
                    success = rename_node(session, old_name, new_name)
                    if success:
                        print(f"Renamed node '{old_name}' to '{new_name}' successfully.")
                elif goal == 13: #Deleting All Nodes from database
                    batch_size = int(args[0]) if args else 5000
                    delete_all_nodes_in_batches(batch_size, 3, 3)
                else:
                    print("Invalid goal number")
                    sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Goal {goal} executed in {execution_time:.4f} seconds.")

    close_driver()

if __name__ == "__main__":
    asyncio.run(main())
