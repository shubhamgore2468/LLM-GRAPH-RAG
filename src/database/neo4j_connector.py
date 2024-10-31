from neo4j import GraphDatabase
import os

os.environ['NEO4J_USERNAME'] = NEO4J_USERNAME
os.environ['NEO4J_PASSWORD'] = NEO4J_PASSWORD
os.environ['NEO4J_URI'] = NEO4J_URI
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph()

# driver = GraphDatabase.driver(uri, auth=(username, password))

# # Example: Create a node
# with driver.session() as session:
#     session.run("CREATE (n:Person {name: 'Alice'})")

# driver.close()

# # Stop and remove the container
# subprocess.run(["docker", "stop", "my-neo4j-instance"])
# subprocess.run(["docker", "rm", "my-neo4j-instance"])