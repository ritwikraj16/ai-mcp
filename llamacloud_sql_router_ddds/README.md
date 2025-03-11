# US City Guide: Combining RAG and Text-to-SQL in a Single Query Interface

This project creates a custom agent that can query either your LlamaCloud index for RAG-based retrieval or a separate SQL query engine as a tool. 

We use:
* LlamaIndex for orchestrating the RAG app.
* Streamlit to build the UI.

A demo is shown below:
- demo.mp4

## Installation and setup

In this example, we'll use PDFs of Wikipedia pages of US cities and a SQL database of their populations and states as documents.