"""
Test Script for RAG-SQL Router

This script tests the functionality of the router workflow by initializing
all components and running a few sample queries.
"""

import asyncio
import nest_asyncio

from src.database.city_stats import CityStatsDB
from src.rag.cloud_index import LlamaCloudRAG
from src.router.tools import get_all_tools
from src.router.workflow import RouterOutputAgentWorkflow
from src.config import enable_tracing

# Apply nest_asyncio to allow running asyncio in notebooks/scripts
nest_asyncio.apply()

# Enable tracing if configured
phoenix_api_key = enable_tracing()

# Initialize components
def initialize_components():
    """
    Initialize the database, RAG, and router components.
    
    Returns:
        tuple: (city_stats_db, llama_cloud_rag, workflow)
    """
    print("Initializing city database...")
    city_stats_db = CityStatsDB()
    city_stats_db.populate_default_data()
    
    print("Initializing LlamaCloud RAG...")
    llama_cloud_rag = LlamaCloudRAG()
    
    print("Setting up tools and workflow...")
    tools = get_all_tools(city_stats_db, llama_cloud_rag)
    workflow = RouterOutputAgentWorkflow(tools=tools, verbose=True, timeout=60)
    
    return city_stats_db, llama_cloud_rag, workflow

# Test with sample queries
async def test_queries(workflow):
    """
    Test the workflow with various types of queries.
    
    Args:
        workflow: The initialized workflow
    """
    # SQL-based query
    print("\n=== Testing SQL Query ===")
    sql_query = "What's the population of Miami?"
    print(f"Query: {sql_query}")
    result = await workflow.run(message=sql_query)
    print(f"Response: {result}")
    
    # Reset chat history between queries
    workflow.reset()
    
    # RAG-based query
    print("\n=== Testing RAG Query ===")
    rag_query = "Tell me about the history of Chicago."
    print(f"Query: {rag_query}")
    result = await workflow.run(message=rag_query)
    print(f"Response: {result}")
    
    workflow.reset()
    
    # Mixed query
    print("\n=== Testing Mixed Query ===")
    mixed_query = "What's the largest city in Texas and what is it known for?"
    print(f"Query: {mixed_query}")
    result = await workflow.run(message=mixed_query)
    print(f"Response: {result}")

# Main test function
async def main():
    """Main test function."""
    city_stats_db, llama_cloud_rag, workflow = initialize_components()
    await test_queries(workflow)

# Run the tests
if __name__ == "__main__":
    print("Starting RAG-SQL Router tests...")
    asyncio.run(main())
    print("\nTests completed.") 