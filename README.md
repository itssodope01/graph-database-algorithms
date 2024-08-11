# 20 DB2 Pritam Chakraborty

## Name

Graph Database Project

## Introduction

The Project was designed to interact with a graph database representing Wikipedia Main topic Classification categories. It has a command Line utility feature that allows us to query the database efficiently and seamlessly.
Link to Wikipedia classifications: <https://en.wikipedia.org/wiki/Category:Main_topic_classifications>

## Table of Contents

1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Setup](#setup)
7. [Design and Implementation](#design-and-implementation)
8. [Usage](#usage)
9. [Results](#results)
10. [Manual](#manual)
11. [Self Evaluation](#self-evaluation)
12. [Contributing](#contributing)
13. [Support](#support)
14. [License](#license)

## Technologies Used

This Project is build using:

### Neo4j version 5.20.0

### Python version 3.12.3

## Architecture

### Components and Interactions

**Neo4j Database:** Stores the graph data representing Wikipedia classifications.

**Python Scripts:**

import_data.py: Handles importing data from CSV files into Neo4j.

utils.py: Provides utility functions for database operations.

goals.py: Defines functions for various database queries (goals).

dbcli.py: Command-line interface for interacting with the database using the defined goals.

**Configuration File:**

config.py: Stores configuration settings such as database connection details.

### Data Flow

Data Import:
import_data.py reads the data file (taxonomy_iw.csv.gz), processes it, and imports it into Neo4j.

Database Interaction:
dbcli.py reads user commands and executes corresponding functions from goals.py, which interact with the Neo4j database using Cypher queries.

Utility Functions:
utils.py provides shared functions used by other scripts to manage database connections and execute queries.

## Prerequisites

Python 3.12.3 Installation.
Neo4j Installation and server accessibility.
A Virtual environment in the project directory.

Packages & libraries:
Python Neo4j Pandas Package Installation.
Tqdm (optional) for Realtime Progress Tracking
csv, gzip, concurrent.futures, asyncio, time

## Installation

Installations are based on Linux Environment (Ubuntu)

### Installing Neo4j

1. Open a Terminal and run the commands to ensure your system is upto date:

```
sudo apt update
sudo apt upgrade -y
```

2. Add Neo4j repository to pakage manager:

```
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.x' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
```

3. Install Neo4j:
   `sudo apt install neo4j -y`

4. Check Neo4j version to confirm Installation:
   neo4j --version

### Installing Python

1. Install Python with this command:
   `sudo apt install python3 python3-venv python3-pip -y`

### Setting up Virtual Environment and Installing Pakages

1. Go to the project directory and set up a virtual environment:

```
python3 -m venv myenv
source myenv/bin/activate
```

2. With the virtual environment activated, Install neo4j Pandas
   `pip install neo4j pandas`

## Setup

1. In the project directory download the compressed file:
   [taxonomy_iw.csv.gz](taxonomy_iw.csv.gz)

2. In the project directory download all the neccesay files:

   1. [config.py](src/config.py)
   2. [utils.py](src/utils.py)
   3. [import_data.py](src/import_data.py)
   4. [goals.py](src/goals.py)
   5. [dbcli.py](src/dbcli.py)

3. Open a Terminal, and navigate to the project directory
   `cd dbproject`

4. Activate the virtual Environment:
   `source myenv/bin/activate`

5. Enable and Start Neo4j server:

```
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

6. Open the Neo4j browser interface by navigating to http://localhost:7474 in your web browser. The default username is neo4j and you will be prompted to set a password.

   - From the neo4j browser window, it is possible to interact with the database and nodes graphically and interactively.

7. Open the 'config.py' file in a text editor and provide your original uri, username and password and finally save the file.

   - Generally, uri = 'bolt://localhost:7687' and username by default is 'neo4j'

8. In the terminal run this command to import data to neo4j from the compressed file.
   `python import_data.py`

## Design and implementation

1. **Schema Design**:

   - Nodes: Represent categories with property `name`.
   - Relationships: `HAS_SUBCATEGORY` relationship between nodes to represent parent-child relationships.
   - Created a unique constraint on the name property of the Category nodes to ensure each category name is unique.
   - Index is created on the property "name" for all nodes.

2. **Data Import**:

   - **import_data.py**: Imports data from a CSV file (`taxonomy_iw.csv.gz`) into Neo4j. It handles data decompression, batch processing, and error logging.
   - Implemented batch processing in import_data.py to handle large volumes of data efficiently.
   - Managed retries for transient errors during batch processing to ensure data integrity.
   - Importing is done in a multi-threaded environment (using 4 cores).
   - tqdm is used to analyze real time progress

3. **utils.py**: Provides utility functions to interact with the Neo4j database, manage the Neo4j driver, create constraints, create index ,and process batches of data.

4. **Goals Implementation**:
   - **goals.py**: Defines functions for different database operations (goals) such as finding children, parents, grandparents, counting nodes, finding paths, etc.
   - Each goal function uses Cypher queries to interact with Neo4j to fetch or manipulate data.
   - Each query function uses yield to produce results one at a time, allowing the transaction to stay open while results are being processed.
5. **Command Line Interface**:
   - **dbcli.py**: Command-line interface (CLI) tool that interacts with the Neo4j database using the defined goals. It reads user commands and executes corresponding queries using the Neo4j Python driver.
   - The main script iterates over the results from the transaction and prints each result immediately, ensuring that data is streamed and printed as it is found.

## Usage

Activate the virtual environment and use the following commands:

```bash
python dbcli.py <goal_number> [arguments]
```

Available goals:

1. Find children of a node: `python dbcli.py 1 <node_name>`
2. Count children of a node: `python dbcli.py 2 <node_name>`
3. Find grandchildren of a node: `python dbcli.py 3 <node_name>`
4. Find parents of a node: `python dbcli.py 4 <node_name>`
5. Count parents of a node: `python dbcli.py 5 <node_name>`
6. Find grandparents of a node: `python dbcli.py 6 <node_name>`
7. Count unique nodes: `python dbcli.py 7`
8. Find root nodes: `python dbcli.py 8`
9. Find nodes with most children: `python dbcli.py 9`
10. Find nodes with least children: `python dbcli.py 10`
11. Rename a node: `python dbcli.py 11 <old_name> <new_name>`
12. Find paths between nodes: `python dbcli.py 12 <start_node> <end_node> [search_depth]`

## Results

### Check "Results" folder for more intensive query results

[Results](Results)

## Manual

Instructions on how to reproduce the results

**1.** Follow the installation and setup instructions to set up the environment and import data into Neo4j.

**2.** Use the command-line interface (CLI) provided by dbcli.py to run queries. See Usage section to know the commands.

**3.** Refer to the results section to understand the output format and validate against your results.

## Self Evaluation

Problems Faced and Solutions

#### Goal 12 (Find all paths between two given nodes)

Initial Implementation: A simple, synchronous approach that resulted in slow performance (lag and timeouts) for complex scenarios.

Improvements made:

**1. Search Depth:** Introduced a parameter to limit the depth of the search, preventing the algorithm from exploring paths beyond a certain level. This significantly improved efficiency, by not letting the search go down irrelevant branches. By default, the search depth is set to 10 when no value is provided in the CLI.

**2. Asynchronous processing:** To optimize further, I implemented asynchronous processing. The task now first identifies all the child nodes of the start node, then initiates path-finding from each of these child nodes to the end node simultaneously. Each path is printed as soon as it's found using ‘yield’ (a generator for streamed printing).

##### Comparison table of the improvements made

Start Node: "Centuries" ; End node: ""2020s_anime_fimls"

![Optimization-Comparison-Image](Optimization-Comparison.png)

As we can see, when the start and end nodes are not in close proximity and there are many branches to explore, the standard Cypher query may become overwhelmed and unresponsive during an unbounded path search, potentially getting lost in irrelevant branches.

By employing a default search depth of 10, the algorithm efficiently identifies a significant number of relevant paths quickly, striking an optimal balance between search depth and time efficiency. For scenarios where time is not a concern, deeper searches can be conducted by adjusting the custom search depth parameter to explore more extensive paths.

## Support

For assistance or inquiries, please open an issue in the issue tracker or reach out via email at <Pritam.Chakraborty1@outlook.com>

## Contributing

I welcome contributions from the community to improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
