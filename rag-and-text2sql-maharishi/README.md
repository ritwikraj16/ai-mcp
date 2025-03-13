# LLM With Multiple Query Tools (SQL & RAG)

The project builds a LLM powered chatbot that has access to two tools to answer user question:
- SQL Tool for querying database
- RAG Tool to fetch relevant content

LLM will convert user natural language questions to appropriate SQL query or relevant input query for RAG setup to fetch data.

We use (100% local):

|Tech Stack                        |Purpose                                              |
|----------------------------------|-----------------------------------------------------|
|LlamaIndex                        |To orchestrate tool call                             |      
|Ollama                            |To serve local LLM (select any function calling LLM) |
|Qdrant                            |For Vector Database                                  |
|SQL Alchemy                       |For SQL Database                                     |
|Streamlit                         |For UI                                               |                
|CometML's Opik                    |Tracing, Observability, Evaluation                   |

A demo is shown below:
[Video Demo](rag-and-text2sql-maharishi)

---

## Installation and Setup

#### Ollama

Make sure the ollama server is running. If setting it up for the first time then install ollama and start the server using the below command and pull required model:

```python
# install ollama
curl https://ollama.ai/install.sh | sh

# start the ollama server
ollama serve &

# pull your required model
ollama pull qwen2.5:7b
```

#### Opik

We will set up Opik locally using docker. The Opik dashboard will be available on http://localhost:5173/

```python
# Clone the Opik repository
git clone https://github.com/comet-ml/opik.git

# Run the Opik platform
cd opik/deployment/docker-compose
docker compose up --detach
```

#### Qdrant

We will be running Qdrant locally in memory so no need for separate setup.

#### Run App

Set Up Virtual Environment and Install Dependencies. Ensure python 3.12 or later is installed:

```python
virtualenv -p python3.12 .venv 
source .venv/bin/activate
pip3 install -r requirements.txt
```
Now run the streamlit application:
```python
streamlit run app.py
```
---

## X Thread:

X Thread: 

---

## 📬 Stay Updated with Our Newsletter!
**Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science when you subscribe to our newsletter! Stay in the loop with the latest tutorials, insights, and exclusive resources. [Subscribe now!](https://join.dailydoseofds.com)

[![Daily Dose of Data Science Newsletter](https://github.com/patchy631/ai-engineering/blob/main/resources/join_ddods.png)](https://join.dailydoseofds.com)

---

## Contribution
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
