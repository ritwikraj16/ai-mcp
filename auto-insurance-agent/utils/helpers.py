import json
import os
from ..models.schemas import ClaimInfo

def parse_claim(file_path: str) -> ClaimInfo:
    """Parse claim information from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return ClaimInfo.model_validate(data)

def parse_claim_from_json_string(json_string: str) -> ClaimInfo:
    """Parse claim information from a JSON string."""
    data = json.loads(json_string)
    return ClaimInfo.model_validate(data)

def get_declarations_docs(policy_number: str, top_k: int = 1, declarations_index=None):
    """Get declarations retriever with improved error handling and better queries for markdown files."""
    if declarations_index is None:
        return []
    
    try:
        from llama_index.core.vector_stores.types import MetadataFilters
        
        # Try different query approaches to find markdown declaration files
        all_docs = []
        
        # First try with policy number filter
        try:
            filters = MetadataFilters.from_dicts([
                {"key": "policy_number", "value": policy_number}
            ])
            retriever = declarations_index.as_retriever(
                rerank_top_n=top_k,
                filters=filters
            )
            docs = retriever.retrieve(f"declarations page for {policy_number}")
            if docs:
                all_docs.extend(docs)
        except Exception as e:
            print(f"Error with filtered retrieval: {str(e)}")
        
        # If no results, try without filters but with more specific queries
        if not all_docs:
            try:
                retriever = declarations_index.as_retriever(similarity_top_k=top_k)
                
                # Try multiple query variations to find markdown declaration files
                queries = [
                    f"declarations page for {policy_number}",
                    f"{policy_number} declarations",
                    f"{policy_number} policy declarations",
                    f"{policy_number} insurance declarations",
                    # Add queries for specific policy holders if we know them
                    "John Smith declarations" if "ABC123" in policy_number else None,
                    "Alice Johnson declarations" if "DEF456" in policy_number else None
                ]
                
                # Filter out None values
                queries = [q for q in queries if q]
                
                for query in queries:
                    try:
                        docs = retriever.retrieve(query)
                        if docs:
                            all_docs.extend(docs)
                            print(f"Found docs with query: {query}")
                            break  # Stop once we find documents
                    except Exception as query_e:
                        print(f"Error with query '{query}': {str(query_e)}")
            except Exception as e:
                print(f"Error with unfiltered retrieval: {str(e)}")
        
        # Return unique documents
        unique_docs = {}
        for doc in all_docs:
            unique_docs[doc.id_] = doc
        
        return list(unique_docs.values())
    except Exception as e:
        # Log the error but don't crash
        print(f"Error retrieving declarations: {str(e)}")
        return []

def get_local_declaration_file(policy_number: str):
    """Check for local declaration files in the data directory."""
    # Map policy numbers to potential file names
    policy_file_map = {
        "POLICY-ABC123": "data/john-declarations.md",
        "POLICY-DEF456": "data/alice-declarations.md"
    }
    
    # Check if we have a mapping for this policy number
    if policy_number in policy_file_map:
        file_path = policy_file_map[policy_number]
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading local declaration file: {str(e)}")
    
    # Also try a more general pattern search in the data directory
    try:
        data_dir = "data"
        if os.path.exists(data_dir) and os.path.isdir(data_dir):
            for filename in os.listdir(data_dir):
                if policy_number.lower() in filename.lower() and filename.endswith((".md", ".txt")):
                    file_path = os.path.join(data_dir, filename)
                    with open(file_path, "r") as f:
                        return f.read()
    except Exception as e:
        print(f"Error searching for declaration files: {str(e)}")
    
    return None

def generate_workflow_visualization():
    """Generate workflow visualization HTML."""
    from llama_index.utils.workflow import draw_all_possible_flows
    from ..workflow.workflow import AutoInsuranceWorkflow
    
    # Generate the visualization HTML
    html_file = "auto_insurance_workflow.html"
    draw_all_possible_flows(AutoInsuranceWorkflow, filename=html_file)
    
    # Read the generated HTML file
    with open(html_file, "r") as f:
        html_content = f.read()
    
    return html_content 
