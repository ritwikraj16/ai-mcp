SQL + RAG Query Engine

Twitter post typefully: https://typefully.com/t/su75XlG

Demo Video : https://youtu.be/yFpYjAKbXpU?si=lHcS_kjPZcBvmPPI
Project Overview
This project is an AI-driven Hybrid Query Engine that can process both SQL-based structured queries and unstructured document searches using LlamaIndex, Ollama (Mistral), and Qdrant.
Features
✅ Structured Data: Uses SQL to query city statistics like population & state.
✅ Unstructured Data: Retrieves answers from Wikipedia PDFs using embeddings.
✅ Smart Query Routing: Uses LLMs to decide whether to use SQL or vector search.

 Tech Stack
LlamaIndex: For vector-based document search (RAG).
Ollama (Mistral LLM): For intelligent query understanding.
Qdrant: For efficient vector storage & retrieval.
SQLAlchemy: For managing structured SQL databases.
HuggingFace Embeddings: To encode text into vector representations.

Installation Guide
1️⃣ Clone the Repository
Fork and clone the repo:
git clone https://github.com/sakshiware_25/ai-engineering-hub.git
 cd ai-engineering-hub

2️⃣ Install Dependencies
Ensure you have Python 3.8+ installed, then run:
pip install -r requirements.txt

3️⃣ Download Model & PDFs
Place your HuggingFace embeddings model at the specified path.
Add Wikipedia PDFs inside the /data/ folder.

🚀 How to Run the Code
Run the following command to start the query engine:
python llamacloud_sql_router.py


📊 Example Queries
Once running, try:
Which city has the highest population?
Where is the Space Needle located?
How do people in Chicago get around?

The system will intelligently route the query between SQL & RAG!


📩 Contact
For any questions, feel free to open an issue or reach out! 🚀
