# Combining RAG and Text-to-SQL in a Single Query Interface

This project showcases a custom agent using either a vector index for RAG or a SQL database to query data sources, such as Wikipedia PDFs and a city population database.

## Features

- **Dual Query System**:
  - SQL Database queries for structured data analysis
  - RAG-powered retrieval for semantic knowledge
- **Smart Query Routing**: Automatically determines the best tool for each query
- **Interactive UI**: Built with Streamlit for easy interaction
- **Observability**: Integration with Cometml's Opik for monitoring
- **Vector Storage**: Qdrant VectorDB for efficient embedding storage

[Video demo](demo.mp4)
[Twitter/X thread]()

## Project Structure

```
project/
│── sql_data.py         # SQL database population script
│── tools.py            # Both SQL and RAG query handling tools
│── workflow.py         # Main workflow for query routing
│── app.py              # Main Streamlit application
│── README.md           # Project documentation
│── demo.mp4            # Video demo of the project
└── requirements.txt    # Project dependencies
```

## Installation and Setup

### Prerequisites

- Docker for Qdrant (verify with `docker info`)
- Python 3.11 or later
- OpenAI API key
- Comet ML API key

**Setup OpenAI**:

Get an API key from [OpenAI](https://platform.openai.com/api-keys) and set it in the Streamlit UI.

**Setup Opik**:

Get an API key from [Comet ML](https://www.comet.com/) and set it in the terminal when adding observality to the app using Opik.

**Setup Qdrant VectorDB**:

First, pull the Qdrant image:

```bash
docker pull qdrant/qdrant
```

Then run the container:

```bash
docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant
```

**Install Dependencies**:

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

**Run the app**:

Before running the app, populate the SQL database by running:

```bash
python sql_data.py
```

Then, start the Streamlit application:

```bash
streamlit run app.py
```

## How to Use

1. Open the Streamlit UI in your browser (usually at `http://localhost:8501`).
2. Set your OpenAI API key in the UI to enable RAG + Text-to-SQL capabilities.
3. Enter your queries in natural language, such as:
   - "What is the population of Chicago?"
   - "What Native American tribe originally inhabited the Miami area?"
   - "Seattle was struck by which natural disaster in 2001?"
4. The system will automatically:
   - Route structured data queries to the SQL database
   - Send knowledge-based queries to the RAG system
   - Format and display the results
5. Monitor LLM calls and other metrics in the Comet ML dashboard.

## Example Queries

| Query Type  | Example                                             | Processing Method |
| ----------- | --------------------------------------------------- | ----------------- |
| Statistical | "What's the largest city by population?"            | SQL Database      |
| Historical  | "When was Miami officially incorporated as a city?" | RAG System        |
| Hybrid      | "Compare NYC and LA populations and cultures"       | Both Systems      |

## Troubleshooting

1. **Qdrant Connection Issues**:

   - Verify Docker is running
   - Check if the container is accessible on port 6333

2. **API Authentication Errors**:
   - Ensure API keys are correctly set in the UI
   - Verify API quota availability

---

## 📬 Stay Updated with Our Newsletter!

**Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science when you subscribe to our newsletter! Stay in the loop with the latest tutorials, insights, and exclusive resources. [Subscribe now!](https://join.dailydoseofds.com)

[![Daily Dose of Data Science Newsletter](https://github.com/patchy631/ai-engineering/blob/main/resources/join_ddods.png)](https://join.dailydoseofds.com)

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
