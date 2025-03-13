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

#  Load the model manually
hf_model = SentenceTransformer("E:/huggingface_models/all-MiniLM-L6-v2")

# Use only the model name, not the model itself
Settings.embed_model = HuggingFaceEmbedding(model_name="E:/huggingface_models/all-MiniLM-L6-v2")

# Use Ollama as LLM
Settings.llm = Ollama(model="mistral", request_timeout=300)

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
for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.begin() as connection:
        connection.execute(stmt)

# SQL Query Engine
sql_database = SQLDatabase(engine, include_tables=["city_stats"])
sql_query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=["city_stats"])

# Load PDF Documents
pdf_files = [
    r"E:\rag and sql\New York City - Wikipedia.pdf",
    r"E:\rag and sql\Chicago - Wikipedia.pdf",
    r"E:\rag and sql\Houston - Wikipedia.pdf",
    r"E:\rag and sql\Seattle - Wikipedia.pdf",
    r"E:\rag and sql\Miami - Wikipedia.pdf"
]

documents = []
pdf_reader = PDFReader()
for pdf in pdf_files:
    documents.extend(pdf_reader.load_data(pdf))

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
        """Appends msg to chat history and returns response."""
        chat_res = await self.llm.achat(messages=[ChatMessage(role="user", content=self.chat_history[-1].content)])
        ai_message = ChatMessage(role="assistant", content=chat_res.message.content)  # ✅ Fix response parsing
        self.chat_history.append(ai_message)
        return StopEvent(result=ai_message.content)  # ✅ No tool calls



# Create the Workflow
wf = RouterOutputAgentWorkflow(tools=[sql_tool, llama_cloud_tool], verbose=True,timeout = 600)

# Example Queries
import asyncio

async def main():
    queries = [
        "Which city has the highest population?",
        "What state is Houston located in?",
        "Where is the Space Needle located?",
        "How do people in Chicago get around?",
        "What is the historical name of Los Angeles?"
    ]

    for query in queries:
        result = await wf.run(message=query)
        print(result)

# Run the main function properly
if __name__ == "__main__":
    asyncio.run(main())  # Ensures async execution
