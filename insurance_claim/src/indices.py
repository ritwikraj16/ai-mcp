import os
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.vector_stores.types import MetadataFilters

# Index for general auto insurance policies
index = LlamaCloudIndex(
    name="auto_insurance_policies_0",
    project_name="Daily_Dose_of_DS",
    organization_id=os.environ["LLAMA_ORG_ID"],
    api_key=os.environ["LLAMA_API_KEY"]
)
retriever = index.as_retriever(rerank_top_n=3)

# Index for declarations pages
declarations_index = LlamaCloudIndex(
    name="auto_insurance_declarations_0",
    project_name="Daily_Dose_of_DS",
    organization_id=os.environ["LLAMA_ORG_ID"],
    api_key=os.environ["LLAMA_API_KEY"]
)

def get_declarations_docs(policy_number: str, top_k: int = 1):
    """
    Retrieve declarations docs for the given policy using metadata filtering.
    """
    filters = MetadataFilters.from_dicts([
        {"key": "policy_number", "value": policy_number}
    ])
    retriever = declarations_index.as_retriever(
        retrieval_mode="files_via_metadata",
        rerank_top_n=top_k,
        filters=filters
    )
    return retriever.retrieve(f"declarations page for {policy_number}")