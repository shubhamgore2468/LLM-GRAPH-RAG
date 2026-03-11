import os
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import logging

load_dotenv()

_graph_instance = None

def get_graph() -> Neo4jGraph:
    """Get a Neo4jGraph instance with the configured connection."""
    global _graph_instance

    if _graph_instance is None:
        logging.info("Graph instance not found. Creating new neo4j conection.")
        try:
            _graph_instance = Neo4jGraph()
            _graph_instance.query(
                    "CREATE FULLTEXT INDEX entity IF NOT EXISTS FOR (e:__Entity__) ON EACH [e.id]"
                )
            _graph_instance.query(
                "CREATE VECTOR INDEX `new_vector_index` IF NOT EXISTS FOR (d:Document) ON (d.embedding) OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}}"
            )
            logging.info("Successfully created graph instance and ensured indexes exist.")
        except Exception as e:
            logging.error(f"Failed to create Neo4j graph instance or indexes: {e}", exc_info=True)
            raise

    return _graph_instance