# KitOps MCP Server

We are going to implement an MCP server to orchestrate KitOps for managing and distributing machine learning models. Agents will be able to connect to discover tools for creating, inspecting, pushing, pulling, and removing ModelKits from remote registries like Jozu Hub.

We use:

- [KitOps](https://kitops.org/) for versioning, packaging, and distributing ML models
- Cursor (MCP Host)

## Set Up

Follow these steps one by one:

### Install Kit CLI

Here is the documentation for downloading and installing the Kit CLI: [Kit CLI Installation](https://kitops.org/docs/cli/installation/) for your operating system.

After installing the Kit CLI, you can verify the installation by running:

```bash
kit version
```

### Create .env File

Create a `.env` file in the root directory of your project with the following content:

```env
JOZU_USERNAME=<your_jozu_hub_email>
JOZU_PASSWORD=<your_jozu_hub_account_password>
JOZU_NAMESPACE=<name_of_repository_in_jozu_hub>
```

All the values are associated with your Jozu Hub account. If you don't have a Jozu account, you can create one at [Jozu Hub](https://jozu.ml/).

### Install Dependencies

```bash
uv sync
```

## Use MCP Server

Run the MCP server with the created configuration file as `mcp.json` either globally or in the current project directory. Here's the code of configuring MCP globally to run the server:

```json
{
  "mcpServers": {
    "kitops_mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/akshay/Eigen/ai-engineering-hub/kitops-mcp",
        "run",
        "--with",
        "mcp",
        "server.py"
      ]
    }
  }
}
```

## 📬 Stay Updated with Our Newsletter!

**Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science when you subscribe to our newsletter! Stay in the loop with the latest tutorials, insights, and exclusive resources. [Subscribe now!](https://join.dailydoseofds.com)

[![Daily Dose of Data Science Newsletter](https://github.com/patchy631/ai-engineering/blob/main/resources/join_ddods.png)](https://join.dailydoseofds.com)

## Contribution

Contributions are welcome! Feel free to fork this repository and submit pull requests with your improvements.
