import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Import required modules from our package
from src.indices import retriever
from src.workflow import AutoInsuranceWorkflow, LogEvent

st.set_page_config(
    page_title="ClaimSonic: Auto Claim Wizard",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Helper to Display Step Logs in Sidebar
def display_log(message: str, color: str = "#4CAF50"):
    st.markdown(f"""
    <div style="padding: 8px; margin-bottom: 6px; background-color: {color}; color: white; border-radius: 4px;">
      {message}
    </div>
    """, unsafe_allow_html=True)

# Instantiate the workflow (verbose mode enabled)
workflow = AutoInsuranceWorkflow(policy_retriever=retriever, verbose=True, timeout=None)

# Function to Run the Workflow Asynchronously
async def run_workflow(claim_json_text: str):
    st.write("Running the Claim Workflow...")
    handler = workflow.run(claim_json_text=claim_json_text)
    async for event in handler.stream_events():
        if isinstance(event, LogEvent):
            display_log(event.msg)
    return await handler

# Custom CSS for Styling
st.markdown("""
<style>
.main {
    background-color: #f9fafb;
    font-family: 'Inter', sans-serif;
}
.decision-output {
   background-color: #1E1E1E;
   border-radius: 10px;
   padding: 1rem;
   margin-top: 1.5rem;
   box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
   color: #ffffff;
}
.decision-output h4 {
   color: #ffffff;
   margin-bottom: 0.5rem;
}
.decision-output p {
   margin: 0.5rem 0;
}
.decision-output .number {
   color: #FFD700;
   font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Main Content Container
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.header("Cars insurance claim")
st.markdown("<p class='subheader'>claim adjuster's smart assistant for processing auto insurance claims.</p>", unsafe_allow_html=True)
st.info("Please input a JSON with details from the claims portal, including claim number, date of loss, claimant name, policy number, loss description, estimated repair cost, and vehicle details.")

# Use a text area for JSON Input
claim_json_input = st.text_area(
    "Enter Claim JSON",
    value="""{
  "claim_number": "",
  "policy_number": "",
  "claimant_name": "",
  "date_of_loss": "",
  "loss_description": "",
  "estimated_repair_cost": 0.0,
  "vehicle_details": ""
}""",
    height=200
)

if st.button("Run Claim Workflow"):
    with st.spinner("Generating decision..."):
        result = asyncio.run(run_workflow(claim_json_input))
        decision = result["decision"]
        st.markdown(f"""
        <div class='decision-output'>
            <h4>Final Claim Decision</h4>
            <p><strong>Claim Number:</strong> <span class="number">{decision.claim_number}</span></p>
            <p><strong>Covered:</strong> <span class="number">{'Yes' if decision.covered else 'No'}</span></p>
            <p><strong>Deductible:</strong> <span class="number">${decision.deductible:.2f}</span></p>
            <p><strong>Recommended Payout:</strong> <span class="number">${decision.recommended_payout:.2f}</span></p>
            <p><strong>Notes:</strong> {decision.notes}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)