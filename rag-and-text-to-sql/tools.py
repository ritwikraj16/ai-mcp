# Required imports
from sqlalchemy import create_engine
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    SQLDatabase,
)
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import NLSQLTableQueryEngine
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import qdrant_client
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore


#####################################
# Define Tools for Router Agent
#####################################
def setup_sql_tool():
    """Setup SQL query tool for querying city database."""
    # Setup SQLite database
    db_path = "city_database.sqlite"
    engine = create_engine(f"sqlite:///{db_path}")
    sql_database = SQLDatabase(engine)

    # Create SQL query engine
    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["city_stats"],
    )

    # Create tool for SQL querying
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating a natural language query into a SQL query over"
            " a table containing: city_stats, containing the population/state of"
            " each city located in the USA."
        ),
        name="sql_tool",
    )

    # Return the SQL tool
    return sql_tool


def setup_document_tool(file_dir):
    """Setup document query tool from uploaded documents."""
    # Create a reader and load the data
    loader = SimpleDirectoryReader(
        input_dir=file_dir, required_exts=[".pdf"], recursive=True
    )
    docs = loader.load_data()

    # Setup the embedding model
    # embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.embed_model = embed_model

    # Creating a vector index over loaded data
    client = qdrant_client.QdrantClient(host="localhost", port=6333)
    vector_store = QdrantVectorStore(client=client, collection_name="rag_and_sql")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    vector_index = VectorStoreIndex.from_documents(
        docs, show_progress=True, storage_context=storage_context
    )
    # vector_index = VectorStoreIndex.from_documents(docs, show_progress=True)

    # Create a query engine for the vector index
    docs_query_engine = vector_index.as_query_engine(streaming=True)

    # Create tool for document querying
    docs_tool = QueryEngineTool.from_defaults(
        query_engine=docs_query_engine,
        description=(
            "Useful for answering semantic questions about content in the uploaded document."
        ),
        name="document_tool",
    )

    # Return the document tool
    return docs_tool
