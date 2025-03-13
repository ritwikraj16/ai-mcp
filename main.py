import streamlit as st
import asyncio

# Import the RouterOutputAgentWorkflow (assuming `wf` is defined in llamacloud_sql_router.py)
from llamacloud_sql_router import wf  

# Streamlit UI
st.set_page_config(page_title="RAG and Text-to-SQL", page_icon="📊", layout="wide")

# Sidebar for instructions and query history
with st.sidebar:
    st.header("Combining RAG and Text-to-SQL in a Single Query Interface ")
    st.write("Ask any question, and AI will answer.")
    st.markdown("---")
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if st.session_state.query_history:
        st.subheader("📜 Query History")
        for i, q in enumerate(st.session_state.query_history[-5:]):
            st.text(f"{i+1}. {q}")
    st.markdown("---")
    if st.button("Clear History"):
        st.session_state.query_history = []

# Main content
st.title("RAG and Text-to-SQL")
query = st.text_input("💡 Enter your query:")

async def get_response(query):
    if query:
        result = await wf.run(message=query)
        return result
    return None

# Display response when button is clicked
col1, col2 = st.columns([3, 1])
with col2:
    get_answer = st.button("🚀 Get Answer")

if get_answer:
    if query.strip():
        st.session_state.query_history.append(query)
        with st.spinner("🤖 Thinking..."):
            response = asyncio.run(get_response(query))
            if response:
                st.toast("✅ Answered successfully")
                st.write(response)
            else:
                st.warning("⚠️ No data available for this query.")
    else:
        st.warning("⚠️ Please enter a query.")
