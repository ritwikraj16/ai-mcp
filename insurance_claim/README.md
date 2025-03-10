#  Insurance Claim Workflow by Federico Trotta





## Installation

### Requirements
To replicate this tutorial must match the following requirements:
- Python [x] or higher installed on your machine.
- A valid llamaindex API key that can be retrieved [here](https://cloud.llamaindex.ai/).
- A valid OpenAI API key that can be retrieved [here](https://platform.openai.com/api-keys).

Credentials can be set into a `.env` file like so:
```plaintext
OPENAI_API_KEY = ""
LLAMA_ORG_ID = ""
LLAMA_CLOUD_API_KEY= ""
```

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
- `data/` contains files to insert into [cloudllama](#project-set-up-cloudllama).
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

### Project set up: cloudllama
In cloudllama, do the following:
- When you logged in into cloud.llama, the `LLAMA_ORG_ID` can be found in **Settings** > **Organization** > **Organization ID**. In othwe words, set `LLAMA_ORG_ID = <the value of Organization ID>`.
- Still in **Settings**, give a name to **Project Name** under the **Projects** table. This must be the same value as the variable `project_name`of the `LlamaCloudIndex()` method.
- The project assumes the possiblity of parsing a PDF file that can be downloaded from [here](https://nationalgeneral.com/forms_catalog/CAIP400_03012006_CA.pdf). However, you can skip this passage and copy and paste the `.json` and `.md` files you find in the `data/` folder as new indexes in cloudllama. To do so, in the section **Index** click on **Create index** and drag and drop the two `.md` files and name the index as `auto_insurance_declarations_0`. To the same for the two `.json` files and name the index as `auto_insurance_policies_0`.

## Run the application
To run the application, type:
```plaintext
streamlit run app.py
```