import os
from dotenv import load_dotenv
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.vector_stores.types import MetadataFilters
from llama_index.llms.openai import OpenAI


# Load environment variables from the .env file
load_dotenv()

# Configure the auto insurance policies index
AUTO_INSURANCE_POLICIES_INDEX = LlamaCloudIndex(
    name="auto_insurance_policies_0",
    project_name="Daily_Dose_of_DS",
    organization_id=os.environ["LLAMA_ORG_ID"],
    api_key=os.environ["LLAMA_API_KEY"]
)
policy_retriever = AUTO_INSURANCE_POLICIES_INDEX.as_retriever(rerank_top_n=3)

# Configure the declarations index
DECLARATIONS_INDEX = LlamaCloudIndex(
    name="auto_insurance_declarations_0",
    project_name="Daily_Dose_of_DS",
    organization_id=os.environ["LLAMA_ORG_ID"],
    api_key=os.environ["LLAMA_API_KEY"]
)

def get_declarations_docs(policy_number: str, top_k: int = 1):
    """
    Retrieve declarations documents for the given policy number using metadata filtering.
    """
    filters = MetadataFilters.from_dicts([
        {"key": "policy_number", "value": policy_number}
    ])
    declarations_retriever = DECLARATIONS_INDEX.as_retriever(
        retrieval_mode="files_via_metadata",
        rerank_top_n=top_k,
        filters=filters
    )
    return declarations_retriever.retrieve(f"declarations page for {policy_number}")

# Instantiate the OpenAI LLM
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)