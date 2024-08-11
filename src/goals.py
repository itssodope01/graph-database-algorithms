import sys

# Goal 8
def find_root_node(tx):
    try:
        query = (
            "MATCH (c:Category) "
            "WHERE NOT (c)<-[:HAS_SUBCATEGORY]-() "
            "RETURN c.name AS root"
        )
        result = tx.run(query)
        for record in result:
            yield record["root"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 9
def find_nodes_with_most_children(tx):
    try:
        query = (
            "MATCH (c:Category)-[:HAS_SUBCATEGORY]->(child) "
            "WITH c, COUNT(child) AS children_count "
            "ORDER BY children_count DESC "
            "LIMIT 1 "
            "RETURN c.name AS parent, children_count"
        )
        result = tx.run(query)
        for record in result:
            yield record["parent"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Goal 10
def find_nodes_with_least_children(tx):
    try:
        query = (
            "MATCH (c:Category)-[:HAS_SUBCATEGORY]->(child) "
            "WITH c, COUNT(child) AS children_count "
            "WHERE children_count > 0 "
            "WITH MIN(children_count) AS min_children_count "
            "MATCH (c:Category)-[:HAS_SUBCATEGORY]->(child) "
            "WITH c, COUNT(child) AS children_count, min_children_count "
            "WHERE children_count = min_children_count "
            "RETURN c.name AS parent"
        )
        result = tx.run(query)
        for record in result:
            yield record["parent"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 11
def rename_node(tx, old_name, new_name):
    try:
        # Check if the node with old_name exists
        check_query = "MATCH (c:Category {name: $old_name}) RETURN c"
        result = tx.run(check_query, old_name=old_name)

        if not result.peek():
            # If the node doesn't exist, print a message and return
            print(f"Node with name '{old_name}' does not exist.")
            sys.exit(1)
            return False

        # If the node exists, rename it
        rename_query = "MATCH (c:Category {name: $old_name}) SET c.name = $new_name"
        tx.run(rename_query, old_name=old_name, new_name=new_name)
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# Goal 12
def find_all_paths(tx, start_node, end_node, search_depth):
    try:
        query = (
            f"MATCH p=(start:Category {{name: $start_node}})-[:HAS_SUBCATEGORY*..{search_depth}]->(end:Category {{name: $end_node}}) "
            "RETURN p"
        )
        result = tx.run(query, start_node=start_node, end_node=end_node)
        for record in result:
            path = record["p"]
            nodes = [node["name"] for node in path.nodes]
            yield " --> ".join(nodes)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 1
def find_all_children(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})-[:HAS_SUBCATEGORY]->(child) "
            "RETURN child.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        for record in result:
            yield record["name"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 2
def count_all_children(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})-[:HAS_SUBCATEGORY]->(child) "
            "RETURN COUNT(child) AS count"
        )
        result = tx.run(query, node_name=node_name)
        return result.single()["count"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

# Goal 3
def find_all_grandchildren(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})-[:HAS_SUBCATEGORY]->(:Category)-[:HAS_SUBCATEGORY]->(grandchild) "
            "RETURN grandchild.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        for record in result:
            yield record["name"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 4
def find_all_parents(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})<-[:HAS_SUBCATEGORY]-(parent) "
            "RETURN parent.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        for record in result:
            yield record["name"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 5
def count_all_parents(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})<-[:HAS_SUBCATEGORY]-(parent) "
            "RETURN COUNT(parent) AS count"
        )
        result = tx.run(query, node_name=node_name)
        return result.single()["count"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

# Goal 6
def find_all_grandparents(tx, node_name):
    try:
        query = (
            "MATCH (c:Category {name: $node_name})<-[:HAS_SUBCATEGORY]-(:Category)<-[:HAS_SUBCATEGORY]-(grandparent) "
            "RETURN grandparent.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        for record in result:
            yield record["name"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Goal 7
def count_unique_nodes(tx):
    try:
        query = (
            "MATCH (c:Category) "
            "RETURN COUNT(DISTINCT c.name) AS unique_count"
        )
        result = tx.run(query)
        return result.single()["unique_count"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0


# Helper function to find one shortest path
def find_shortest_path(driver, start_node, end_node):
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH path = ShortestPath((start:Category {name: $start_node})-[:HAS_SUBCATEGORY*]-(end:Category {name: $end_node})) "
                "RETURN path",
                start_node=start_node, end_node=end_node
            )
            for record in result:
                path = record["path"]
                nodes = [node["name"] for node in path.nodes]
                yield " --> ".join(nodes)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

