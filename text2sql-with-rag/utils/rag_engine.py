import os
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.tools import QueryEngineTool

# RAG Ingine after creating the index of the documents uploaded to Llama Cloud
def retrieve_rag_tool():
    index = LlamaCloudIndex(
        name="text2sql-with-rag", 
        project_name="Default",
        organization_id=os.getenv("LLAMA_CLOUD_ORG_ID"),
        api_key=os.getenv("LLAMA_CLOUD_API_KEY")
    )


    llama_cloud_query_engine = index.as_query_engine()

    llama_cloud_tool = QueryEngineTool.from_defaults(
    query_engine=llama_cloud_query_engine,
    description=(
        f"Useful for answering semantic questions about certain cities in the US."
    ),
    name="llama_cloud_tool"
    )

    return llama_cloud_tool