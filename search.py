"""
ChromaDB Searcher: Search and Retrieve Documents from ChromaDB

This script, a part of the SynthSpider package, is designed to facilitate searching in ChromaDB using a user-defined query. It allows users to specify the number of results to return and the embedding function to use for the search, enhancing the relevance and accuracy of the results.

Functions:
    argparse.ArgumentParser: Parses command line arguments.
    search_in_chromadb: Performs a search in ChromaDB based on the given query, number of results, and collection.
    openai_ef, azure_ef, default_ef: Different embedding functions available for ChromaDB search.

Command Line Arguments:
    query (str): The search query for ChromaDB.
    --n (int, default=5): The number of results to return from the search.
    --ef (str, choices=["default", "openai", "azure"], default="default"): The embedding function to use for the search.

Workflow:
    1. Parse command line arguments for the search query, number of results, and embedding function.
    2. Select the appropriate embedding function based on user input.
    3. Initialize a collection in ChromaDB with the selected embedding function.
    4. Perform a search in ChromaDB using the provided query and collection.
    5. Print the URLs and content of each retrieved document.

Example Usage:
    python chromadb_searcher.py "Your search query" --n 10 --ef "openai"
"""

import argparse
from SynthSpider import (
    search_in_chromadb,
    default_ef,
    openai_ef,
    azure_ef,
    chroma_client,
    collection_name,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search in ChromaDB.")
    parser.add_argument("query", type=str, help="Search query.")
    parser.add_argument("--n", type=int, default=5, help="Number of results to return.")
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

    # Perform the search
    results = search_in_chromadb(args.query, args.n, collection)

# Print the results
for i in range(
    len(results["documents"])
):  # Iterate over each set of documents (outer list)
    for j in range(
        len(results["documents"][i])
    ):  # Iterate over documents in each set (inner list)
        print(f"URL: {results['metadatas'][i][j]['url']}")
        print(f"Content: {results['documents'][i][j]}")  # Print the document
        print("-" * 50)
