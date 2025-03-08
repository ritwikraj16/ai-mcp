from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import asyncio
import re
import os

from utils.sql_engine import retrieve_sql_tool
from utils.rag_engine import retrieve_rag_tool
from utils.agent import RouterOutputAgentWorkflow

def format_response(response):
    """
    Automatically detects lists and formats them into proper markdown bullet points.
    Preserves introductory text before the list.
    """
    # Try to detect an introductory sentence followed by a list
    match = re.match(r"^(.*?:)(.*)$", response, re.DOTALL)
    
    if match:
        intro, list_part = match.groups()
        list_items = [item.strip() for item in list_part.split(", ") if item.strip()]
        
        # If the detected part has multiple items, convert it into a Markdown list
        if len(list_items) > 1:
            formatted_list = "\n".join(f"- {item}" for item in list_items)
            return f"{intro}\n\n{formatted_list}"  # Keep intro, add space before list
    
    return response

# Load environment variables from .env
load_dotenv()

# Define the OpenAI LLM
Settings.llm = OpenAI("gpt-3.5-turbo")

# Initialize the chatbot workflow
sql_tool = retrieve_sql_tool()
rag_tool = retrieve_rag_tool()
wf = RouterOutputAgentWorkflow(tools=[sql_tool, rag_tool], verbose=True, timeout=120)

# Initialize Streamlit app
st.set_page_config(page_title="City Explorer Chatbot", page_icon="🌆")
st.title("City Explorer Chatbot🌆")

# Add sidebar with tool description
st.sidebar.title("About This Chatbot")
st.sidebar.image(os.path.dirname(os.path.abspath(__file__)) + "/assets/us_cities.jpeg")
st.sidebar.info(
    "Welcome to the City Explorer Chatbot! This tool helps you find key attractions, places to visit, and "
    "other essential details about major U.S. cities. "
    "Currently, we support queries related to **New York City, Los Angeles, Chicago, Houston, Miami, and Seattle**. "
    "Simply type in your question, and our AI will retrieve useful information from structured databases and knowledge sources."
)

# Initialize session state for chat history if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
if user_input := st.chat_input("Ask about New York City, Los Angeles, Chicago, Houston, Miami, or Seattle..."):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response from agent
    async def get_response(user_input):
        return await wf.run(message=user_input)

    response = asyncio.run(get_response(user_input))
    formatted_response = format_response(response)
    with st.chat_message("assistant"):
        st.markdown(formatted_response, unsafe_allow_html=True)
    
    # Append agent response to chat history
    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
