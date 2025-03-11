# Required imports
import os
import uuid
import asyncio
import tempfile
import time
import nest_asyncio
from dotenv import load_dotenv
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

# Import necessary components from llama_index
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from tools import setup_document_tool, setup_sql_tool
from workflow import RouterOutputAgentWorkflow

# Configure Opik for Llama Index
import opik
opik.configure(use_local=False)

from llama_index.core.callbacks import CallbackManager
from opik.integrations.llama_index import LlamaIndexCallbackHandler

opik_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([opik_callback_handler])


# Load environment variables
load_dotenv()

# Apply nest_asyncio to allow running asyncio in Streamlit
nest_asyncio.apply()

# Set page configuration
st.set_page_config(
    page_title="RAG & SQL Fusion 🔗",
    page_icon="🏙️",
    layout="wide",
)

# Initialize session state
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

if "workflow" not in st.session_state:
    st.session_state.workflow = None

if "workflow_needs_update" not in st.session_state:
    st.session_state.workflow_needs_update = False


#####################################
# Helper Functions
#####################################
def reset_chat():
    """Reset the chat history and clear context"""
    # Clear messages immediately
    if "messages" in st.session_state:
        st.session_state.messages = []

    if "workflow" in st.session_state and st.session_state.workflow:
        st.session_state.workflow = None
        st.session_state.workflow_needs_update = True


def display_pdf(file_path):
    """Display PDF in the Streamlit app using a dedicated PDF viewer component"""
    try:
        # Use the pdf_viewer component with recommended settings
        pdf_viewer(
            file_path,
            width="100%",  # Use percentage for responsive width
            height=600,  # Fixed height in pixels
            render_text=True,  # Enable text layer for copy-paste
            pages_vertical_spacing=5,  # Add more space between pages
            annotation_outline_size=2,  # Make any annotations more visible
            pages_to_render=[1, 2, 3],  # Render only the first 3 pages
        )

        # Provide download option even when viewer works
        with open(file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=os.path.basename(file_path),
                mime="application/pdf",
            )

    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")
        st.warning("To view the PDF, you can download it using the button below")

        # Fallback to download only
        try:
            with open(file_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_file.read(),
                    file_name=os.path.basename(file_path),
                    mime="application/pdf",
                )
        except Exception as download_error:
            st.error(f"Unable to provide PDF download option: {str(download_error)}")


@st.cache_resource
def initialize_models(api_key=None):
    """Initialize LLM model with the given API key"""
    openai_api_key = api_key or st.secrets.get("OPENAI_API_KEY")
    if not openai_api_key:
        return None

    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Initialize LLM
    llm = OpenAI(model="gpt-4o-mini")

    return llm


def handle_file_upload(uploaded_files):
    """Function to handle multiple file uploads with temporary directory"""
    try:
        # Create a temporary directory if it doesn't exist yet
        if not hasattr(st.session_state, "temp_dir") or not os.path.exists(
            st.session_state.temp_dir
        ):
            st.session_state.temp_dir = tempfile.mkdtemp()

        # Track uploaded files
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []

        # Process each uploaded file
        file_paths = []
        for uploaded_file in uploaded_files:
            # Save file to temporary location
            temp_file_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)

            # Write the file
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Add to list of uploaded files
            st.session_state.uploaded_files.append(
                {"name": uploaded_file.name, "path": temp_file_path}
            )
            file_paths.append(temp_file_path)

        st.session_state.file_uploaded = True
        st.session_state.current_pdf = (
            file_paths[0] if file_paths else None
        )  # Set first file as current for preview
        st.session_state.workflow_needs_update = True  # Mark workflow for update

        return file_paths
    except Exception as e:
        st.error(f"Error uploading files: {str(e)}")
        return None


def set_api_key(api_key):
    """Function to set API key"""
    st.session_state.api_key = api_key
    st.session_state.api_key_set = True


def initialize_workflow(tools):
    """Initialize workflow with the given tools"""
    try:
        workflow = RouterOutputAgentWorkflow(tools=tools, verbose=False, timeout=120)
        st.session_state.workflow = workflow
        return workflow
    except Exception as e:
        st.error(f"Error initializing workflow: {str(e)}")
        return None


async def process_query(query, workflow):
    """Function to process a query using the workflow"""
    try:
        with st.spinner("Processing your query..."):
            result = await workflow.run(message=query)
        return result
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request. Please try a different question."


