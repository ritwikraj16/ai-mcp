# section 1

from sqlalchemy import create_engine
from llama_index.core.indices.struct_store.sql import SQLDatabase

DB_PATH = "sales.db" 
engine = create_engine(f"sqlite:///{DB_PATH}")
sql_db = SQLDatabase(engine)

# section 2


from llama_index.llms.ollama import Ollama 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

llm = Ollama(model="llama3.1:70b") 
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")

# section 3

from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore

qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant_store = QdrantVectorStore(client=qdrant_client, 
                                 collection_name="my_collection")

# section 4

from llama_index.core.objects import (
    SQLTableNodeMapping, 
    SQLTableSchema, 
    ObjectIndex)

table_node_mapping = SQLTableNodeMapping(sql_db)
table_schema_objs = [
    SQLTableSchema(table_name="city_stats"),
    SQLTableSchema(table_name="customers"),
    # Add all your tables here
]

obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    vector_store=qdrant_store,
)

# section 5

from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine

query_engine = SQLTableRetrieverQueryEngine(
    sql_db, obj_index.as_retriever(similarity_top_k=1, 
                                   embed_model=embed_model, 
                                   llm=llm)
)

question = "Which product has the highest order so far" 
response = query_engine.query(question)
