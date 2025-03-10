#  Insurance Claim Workflow by Federico Trotta





## Installation

### Requirements
To replicate this tutorial must match the following requirements:
- Python [x] or higher installed on your machine.
- A valid XXXXX API key.

### Prerequisites
Suppose you call the main folder of your project `insurance_claim/`. At the end of this step, the folder will have the following structure:
```plaintext
insurance_claim/
    ├── app.py
    ├── data/
    └── venv/
```

Where:
- `app.py` is the Python file containing all the logic.
- `data/` contains the input and output data.
- `venv/` contains the virtual environment.

You can create the venv/ virtual environment directory like so:
```plaintext
python3 -m venv venv
```
To activate it, on Windows, run:
```plaintext
venv\Scripts\activate
```

Equivalently, on macOS and Linux, execute:
```plaintext
source venv/bin/activate
```

You can now install dependencies:
```plaintext
pip install -r requirements.txt
```

Finally, the PDF file used for this tutorial can be dowloaded [here](https://nationalgeneral.com/forms_catalog/CAIP400_03012006_CA.pdf) and must be uploaded [here](https://cloud.llamaindex.ai/login) to be parsed by the LLM.