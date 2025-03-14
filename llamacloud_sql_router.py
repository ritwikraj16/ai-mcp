# -*- coding: utf-8 -*-
"""llamacloud_sql_router.py"""

# Import necessary libraries
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama  
from llama_index.core import VectorStoreIndex, Settings, SQLDatabase
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, insert
from llama_index.readers.file import PDFReader
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool, BaseTool
from llama_index.core.llms import ChatMessage, LLM
from llama_index.core.workflow import Workflow, Event, StartEvent, StopEvent, step
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer
import asyncio
import sys
  
  
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os  

# Get the model path from an environment variable, defaulting to "all-MiniLM-L6-v2"
model_path = os.environ.get("MODEL_PATH", "all-MiniLM-L6-v2")  

hf_model = SentenceTransformer(model_path)  
Settings.embed_model = HuggingFaceEmbedding(model_name=model_path)

# Use Ollama as LLM

try:
    Settings.llm = Ollama(model="mistral", request_timeout=300)
    print("✅ Ollama model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading Ollama model: {e}")
    print("Make sure Ollama is running and the mistral model is available.")
    sys.exit(1)

print("✅ Model Loaded Successfully!")

# Create SQL Database in Memory
engine = create_engine("sqlite:///:memory:", future=True)
metadata_obj = MetaData()

# Create city SQL table
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("state", String(16), nullable=False),
)
metadata_obj.create_all(engine)

# Insert Data
rows = [
    {"city_name": "New York City", "population": 8336000, "state": "New York"},
    {"city_name": "Los Angeles", "population": 3822000, "state": "California"},
    {"city_name": "Chicago", "population": 2665000, "state": "Illinois"},
    {"city_name": "Houston", "population": 2303000, "state": "Texas"},
    {"city_name": "Miami", "population": 449514, "state": "Florida"},
    {"city_name": "Seattle", "population": 749256, "state": "Washington"},
]
with engine.begin() as connection:
    connection.execute(insert(city_stats_table), rows)


# SQL Query Engine
sql_database = SQLDatabase(engine, include_tables=["city_stats"])
sql_query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=["city_stats"]) 



# Get PDF folder path from environment variable, default to "data"
pdf_files_env = os.environ.get("PDF_FILES_PATH", "data")


# Construct file paths dynamically
pdf_files = [
    os.path.join(pdf_files_env, "New York City - Wikipedia.pdf"),
    os.path.join(pdf_files_env, "Chicago - Wikipedia.pdf"),
]


documents = []
pdf_reader = PDFReader()
for pdf in pdf_files:
    try:
        if os.path.exists(pdf):
            print(f"Loading PDF: {pdf}")
            documents.extend(pdf_reader.load_data(pdf))
        else:
            print(f"⚠️ Warning: PDF file not found: {pdf}")
    except Exception as e:
        print(f"❌ Error loading PDF {pdf}: {e}")

# Create Local Vector Index
index = VectorStoreIndex.from_documents(documents, embed_model=Settings.embed_model)
llama_cloud_query_engine = index.as_query_engine()

# Create Tools
sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description="Useful for querying city populations and locations in a SQL database.",
    name="sql_tool"
)

llama_cloud_tool = QueryEngineTool.from_defaults(
    query_engine=llama_cloud_query_engine,
    description="Useful for answering questions about US cities.",
    name="llama_cloud_tool"
)

# Custom Agent Workflow
class InputEvent(Event):
    """Input event."""

class GatherToolsEvent(Event):
    """Gather Tools Event"""
    tool_calls: Any

class ToolCallEvent(Event):
    """Tool Call event"""
    tool_call: Any

class ToolCallEventResult(Event):
    """Tool call event result."""
    msg: ChatMessage

class RouterOutputAgentWorkflow(Workflow):
    """Custom router output agent workflow."""

    def __init__(self, tools: List[BaseTool], timeout: Optional[float] = 10.0, verbose: bool = False):
        """Constructor."""
        super().__init__(timeout=timeout, verbose=verbose)
        self.tools: List[BaseTool] = tools
        self.tools_dict: Dict[str, BaseTool] = {tool.metadata.name: tool for tool in self.tools}
        self.llm: LLM = Settings.llm  
        self.chat_history: List[ChatMessage] = []

    @step()
    async def prepare_chat(self, ev: StartEvent) -> InputEvent:
        message = ev.get("message")
        if message is None:
            raise ValueError("'message' field is required.")
        self.chat_history.append(ChatMessage(role="user", content=message))
        return InputEvent()

    @step()
    async def chat(self, ev: InputEvent) -> StopEvent:
        """Retrieve relevant data from SQL or RAG and return a response."""

        query = self.chat_history[-1].content

        # Example logic to choose the right tool
        if "population" in query or "state" in query:
             result = self.tools_dict["sql_tool"].run(query)
        else:
             result = self.tools_dict["llama_cloud_tool"].run(query)



# Create the Workflow
verbose = os.environ.get("VERBOSE", "False").lower() == "true"

wf = RouterOutputAgentWorkflow(tools=[sql_tool, llama_cloud_tool], verbose=verbose, timeout=600)

# Example Queries


async def main():
    queries = [
        "Which city has the highest population?",
        "What state is Houston located in?",
        "Where is the Space Needle located?",
        "How do people in Chicago get around?",
        "What is the historical name of Los Angeles?"
    ]

    for query in queries:
            try:
                print(f"\nProcessing query: '{query}'")
                result = await wf.run(message=query)
                print(f"Result: {result}")
            except Exception as e:
                print(f"❌ Error processing query '{query}': {e}")

# Run the main function properly
if __name__ == "__main__":
    asyncio.run(main())  # Ensures async execution