#####################################
# Main Streamlit app
#####################################
def main():
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")

        # API Key input
        api_key = st.text_input(
            "OpenAI API Key", type="password", help="Enter your OpenAI API key"
        )
        if st.button("Set API Key"):
            set_api_key(api_key)
            st.success("API Key set!")

        # File upload section in the sidebar
        st.subheader("Documents")
        uploaded_files = st.file_uploader(
            "Choose PDF files", type=["pdf"], accept_multiple_files=True
        )

        if uploaded_files:
            if st.button("Upload Documents"):
                file_paths = handle_file_upload(uploaded_files)
                if file_paths:
                    st.success(f"{len(file_paths)} document(s) uploaded")

                    # Display list of uploaded documents
                    st.write("Uploaded documents:")
                    for i, file in enumerate(st.session_state.uploaded_files):
                        st.write(f"- {file['name']}")

        # Status indicators
        st.subheader("Status")
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.api_key_set:
                st.success("API Key: ✓")
            else:
                st.error("API Key: ✗")

        with col2:
            if st.session_state.file_uploaded:
                st.success("Document: ✓")
            else:
                st.warning("Document: ✗")

    # Chat title and reset button in the same row
    chat_header_col1, chat_header_col2 = st.columns([5, 1])
    with chat_header_col1:
        st.title("RAG & SQL Fusion 🔗")
    with chat_header_col2:
        st.button("Reset Chat ↺", on_click=reset_chat)

    # Initialize models if API key is set
    if st.session_state.api_key_set:
        api_key = st.session_state.api_key
        llm = initialize_models(api_key)
        Settings.llm = llm

        # Initialize tools with first tool as SQL tool
        tools = [setup_sql_tool()]

        if st.session_state.file_uploaded:
            file_key = f"{st.session_state.id}-documents"

            if file_key not in st.session_state.file_cache:
                with st.sidebar:
                    with st.spinner(
                        "Processing documents and initializing workflow..."
                    ):
                        # Use the uploaded documents to create a document tool
                        document_tool = setup_document_tool(
                            file_dir=st.session_state.temp_dir
                        )
                        st.session_state.file_cache[file_key] = document_tool
                    st.sidebar.success("Documents loaded successfully!")

            tools.append(st.session_state.file_cache[file_key])

        # Initialize or update workflow with tools
        if not st.session_state.workflow or st.session_state.workflow_needs_update:
            workflow = initialize_workflow(tools)
            st.session_state.workflow_needs_update = False
        else:
            workflow = st.session_state.workflow

        # Display PDF preview if files are uploaded
        if (
            st.session_state.file_uploaded
            and hasattr(st.session_state, "uploaded_files")
            and st.session_state.uploaded_files
        ):
            # Document selector
            doc_names = [doc["name"] for doc in st.session_state.uploaded_files]
            selected_doc = st.selectbox("Select document to preview:", doc_names)

            # Find the selected document path
            selected_path = next(
                (
                    doc["path"]
                    for doc in st.session_state.uploaded_files
                    if doc["name"] == selected_doc
                ),
                None,
            )

            if (
                selected_path
                and os.path.exists(selected_path)
                and os.path.getsize(selected_path) > 0
            ):
                with st.expander("Document Preview", expanded=False):
                    display_pdf(selected_path)
            else:
                st.warning("Selected document not available for preview.")
        else:
            st.info("Upload documents to enable preview.")

        # Chat interface
        if workflow:
            # Create a container for messages with fixed height
            chat_container = st.container(height=500, border=True)

            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # User input at the bottom
            query = st.chat_input("Ask your question...")

            # Process query if submitted
            if query:
                st.session_state.messages.append({"role": "user", "content": query})

                # Update the display inside the container to include all messages
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(query)

                    # Process and show assistant response inside the container
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        message_placeholder.markdown("Thinking...")

                        # Process the query
                        response = asyncio.run(process_query(query, workflow))

                        # Simulate streaming effect for better UX
                        displayed_response = ""
                        words = response.split()
                        for _, word in enumerate(words):
                            displayed_response += word + " "
                            message_placeholder.markdown(displayed_response + "▌")
                            # Adjust delay for natural reading pace
                            time.sleep(0.01)  # Faster typing for better UX

                        # Final display without cursor
                        message_placeholder.markdown(displayed_response)

                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": displayed_response.strip()}
                    )
            else:
                # Display existing messages in the container
                with chat_container:
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
    else:
        # Application information
        st.info("Please enter your OpenAI API key in the sidebar to begin.")
        st.markdown(
            """
            This application uses OpenAI's API to power the assistant. 
            Once you've entered your API key, you'll be able to:
            1. Query information about U.S. cities
            2. Upload and analyze PDF documents
            """
        )


if __name__ == "__main__":
    # Clean up any temporary directories on exit
    if hasattr(st.session_state, "temp_dir") and os.path.exists(
        st.session_state.temp_dir
    ):
        try:
            os.rmdir(st.session_state.temp_dir)
        except:
            pass

    # Run the main Streamlit app
    main()
