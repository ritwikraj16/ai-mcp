import json
from .models import ClaimInfo

def parse_claim_from_text(json_text: str) -> ClaimInfo:
    """
    Utility to parse claim text (in JSON format) into a ClaimInfo object.
    """
    data = json.loads(json_text)
    return ClaimInfo(**data)


def load_prompt(file_path: str) -> str:
    """
    Utility function to load a prompt from a markdown file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()