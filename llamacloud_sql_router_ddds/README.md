# US City Guide 🏙️: Combining RAG and Text-to-SQL in a Single Query Interface

This project creates a custom agent that can query either your LlamaCloud index for RAG-based retrieval or a separate SQL query engine as a tool. 

We use:
* LlamaIndex for orchestrating the RAG app.
* SQL to create a database and store city populations.
* Streamlit to build the UI.

A demo is shown below:
[Demo](https://github.com/hadenpell/ai-engineering-hub/blob/dailydoseds/llamacloud_sql_router_ddds/demo.mp4) 

## Installation and setup

#### Setup OpenAI
Get an API key from OpenAI and set it in the .env file as follows:
```
OPENAI_API_KEY = YOUR_OPENAI_API_KEY
```

#### Setup LlamaCloud 
Get an API key from LlamaCloud and set it in the .env file as follows:
```
LLAMA_API_KEY = YOUR_LLAMA_API_KEY
```

<b>Install Dependencies</b>: Ensure you have Python 3.10 or later installed.

```
pip install -r requirements.txt
```
 
<b>Run the app:</b>

Run the app by running the following command:
```
streamlit run app.py
```

## Stay Updated with Our Newsletter!