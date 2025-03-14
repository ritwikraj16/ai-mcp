"""
Main UI Components for RAG-SQL Assistant

This module provides the main Streamlit UI components for the RAG-SQL Assistant,
including page configuration, sidebar, and layout.
"""

import os
import streamlit as st
import base64
import logging
from typing import Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="RAG-SQL Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_sidebar():
    """Render the sidebar with API status and about information."""
    from src.config import get_openai_api_key
    
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

def render_header():
    """Render the application header with logo."""
    # Try to find the OpenAI logo
    try:
        # Define possible paths for the logo
        possible_paths = [
            os.path.join("assets", "openai-logo.png"),
            "repo-to-submit-pr/rag-sql-assistant/assets/openai-logo.png",
            "rag-sql-assistant/assets/openai-logo.png"
        ]
        
        # Also check for assets in the same directory as this file
        assets_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "assets"
        if assets_dir.exists():
            possible_paths.append(str(assets_dir / "openai-logo.png"))
        
        # Try each path
        for path in possible_paths:
            if os.path.exists(path):
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    st.markdown("""
                    # RAG-SQL Assistant powered by <img src="data:image/png;base64,{}" width="200" style="vertical-align: -5px; padding-left: 10px;">
                    """.format(
                        base64.b64encode(open(path, "rb").read()).decode()
                    ), unsafe_allow_html=True)
                    st.subheader("Ask questions using natural language - get answers from SQL or documents!")
                
                with col2:
                    from src.ui.chat import reset_chat
                    st.button("Clear ↺", on_click=reset_chat)
                
                return
        
        # If no logo found, use plain header
        col1, col2 = st.columns([6, 1])
        with col1:
            st.header("RAG-SQL Assistant")
            st.subheader("Ask questions using natural language - get answers from SQL or documents!")
        
        with col2:
            from src.ui.chat import reset_chat
            st.button("Clear ↺", on_click=reset_chat)
            
    except Exception as e:
        logger.exception(f"Error loading logo: {e}")
        st.header("RAG-SQL Assistant")
        st.subheader("Ask questions using natural language - get answers from SQL or documents!")

def render_main_ui(process_query_func):
    """
    Render the main UI components including chat interface.
    
    Args:
        process_query_func: Function to process user queries
    """
    from src.ui.chat import initialize_chat_state, display_chat_history, add_user_message, add_assistant_message
    
    # Initialize chat state
    initialize_chat_state()
    
    # Display chat history
    display_chat_history()
    
    # Accept user input
    if prompt := st.chat_input("Ask a question using natural language..."):
        # Add user message to chat history
        add_user_message(prompt)
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Processing your query..."):
                # Process the query
                response = process_query_func(prompt)
                full_response = str(response["content"])
                
                # Display the response directly
                st.markdown(full_response)
            
            # Add assistant response to chat history
            add_assistant_message(full_response) 