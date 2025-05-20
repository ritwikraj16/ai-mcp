# Codegen SDK Demo 🤖

This project demonstrates how to use the Codegen Python SDK to interact with the Codegen API for AI-assisted code generation, review, and refactoring.

## What is Codegen?

Codegen is an AI-powered coding assistant that helps developers:

- Generate code from natural language descriptions
- Review existing code for improvements and best practices
- Explain complex code snippets in plain language
- Refactor code for better readability and performance

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Codegen API key (sign up at [codegen.sh](https://codegen.sh))

### Installation

```bash
pip install codegen-sdk
```

### Setting Up Your API Key

You can provide your API key in two ways:

1. As an environment variable:
   ```bash
   export CODEGEN_API_KEY="your_api_key_here"
   ```

2. Directly in your code:
   ```python
   from codegen_sdk import CodegenClient
   
   client = CodegenClient(api_key="your_api_key_here")
   ```

## Usage Examples

### Generating Code

```python
from codegen_sdk import CodegenClient

client = CodegenClient()

# Generate a function to calculate the factorial of a number
result = client.generate_code(
    prompt="Write a function to calculate the factorial of a number",
    language="python"
)

print(result["code"])
```

### Reviewing Code

```python
code_to_review = """
def process_data(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result
"""

review_result = client.review_code(code_to_review)

for comment in review_result["comments"]:
    print(f"{comment['type']}: {comment['message']}")
```

### Explaining Code

```python
complex_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

explanation = client.explain_code(complex_code, detail_level="high")
print(explanation["explanation"])
```

### Refactoring Code

```python
code_to_refactor = """
def f(x, y):
    z = x + y
    if z > 10:
        print("z is greater than 10")
    else:
        print("z is not greater than 10")
    return z
"""

refactored = client.refactor_code(
    code_to_refactor, 
    goals=["improve_readability", "use_better_naming"]
)

print(refactored["code"])
```

## API Reference

The Codegen SDK provides the following main methods:

| Method | Description |
|--------|-------------|
| `generate_code(prompt, language, max_tokens)` | Generate code based on a natural language description |
| `review_code(code, language)` | Review code for improvements and best practices |
| `explain_code(code, detail_level)` | Get an explanation of what the code does |
| `refactor_code(code, goals)` | Refactor code according to specified goals |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

