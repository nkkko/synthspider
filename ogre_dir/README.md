# AI Demo Project Using SDE Sandbox

## Project Overview

Welcome to our AI Demo Project designed to demonstrate the application of AI technologies for web content manipulation and article generation. This project capitalizes on Python within the SDE sandbox to showcase fetching, storing, searching web content, and generating articles using both OpenAI and Azure OpenAI services.

### Main Features:
- **Sitemap Fetching and Parsing**: Automates the fetching and parsing of sitemap XMLs to extract URLs.
- **Content Extraction and Storage**: Utilizes ChromaDB for storing web page content after retrieval.
- **AI-Powered Search**: Leverages OpenAI and Azure OpenAI embeddings for efficient content search in ChromaDB.
- **Article Generation**: Generates articles based on prompts, integrating the capabilities of OpenAI's GPT models.

## Getting Started

### Prerequisites
- Access to an SDE that supports Dev Container Specification (e.g., Daytona.io, Codeanywhere, Codespaces, or VS Code).
- Python version 3.10 or later.
- OpenAI API key for integrating OpenAI functionalities.
- Azure OpenAI credentials (optional) for users looking to utilize Azure OpenAI features (Requires `AZURE_API_VERSION`, `AZURE_ENDPOINT`, and `AZURE_OPENAI_API_KEY`).

### Installation
This project offers two setup methods:

1. **Using an SDE**:
   - Suitable for Daytona.io, Codeanywhere, Codespaces, or VS Code users, allowing instant environment configuration via `devcontainer.json`.
   - Configure an `.env` file with your `OPENAI_API_KEY` and optionally Azure OpenAI credentials.

2. **Manual Setup**:
    - Clone the Git repository.
    - Install dependencies as follows:
      ```
      pip install -r requirements.txt
      ```
      Alternatively, manually install the packages using:
      ```
      pip install openai chromadb python-dotenv bs4 argparse lxml tiktoken
      ```
    - Set up an `.env` file with your `OPENAI_API_KEY` and optionally Azure OpenAI credentials.

### Usage Instructions

1. **populate.py**: Script to fetch, parse, and store website content. Use the `--ef` flag to select the embeddings function.
   - Usage: `python populate.py [SITEMAP_URL] [--n [MAX_URLS]] [--ef {default|openai|azure}]`

2. **search.py**: Executes searches in the stored data. Select embeddings function with `--ef`.
   - Usage: `python search.py [SEARCH_QUERY] [--n [NUMBER_OF_RESULTS]] [--ef {default|openai|azure}]`

3. **write.py**: Generates articles rooted in ChromaDB search results. Select embeddings function with `--ef`.
   - Usage: `python write.py [PROMPT] --s [SEARCH_TERM] --n [NUMBER_OF_RESULTS] [--ef {default|openai|azure}]`

The `--ef` flag indicates the embeddings function choice: `default` for all-MiniLM-L6-v2, `openai` to use OpenAI's embeddings, and `azure` for Azure's variant.

## Project Structure

- `SynthSpider.py`: A central module encapsulating sitemap fetching, parsing, content retrieval, storage, searching and article generation logic.
- Script files (`populate.py`, `search.py`, `write.py`): Dedicated utilities for interacting with web content and AI APIs.
- `db/`: Houses ChromaDB client and utilities.
- `.env`: Holds environment variables like API keys.
- `.devcontainer`: Provides Dev Environment setup configuration for compatible SDEs.

## Using Azure OpenAI

To leverage Azure OpenAI services, ensure your `.env` file includes `AZURE_API_VERSION`, `AZURE_ENDPOINT`, and `AZURE_OPENAI_API_KEY`. This expands the capabilities around embeddings and article generation, offering an alternative to the standard OpenAI route.

## Examples

Fetch, search and generate content through command-line instructions, showcasing the versatility and power of the integrated APIs and database systems.

## Contributing

We encourage contributions. Enhance, suggest improvements, or extend functionalities while adhering to coding best practices and documentation standards.

## License

Distributed under the [MIT License](LICENSE.md).

## Acknowledgments

Gratitude towards OpenAI and the developers behind ChromaDB for their exceptional tools and services.

## Future Directions

Plans to include prompt handling from files and integration with Azure OpenAI's new endpoints for GPT-4 Turbo model enhancements.

---

*This README guides through setting up, understanding, and contributing to the AI Demo Project utilizing SDE as a versatile sandbox for AI projects.*