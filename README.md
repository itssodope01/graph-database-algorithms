# 20 DB2 Pritam Chakraborty


## Name
Graph Database Project

## Description
The Project was designed to interact with a graph database representing Wikipedia Main topic Classification categories. It has a command Line utility feature that allows us to query the database efficiently and seamelessly. 
Link to Wikipidea classifications: https://en.wikipedia.org/wiki/Category:Main_topic_classifications

## Choice of Technology
This Project is build using:
### Neo4j version 5.20.0
### Python version 3.12.3

## Architechture

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



## Requirements (Prerequisites)
Phython 3.12.3 Installation.
Neo4j Installation and server accecibility.
A Virtual environment in the project directory.

Pakages & libraries: 
Python Neo4j Pandas Pakage Installation.
Tqdm (optional) for Realtime Progress Tracking 
csv, gzip, concurrent.futures, asyncio, time 

## Installation
Installations are based on Linux Environment (Ubuntu)
### Installing Neo4j
1) Open a Terminal and run the commands to ensure your system is upto date:
```
sudo apt update
sudo apt upgrade -y
```


2) Add Neo4j repository to pakage manager:
```
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.x' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
```


3) Install Neo4j:
`sudo apt install neo4j -y`

4) Check Neo4j version to confirm Installation:
neo4j --version

### Installing Python
1) Install Python with this command:
`sudo apt install python3 python3-venv python3-pip -y`

### Setting up Virtual Environment and Installing Pakages
1) Go to the project directory and set up a virtual environment:
```
python3 -m venv myenv
source myenv/bin/activate
```
2) With the virtual environment activated, Install neo4j Pandas
`pip install neo4j pandas`

## Setup (you can download the required files from this repository)
1) In the project directory download the compressed file:
`taxonomy_iw.csv.gz` 

2) In the project directory download all the neccesay files:
```
   a) config.py
   b) utils.py
   c) import_data.py
   d) goals.py
   e) dbcli.py
```

3) Open a Terminal, and navigate to the project directory
`cd dbproject`

4) Activate the virtual Environment:
`source myenv/bin/activate`

5) Enable and Start Neo4j server:
```
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

6) Open the Neo4j browser interface by navigating to http://localhost:7474 in your web browser. The default username is neo4j and you will be prompted to set a password. 
     - From the neo4j browser window, it is possible to interact with the database and nodes graphically and interactively.

7) Open the 'config.py' file in a text editor and provide your original uri, username and password and finally save the file.
     - Generally, uri = 'bolt://localhost:7687' and username by default is 'neo4j'

8) In the terminal run this command to import data to neo4j from the compressed file.
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

## Usage (User manual)

Open terminal and navigate to the project directory, then activate the virtual environment we created earlier with ```source myenv/bin/activate``` command, strat neo4j with ```sudo systemctl start neo4j```, now you are ready to run the cli commands below:

```
- python dbcli.py 1 <node> 
- python dbcli.py 2 <node> 
- python dbcli.py 3 <node> 
- python dbcli.py 4 <node> 
- python dbcli.py 5 <node> 
- python dbcli.py 6 <node> 
- python dbcli.py 7 
- python dbcli.py 8 
- python dbcli.py 9 
- python dbcli.py 10 
- python dbcli.py 11 <old_node-name> <New_node-name> 
- python dbcli.py 12 <start Node> <End Node> 
- python dbcli.py 12 <start Node> <End Node> <custom_Search_Depth>
```

## Results 
### Check "Results" folder for more intensive query results

1) Finds all children of a given node
```
python dbcli.py 1 1880s_films
Child [1880s_films]: 1880s_dance_films
Child [1880s_films]: 1880s_lost_films
Child [1880s_films]: Lists_of_1880s_films
Child [1880s_films]: 1880s_directorial_debut_films
Child [1880s_films]: 1888_films
Child [1880s_films]: 1887_films
Child [1880s_films]: 1889_films
Goal 1 executed in 0.0056 seconds.

```
2) Counts all children of a given node
```
python dbcli.py 2 1880s_films
Total children of '1880s_films': 7
Goal 2 executed in 0.0063 seconds.

```
3) Finds all grand children of a given node
```
python dbcli.py 3 1880s_films
Grandchild [1880s_films]: 1887_directorial_debut_films
Grandchild [1880s_films]: 1887_directorial_debut_films
Goal 3 executed in 0.0053 seconds.
```
4) Finds all parents of a given node
```
python dbcli.py 4 1880s_films
Parent [1880s_films]: 19th-century_films
Parent [1880s_films]: Films_by_decade
Parent [1880s_films]: 1880s_in_film
Parent [1880s_films]: 1880s_works
Goal 4 executed in 0.0055 seconds.
```
5) Counts all parents of a given node
```
python dbcli.py 5 1880s_films
Total parents of '1880s_films': 4
Goal 5 executed in 0.0065 seconds.

```
6) Finds all grand parents of a given node
```
python dbcli.py 6 1880s_films
Grandparent [1880s_films]: 19th_century_in_film
Grandparent [1880s_films]: Films_by_century
Grandparent [1880s_films]: 19th-century_works
Grandparent [1880s_films]: Works_by_type_and_decade
Grandparent [1880s_films]: Arts_by_decade
Grandparent [1880s_films]: Films_by_date
Grandparent [1880s_films]: 1880s_works
Grandparent [1880s_films]: 1880s_in_the_arts
Grandparent [1880s_films]: Film_by_decade
Grandparent [1880s_films]: 1880s
Grandparent [1880s_films]: 19th_century_in_film
Grandparent [1880s_films]: 1880s_in_mass_media
Grandparent [1880s_films]: 1880s_in_the_arts
Grandparent [1880s_films]: 19th-century_works
Grandparent [1880s_films]: Works_by_decade
Grandparent [1880s_films]: 1880s
Goal 6 executed in 0.0051 seconds.

