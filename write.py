"""
SynthSpider: Article Generation Using OpenAI and ChromaDB

This script, part of the SynthSpider package, leverages the power of OpenAI's language models
and ChromaDB's database search capabilities to generate articles based on a user-provided prompt.
It uses an embedding function to enhance search results from ChromaDB, which are then combined
with the initial prompt to create a comprehensive article.

Functions:
    argparse.ArgumentParser: Parses command line arguments.
    search_in_chromadb: Searches in ChromaDB using the given search term and number of results.
    write_article: Generates an article based on the combined prompt and search results.
    openai_ef, azure_ef, default_ef: Different embedding functions used for processing search results.

Command Line Arguments:
    prompt (str): The initial prompt for the article.
    --s (str): The search term to be used for querying ChromaDB. This argument is required.
    --n (int, default=5): The number of search results to retrieve from ChromaDB.
    --ef (str, choices=["default", "openai", "azure"], default="default"): The embedding function
    to be used for processing ChromaDB search results.

Workflow:
    1. Parse command line arguments.
    2. Select the appropriate embedding function.
    3. Initialize a collection in ChromaDB with the selected embedding function.
    4. Perform a search in ChromaDB using the provided search term and number of results.
    5. Append the search results to the initial prompt to create a combined context.
    6. Generate and print the article based on the combined prompt.

Example Usage:
    python synthspider.py "Your article prompt here" --s "Search Term" --n 10 --ef "openai"
"""

import argparse
from SynthSpider import (
    search_in_chromadb,
    write_article,
    default_ef,
    openai_ef,
    azure_ef,
    chroma_client,
    collection_name,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an article using OpenAI and ChromaDB."
    )
    parser.add_argument("prompt", type=str, help="Article prompt.")
    parser.add_argument(
        "--s", type=str, required=True, help="Search term for ChromaDB."
    )
    parser.add_argument(
        "--n", type=int, default=5, help="Number of ChromaDB search results."
    )
    parser.add_argument(
        "--ef",
        type=str,
        default="default",
        choices=["default", "openai", "azure"],
        help="Embedding function to use (default or openai).",
    )

    args = parser.parse_args()

    # Select the embedding function based on the user input
    if args.ef == "openai":
        embedding_function = openai_ef
    elif args.ef == "azure":
        embedding_function = azure_ef
    else:
        embedding_function = default_ef

    # Initialize the collection with the selected embedding function
    collection = chroma_client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function
    )

    # Search in ChromaDB
    search_results = search_in_chromadb(args.s, args.n, collection)

    # Process and append search results to the prompt
    additional_context = ""
    for i in range(
        len(search_results["documents"])
    ):  # Iterate over each set of documents (outer list)
        for j in range(
            len(search_results["documents"][i])
        ):  # Iterate over documents in each set (inner list)
            additional_context += f"{search_results['documents'][i][j]}\n\n"

    combined_prompt = args.prompt + "\n\n" + additional_context

    # Generate the article
    article = write_article(combined_prompt)
    print(article)
