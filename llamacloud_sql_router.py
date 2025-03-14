# -*- coding: utf-8 -*-
"""llamacloud_sql_router.py"""

# Standard library imports
import asyncio
import os
import sys
import logging

# Third-party imports
from sentence_transformers import SentenceTransformer
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

# Set up logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Ensure compatibility with Windows event loop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Get the model path from an environment variable, defaulting to "all-MiniLM-L6-v2"
model_path = os.environ.get("MODEL_PATH", "all-MiniLM-L6-v2")

hf_model = SentenceTransformer(model_path)
Settings.embed_model = HuggingFaceEmbedding(model_name=model_path)

# Load Ollama model with retry logic
async def load_ollama_model(max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            Settings.llm = Ollama(model="mistral", request_timeout=300)
            logger.info("✅ Ollama model loaded successfully!")
            return True
        except Exception as e:
            retries += 1
            logger.error(f"❌ Error loading Ollama model (attempt {retries}/{max_retries}): {e}")
            if retries >= max_retries:
                logger.error("Make sure Ollama is running and the Mistral model is available.")
                return False
            logger.info(f"Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)

    return False

# Run Ollama loading
if not asyncio.run(load_ollama_model()):
    sys.exit(1)

logger.info("✅ Model Loaded Successfully!")

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

# Insert Data using bulk insert
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

# Get PDF folder path and ensure it exists
pdf_files_env = os.environ.get("PDF_FILES_PATH", "data")
if not os.path.exists(pdf_files_env):
    logger.warning(f"⚠️ PDF directory '{pdf_files_env}' does not exist. Creating it now.")
    os.makedirs(pdf_files_env, exist_ok=True)

# Load PDF Documents
pdf_files = [
    os.path.join(pdf_files_env, "New York City - Wikipedia.pdf"),
    os.path.join(pdf_files_env, "Chicago - Wikipedia.pdf"),
]

documents = []
pdf_reader = PDFReader()
for pdf in pdf_files:
    try:
        if os.path.exists(pdf):
            logger.info(f"Loading PDF: {pdf}")
            documents.extend(pdf_reader.load_data(pdf))
        else:
            logger.warning(f"⚠️ PDF file not found: {pdf}")
    except Exception as e:
        logger.error(f"❌ Error loading PDF {pdf}: {e}")

# Create Local Vector Index
if documents:
    index = VectorStoreIndex.from_documents(documents, embed_model=Settings.embed_model)
    llama_cloud_query_engine = index.as_query_engine()
    logger.info(f"✅ Vector index created with {len(documents)} documents")
else:
    logger.warning("⚠️ No documents loaded. Creating an empty index.")
    index = VectorStoreIndex.from_documents([], embed_model=Settings.embed_model)
    llama_cloud_query_engine = index.as_query_engine()

# Create Tools
sql_tool = QueryEngineTool.from_defaults(query_engine=sql_query_engine, name="sql_tool")
llama_cloud_tool = QueryEngineTool.from_defaults(query_engine=llama_cloud_query_engine, name="llama_cloud_tool")

# Define custom events
class InputEvent(Event):
    """Event representing user input."""

class GatherToolsEvent(Event):
    """Event representing tool gathering."""
    tool_calls: Any

class ToolCallEvent(Event):
    """Event representing a tool call."""
    tool_call: Any

class ToolCallEventResult(Event):
    """Event representing a tool call result."""
    msg: ChatMessage

# Custom Agent Workflow
# Custom Agent Workflow
class RouterOutputAgentWorkflow(Workflow):
    """Custom router output agent workflow."""

    def __init__(self, tools: List[BaseTool], timeout: Optional[float] = 10.0, verbose: bool = False):
        """Constructor."""
        super().__init__(timeout=timeout, verbose=verbose)
        self.tools = tools
        self.tools_dict = {tool.metadata.name: tool for tool in self.tools}
        self.llm = Settings.llm  
        self.chat_history = []

    @step()
    async def chat(self, ev: InputEvent) -> StopEvent:
        """Retrieve relevant data from SQL or RAG and return a response."""
        query = self.chat_history[-1].content

        if "population" in query or "state" in query:
            result = self.tools_dict["sql_tool"].run(query)
        else:
            result = self.tools_dict["llama_cloud_tool"].run(query)

        # Append response to chat history
        self.chat_history.append(ChatMessage(role="assistant", content=result))
        return StopEvent(result=result)

# Create the Workflow
verbose = os.environ.get("VERBOSE", "False").lower() == "true"
wf = RouterOutputAgentWorkflow(tools=[sql_tool, llama_cloud_tool], verbose=verbose, timeout=600)

# Example Queries
queries = [
    "Which city has the highest population?",
    "What state is Houston located in?",
    "Where is the Space Needle located?",
    "How do people in Chicago get around?",
    "What is the historical name of Los Angeles?"
]

# Main Function to Execute Queries
async def main():
    logger.info("\n--- Starting conversation example ---")
    for query in queries:
        try:
            result = await wf.run(message=query)
            logger.info(f"User: {query}\nAssistant: {result}")
        except Exception as e:
            logger.error(f"❌ Error processing query '{query}': {e}")

# Run the async function properly
if __name__ == "__main__":
    asyncio.run(main())  # Ensures async execution
