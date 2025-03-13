from sqlalchemy import create_engine, text
from llama_index.core.indices.struct_store.sql import SQLDatabase
from llama_index.core.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq 
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)  

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")  

engine = create_engine("sqlite:///:memory:")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            score INTEGER
        )
    """))
    conn.execute(text("""
        INSERT INTO students (name, score) VALUES 
        ('Alice', 85), 
        ('Bob', 75), 
        ('Charlie', 90)
    """))
    conn.commit()

sql_db = SQLDatabase(engine)

query_engine = NLSQLTableQueryEngine(sql_database=sql_db, embed_model=embed_model, llm=llm)


# question = "How many students scored above 80?"
# response = query_engine.query(question)

print(NLSQLTableQueryEngine.__doc__)
