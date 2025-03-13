import streamlit as st
import asyncio
import os
from pathlib import Path
from llama_index.llms.openai import OpenAI
from patient_case_summary import GuidelineRecommendationWorkflow, retriever, LogEvent
from llama_index.llms.ollama import Ollama

# Set page configuration for a wider layout and custom title
st.set_page_config(page_title="Patient Case Summary Generator", layout="wide", page_icon="🏥")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: white;
        text-align: center-left;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 24px;
        color: white;
        margin-top: 20px;
    }
    .summary-box {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        white-space: pre-wrap;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        width: 95%;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .description {
        font-size: 20px;
        margin-bottom: 20px;
        margin-right: 40px;
        color: white;
        opacity: 0.5;
            }
    </style>
""", unsafe_allow_html=True)

# App title with custom styling
st.markdown('<div class="main-title">🏥 Patient Case Summary Generator</div>', unsafe_allow_html=True)
# Sidebar for instructions and branding
with st.sidebar:
    st.markdown("### How to Use")
    st.markdown("""
    1. Upload a patient JSON file.
    2. Click 'Generate Summary' to process the data.
    3. View the formatted patient summary.
    """)
    st.markdown("---")
    st.markdown("Powered by Ollama & Streamlit")

# Main content area
col1, col2 = st.columns([2, 1])  # Two-column layout

with col2:
    # File upload with a nicer label
    st.markdown("#### Upload Patient Data")
    uploaded_file = st.file_uploader("Choose a patient JSON file", type=["json"], help="Upload a Synthea-generated FHIR JSON file.")

    # Save uploaded file temporarily if provided
    if uploaded_file:
        patient_json_path = "temp_patient.json"
        with open(patient_json_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully: {uploaded_file.name}")
    else:
        patient_json_path = None

with col1:
    st.markdown('<div class="description">The Patient Case Summary Generator is a Streamlit app that lets healthcare professionals upload patient JSON data to create concise AI-generated summaries. It uses medical guidelines to detail conditions, encounters, and recommendations.</div>', unsafe_allow_html=True)
    # Button with progress feedback
    st.markdown("#### Generate")
    generate_btn = st.button("Generate Summary", key="generate_btn")
    if generate_btn:
        if not patient_json_path or not os.path.exists(patient_json_path):
            st.error("Please upload a valid patient JSON file first.", icon="🚨")
        else:
            with st.spinner("Processing patient data..."):
                # Initialize the workflow
                llm = OpenAI(model="gpt-4o")
                workflow = GuidelineRecommendationWorkflow(
                    guideline_retriever=retriever,
                    llm=llm,
                    verbose=True,
                    timeout=None
                )

                # Define async function to run the workflow
                async def run_workflow():
                    handler = workflow.run(patient_json_path=patient_json_path)
                    response_dict = await handler
                    return response_dict["case_summary"]

                # Run the workflow and display results
                try:
                    case_summary = asyncio.run(run_workflow())
                    
                    # Display the summary in a styled box
                    st.markdown('<div class="subheader">Patient Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-box">{case_summary.render()}</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}", icon="❌")



# Clean up temporary file
if patient_json_path and os.path.exists(patient_json_path):
    os.remove(patient_json_path)