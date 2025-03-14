"""
RAG-SQL Assistant

This application provides a Streamlit interface for the RAG-SQL Assistant,
which combines RAG and Text-to-SQL capabilities in a single interface.
"""

import os
import streamlit as st
import uuid
import gc
import logging
import base64
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any, List

# Import from local modules
from src.router.workflow import RouterWorkflow
from src.router.tools import create_rag_tool, create_sql_tool
from src.config import get_openai_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize session state
if "chat_id" not in st.session_state:
    st.session_state.chat_id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.chat_id

# Page configuration
st.set_page_config(
    page_title="RAG-SQL Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def reset_chat():
    """Reset the chat by clearing message history."""
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()

def process_query(query: str) -> Dict[str, Any]:
    """
    Process a user query through the router workflow.
    
    Args:
        query: The user's query string
        
    Returns:
        Dictionary with response content and metadata
    """
    try:
        # Create tools
        rag_tool = create_rag_tool()
        sql_tool = create_sql_tool()
        
        # Initialize router workflow
        router = RouterWorkflow(
            tools=[rag_tool, sql_tool],
            verbose=True,
            llm=None,  # Will use default from config
            chat_history=[]  # Start fresh for each query
        )
        
        # Define an async function to run the workflow
        async def run_workflow():
            return await router.run(message=query)
        
        # Run the async function in a new event loop
        result = asyncio.run(run_workflow())
        
        # Get metadata about which tool was used
        workflow_metadata = {
            "tool_used": "RAG" if "RAG" in str(result) else "SQL"
        }
        
        # If SQL was used, extract the query
        if workflow_metadata["tool_used"] == "SQL":
            # Try to extract SQL query from result
            import re
            sql_match = re.search(r"```sql\n(.*?)\n```", str(result), re.DOTALL)
            if sql_match:
                workflow_metadata["sql_query"] = sql_match.group(1)
            else:
                # Fallback to a simpler pattern
                sql_match = re.search(r"SQL query: (.*?)(?:\n|$)", str(result), re.DOTALL)
                if sql_match:
                    workflow_metadata["sql_query"] = sql_match.group(1)
        
        # If RAG was used, extract sources if available
        elif workflow_metadata["tool_used"] == "RAG":
            # Try to extract sources
            import re
            sources_match = re.search(r"Sources:\n(.*?)(?:\n\n|$)", str(result), re.DOTALL)
            if sources_match:
                sources_text = sources_match.group(1)
                workflow_metadata["rag_sources"] = [s.strip() for s in sources_text.split("\n") if s.strip()]
            
        return {
            "content": result,
            "metadata": workflow_metadata
        }
    except Exception as e:
        logger.exception(f"Error processing query: {e}")
        return {
            "content": f"I encountered an error processing your query: {str(e)}",
            "metadata": {"error": str(e)}
        }

# Sidebar
with st.sidebar:
    st.header("🤖 RAG-SQL Assistant")
    
    # Environment status
    api_key = get_openai_api_key()
    api_status = "✅ Connected" if api_key else "❌ Not Connected"
    
    st.markdown(f"**OpenAI API Status:** {api_status}")
    
    if not api_key:
        st.warning("Please set your OpenAI API key in the .env file.")
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    ### About This Project
    
    This RAG-SQL Assistant demonstrates how to create a hybrid query system that combines 
    the strengths of both retrieval-augmented generation and text-to-SQL capabilities.
    
    The project was created as a demonstration for the Daily Dose of Data Science publication.
    
    **Source Code**: [GitHub Repository](https://github.com/patchy631/ai-engineering-hub)
    """)
    
    st.markdown("""
    ---
    
    ## 📬 Stay Updated with Daily Dose of Data Science!
    
    **Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science 
    when you subscribe to our newsletter!
    
    [Subscribe now!](https://join.dailydoseofds.com)
    """)

# Main content area with column layout
col1, col2 = st.columns([6, 1])

with col1:
    # Use try/except to handle potential image loading errors
    try:
        openai_logo_path = os.path.join("assets", "openai-logo.png")
        if os.path.exists(openai_logo_path):
            st.markdown("""
            # RAG-SQL Assistant powered by <img src="data:image/png;base64,{}" width="200" style="vertical-align: -5px; padding-left: 10px;">
            """.format(
                base64.b64encode(open(openai_logo_path, "rb").read()).decode()
            ), unsafe_allow_html=True)
        else:
            # Logo not found in expected location, try alternative paths
            alt_paths = [
                "repo-to-submit-pr/rag-sql-assistant/assets/openai-logo.png",
                "rag-sql-assistant/assets/openai-logo.png"
            ]
            
            for path in alt_paths:
                if os.path.exists(path):
                    st.markdown("""
                    # RAG-SQL Assistant powered by <img src="data:image/png;base64,{}" width="200" style="vertical-align: -5px; padding-left: 10px;">
                    """.format(
                        base64.b64encode(open(path, "rb").read()).decode()
                    ), unsafe_allow_html=True)
                    break
            else:
                # Still not found, use plain header
                st.header("RAG-SQL Assistant")
    except Exception as e:
        logger.exception(f"Error loading logo: {e}")
        st.header("RAG-SQL Assistant")
        
    st.subheader("Ask questions using natural language - get answers from SQL or documents!")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display tool information if available
        if message["role"] == "assistant" and "metadata" in message and "tool_used" in message["metadata"]:
            tool_used = message["metadata"]["tool_used"]
            st.caption(f"Tool used: {tool_used}")
        
        # Display SQL query if available
        if message["role"] == "assistant" and "metadata" in message and "sql_query" in message["metadata"]:
            sql_query = message["metadata"]["sql_query"]
            with st.expander("View SQL Query"):
                st.code(sql_query, language="sql")
        
        # Display RAG sources if available
        if message["role"] == "assistant" and "metadata" in message and "rag_sources" in message["metadata"]:
            rag_sources = message["metadata"]["rag_sources"]
            with st.expander("View Sources"):
                for source in rag_sources:
                    st.markdown(f"- {source}")

# Accept user input
if prompt := st.chat_input("Ask a question using natural language..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Processing your query..."):
            # Process the query
            response = process_query(prompt)
            full_response = str(response["content"])
            
        # Display the response with streaming-like effect for better user experience
        message_placeholder.markdown(full_response + "▌")
        import time
        time.sleep(0.1)  # Brief pause for visual effect
        message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history with metadata
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "metadata": response["metadata"]
        })
