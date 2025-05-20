"""
Codegen Python SDK Demo
=======================

This file demonstrates how to use the Codegen Python SDK to interact with the Codegen API.
Codegen is an AI-powered coding assistant that helps developers write, review, and understand code.

Prerequisites:
- Python 3.8+
- Codegen API key

Installation:
```bash
pip install codegen-sdk
```
"""

import os
from typing import Dict, List, Optional, Union
import requests


class CodegenClient:
    """
    A client for interacting with the Codegen API.
    
    This client provides methods to:
    - Generate code based on natural language descriptions
    - Review existing code for improvements
    - Explain complex code snippets
    - Refactor code for better readability and performance
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Codegen client.
        
        Args:
            api_key: Your Codegen API key. If not provided, will look for CODEGEN_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("CODEGEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or through the CODEGEN_API_KEY environment variable."
            )
        
        self.base_url = "https://api.codegen.sh/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_code(self, prompt: str, language: str = "python", max_tokens: int = 1000) -> Dict:
        """
        Generate code based on a natural language description.
        
        Args:
            prompt: A description of what the code should do
            language: The programming language to generate code in
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dict containing the generated code and metadata
        """
        endpoint = f"{self.base_url}/generate"
        payload = {
            "prompt": prompt,
            "language": language,
            "max_tokens": max_tokens
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def review_code(self, code: str, language: str = None) -> Dict:
        """
        Review code for potential improvements, bugs, and best practices.
        
        Args:
            code: The code to review
            language: The programming language of the code (optional, will be auto-detected if not provided)
            
        Returns:
            Dict containing review comments and suggestions
        """
        endpoint = f"{self.base_url}/review"
        payload = {
            "code": code,
            "language": language
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def explain_code(self, code: str, detail_level: str = "medium") -> Dict:
        """
        Get an explanation of what the provided code does.
        
        Args:
            code: The code to explain
            detail_level: Level of detail in the explanation ("low", "medium", "high")
            
        Returns:
            Dict containing the explanation
        """
        endpoint = f"{self.base_url}/explain"
        payload = {
            "code": code,
            "detail_level": detail_level
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def refactor_code(self, code: str, goals: List[str] = None) -> Dict:
        """
        Refactor code to improve readability, performance, or other aspects.
        
        Args:
            code: The code to refactor
            goals: Specific refactoring goals (e.g., ["improve_readability", "optimize_performance"])
            
        Returns:
            Dict containing the refactored code
        """
        endpoint = f"{self.base_url}/refactor"
        payload = {
            "code": code,
            "goals": goals or ["improve_readability"]
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize the client (replace with your actual API key or set environment variable)
    client = CodegenClient(api_key="your_api_key_here")
    
    # Generate code example
    result = client.generate_code(
        prompt="Create a function that calculates the Fibonacci sequence up to n terms",
        language="python"
    )
    print("Generated Code:")
    print(result["code"])
    print("\n" + "-" * 50 + "\n")
    
    # Code to review
    sample_code = """
    def sort_list(items):
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if items[j] > items[j + 1]:
                    items[j], items[j + 1] = items[j + 1], items[j]
        return items
    """
    
    # Review code example
    review_result = client.review_code(sample_code)
    print("Code Review:")
    for comment in review_result["comments"]:
        print(f"- {comment['message']}")