```
7) Counts how many uniquely named nodes there are
```
python dbcli.py 7 1880s_films
Total unique nodes: 2031337
Goal 7 executed in 0.2233 seconds.

```
8) Finds a root node, one which is not a subcategory of any other node
```
python dbcli.py 8
check goal8_results.txt
```

9) Finds nodes with the most children
```
python dbcli.py 9
Node with the most children: Albums_by_artist
Goal 9 executed in 2.8951 seconds.
```
10) Finds nodes with the least children (number of children is greater than zero)
```
python dbcli.py 10
check goal10_results.txt
```
11) Renames a given node
```
case 1:
python dbcli.py 11 mynode rename_mynode
Node with name 'mynode' does not exist.
Goal 11 executed in 0.0059 seconds.

case 2:
python dbcli.py 11 new_node_name 1880s_films
Renamed node 'new_node_name' to '1880s_films' successfully.
Goal 11 executed in 0.0132 seconds.
```
12) Find all paths from start to end Node. 
```
python dbcli.py 12 21st-century_films 2020s_anime_films

Path: 21st-century_films -->  21st-century_animated_films --> 2020s_animated_films --> 2020s_anime_films

Path: 21st-century_films -->  2020s_films --> 2020s_Japanese_films --> 2020s_anime_films

Path: 21st-century_films -->  2020s_films --> 2020s_animated_films --> 2020s_anime_films

Total Paths Found: 3
Search Depth: 10
To increase Search Depth, Usage: dbcli 12 <start_node> <end_node> [search_depth]
Goal 12 executed in 0.0398 seconds.

Check "goal_12_results.txt" file in "Results" directory:

Path: History -->  Chronology --> Centuries --> Centuries_by_country --> Centuries_in_Japan --> 21st_century_in_Japan --> 2020s_in_Japan --> 2020s_anime --> 2020s_anime_films

Total Paths Found: 3434
Search Depth: 10
To increase Search Depth, Usage: dbcli 12 <start_node> <end_node> [search_depth]
Goal 12 executed in 141.9033 seconds.

```
If no paths are found within the default or specified search depth, the shortest path is printed (if there is one).

## Manual /Instructions on how to reproduce the results

**1.** Follow the installation and setup instructions to set up the environment and import data into Neo4j.

**2.** Use the command-line interface (CLI) provided by dbcli.py to run queries. See Usage section to know the commands. 

**3.** Refer to the results section to understand the output format and validate against your results.

## Problems Faced and Solutions (Self Evaluation)

#### Goal 12 (Find all paths between two given nodes)
Initial Implementation: A simple, synchronous approach that resulted in slow performance (lag and timeouts) for complex scenarios. 

Improvements made:  

**1. Search Depth:** Introduced a parameter to limit the depth of the search, preventing the algorithm from exploring paths beyond a certain level. This significantly improved efficiency, by not letting the search go down irrelevant branches. By default, the search depth is set to 10 when no value is provided in the CLI.

**2. Asynchronous processing:** To optimize further, I implemented asynchronous processing. The task now first identifies all the child nodes of the start node, then initiates path-finding from each of these child nodes to the end node simultaneously. Each path is printed as soon as it's found using ‘yield’ (a generator for streamed printing).

##### Comparison table of the improvements made
Start Node: "Centuries" ; End node: ""2020s_anime_fimls"

+------------------+----------------+----------------+----------------+------------------+
| Feature          | Standard Cypher| APOC Library   | + Specific Depth| + Async Processing|
+------------------+----------------+----------------+----------------+------------------+
| Cypher Query     | Yes            | Yes            | Yes            | Yes              |
+------------------+----------------+----------------+----------------+------------------+
| Search Depth     | Unbounded      | Unbounded      | 10             | 10               |
+------------------+----------------+----------------+----------------+------------------+
| Asynchronization | No             | No             | No             | Yes              |
+------------------+----------------+----------------+----------------+------------------+
| Time Taken       | > 1hr          | 42.29 sec      | 83.33 sec      | 21.25 sec        |
|                  | (unresponsive) |  >unresponsive |                |
+------------------+----------------+----------------+----------------+------------------+
| Paths Discovered | 0              | 159            | 389            | 389              |
+------------------+----------------+----------------+----------------+------------------+

As we can see, when the start and end nodes are not in close proximity and there are many branches to explore, the standard Cypher query may become overwhelmed and unresponsive during an unbounded path search, potentially getting lost in irrelevant branches.

By employing a default search depth of 10, the algorithm efficiently identifies a significant number of relevant paths quickly, striking an optimal balance between search depth and time efficiency. For scenarios where time is not a concern, deeper searches can be conducted by adjusting the custom search depth parameter to explore more extensive paths.

## Support
For assistance or inquiries, please open an issue in the issue tracker or reach out via email at pritam@student.agh.edu.pl


## Contributing
I welcome contributions from the community to improve this project.

## Authors and acknowledgment
Original Author: Pritam Chakraborty