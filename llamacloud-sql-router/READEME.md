# LlamaCloud SQL Router: An Intelligent Query Router

This repository demonstrates how to build a custom agent that intelligently routes queries between different data sources - specifically a LlamaCloud index for RAG-based retrieval and a SQL database for structured data queries.

![System Overview](media/image3.png)

## Overview

In this project, we create an agentic system that can:
- Accept natural language questions about US cities
- Intelligently decide which data source to query based on the question
- Retrieve information from either unstructured or structured data
- Present a coherent answer back to the user

The data is divided into two types:
1. **Unstructured data:** PDFs of Wikipedia pages about US cities, stored in LlamaCloud with vector indexing for semantic search
2. **Structured data:** A SQLite database containing structured information about cities (population, state)

## Features

- Automatic intelligent routing of queries to the appropriate system
- Integration of both RAG and SQL capabilities in a single interface
- Conversational context maintained across multiple queries
- Extensible workflow architecture for adding new tools

## Demo

Here's what the application looks like when running:

![Demo Screenshot 1](media/image1.png)
![Demo Screenshot 2](media/image2.png)

## Technologies Used

- **LlamaIndex Cloud**: For generating and storing vector embeddings of unstructured data
- **SQLAlchemy**: For accessing and querying structured data
- **OpenAI**: For generating embeddings and handling natural language queries
- **Streamlit**: For creating a simple user interface
- **LlamaIndex Workflow**: For orchestrating the agent's decision making process

## System Architecture

The system follows this architecture:

![System Architecture](media/image4.png)

The workflow consists of:
1. User submits a question through the UI
2. A router agent decides which tool to use for retrieving contextual data
3. The appropriate tool is invoked to retrieve the context
4. The LLM produces a response based on the retrieved context

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- LlamaCloud account (for RAG index)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering-hub.git
cd ai-engineering-hub/llamacloud-sql-router
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export LLAMACLOUD_API_KEY="your-llamacloud-api-key"
```

## Usage

### Preparing the Data

1. Download Wikipedia PDFs for the cities you want to include
2. Create a LlamaCloud index with these PDFs
3. Set up your SQL database with city statistics using the provided script

### Running the Application

1. Configure your LlamaCloud and database settings in `config.py`
2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. Access the UI at `http://localhost:8501`

## How it Works

### Tools Creation

We create two tools for retrieving contextual data:

![Tools Creation](media/image5.png)

1. **SQL Tool**: Translates natural language to SQL queries to retrieve city statistics
2. **LlamaCloud Tool**: Uses RAG retrieval for semantic questions about cities

### Agent Workflow

The agent's workflow wraps these tools and makes them available to the decision-making process:

![Agent Workflow](media/image6.png)

The workflow follows these steps:
1. `prepare_chat()`: Processes the user's message
2. `chat()`: Determines which tools to use
3. `dispatch_calls()`: Sends the query to selected tools
4. `call_tool()`: Executes the tools
5. `gather()`: Collects results from all tools
6. Generates a final response based on the gathered information

## Example Queries

- "Which city has the highest population?" (routes to SQL)
- "What state is Houston located in?" (routes to LlamaCloud)
- "Where is the Space Needle located?" (routes to LlamaCloud)
- "List all of the places to visit in Miami" (routes to LlamaCloud)
- "How do people in Chicago get around?" (routes to LlamaCloud)
- "What is the historical name of Los Angeles?" (routes to LlamaCloud)

## Project Structure

```
llamacloud-sql-router/
├── app.py                  # Streamlit application
├── config.py               # Configuration settings
├── router/
│   ├── __init__.py
│   ├── workflow.py         # Router agent workflow
│   └── events.py           # Event classes for the workflow
├── tools/
│   ├── __init__.py
│   ├── sql_tool.py         # SQL query tool
│   └── rag_tool.py         # RAG retrieval tool
├── data/
│   ├── db_init.py          # Database initialization
│   └── city_stats.sql      # SQL data for cities
├── notebooks/
│   └── llamacloud_sql_router.ipynb  # Jupyter notebook with examples
├── media/                  # Images for documentation
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Limitations

- LLM-based routing may occasionally choose the wrong system
- Requires proper API keys and permissions
- Wikipedia data is static and may become outdated
- The system is designed for demonstration purposes and may need optimization for production use

## Future Improvements

- Add more data sources and query engines
- Implement caching for faster responses
- Add user feedback loop to improve routing decisions
- Extend to more cities and types of information
- Implement error handling and fallback mechanisms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Acknowledgements

- [LlamaIndex](https://github.com/run-llama/llama_index) for the RAG framework
- [OpenAI](https://openai.com/) for the language models
- [Streamlit](https://streamlit.io/) for the UI framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database interactions