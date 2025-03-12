# Patient Case Summary Generator

This application analyzes patient data, matches conditions against clinical guidelines, and generates comprehensive case summaries for clinicians.

![Workflow Diagram](assets/workflow_diagram.png)

## Overview

The Patient Case Summary Generator is a Streamlit application that:

1. Extracts structured data from patient records in FHIR format
2. Maps conditions to relevant encounters and medications
3. Retrieves applicable clinical guidelines
4. Generates a comprehensive case summary with recommendations

## Features

- Upload patient data in FHIR format
- Extract and analyze patient conditions, encounters, and medications
- Match conditions against evidence-based clinical guidelines
- Generate human-readable case summaries
- Download summaries for clinical use
- Progress tracking with detailed workflow logs
- Caching of intermediate results for improved performance

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/patient-case-summary.git
   cd patient-case-summary
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your environment variables by copying the example file:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   LLAMACLOUD_API_KEY=your_llamacloud_api_key_here
   GUIDELINE_INDEX_NAME=medical_guidelines_0
   GUIDELINE_PROJECT_NAME=llamacloud_demo
   GUIDELINE_ORG_ID=your_organization_id_here
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Upload a patient data file in FHIR format using the sidebar

4. Click "Generate Case Summary" to process the data

5. View the generated case summary and download it for clinical use

## Workflow Architecture

The application follows a modular workflow:

1. **Data Extraction**: Parses FHIR patient bundles to extract demographics, conditions, encounters, and medications
2. **Condition Mapping**: Associates each condition with relevant encounters and medications
3. **Guideline Retrieval**: Queries a vector database of clinical guidelines to find relevant recommendations
4. **Case Summary Generation**: Creates a comprehensive summary with condition-specific insights and recommendations

## Data Privacy

This application processes patient data locally on your machine. No patient information is sent to external servers except for:
- OpenAI API calls for natural language processing
- LlamaCloud API calls for guideline retrieval

Ensure you have appropriate permissions to process any patient data you upload.