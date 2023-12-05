"""
Sitemap Content Fetcher: Asynchronous Sitemap Processing and HTML Content Saving in Vector DB

This script, as part of the SynthSpider package, is designed for asynchronous fetching and
processing of website sitemaps. It retrieves sitemap data, parses it to extract URLs, fetches
HTML content of these URLs, and saves them to ChromaDB using a selected embedding function
for enhanced search and retrieval capabilities.

Functions:
    asyncio.run(): Executes the main asynchronous function.
    fetch_sitemap: Fetches the sitemap from the provided URL.
    parse_sitemap: Parses the sitemap XML to extract URLs.
    fetch_and_save_html: Fetches and saves the HTML content of each URL to ChromaDB.
    openai_ef, azure_ef, default_ef: Different embedding functions for ChromaDB content processing.

Command Line Arguments:
    sitemap_url (str): The full URL of the sitemap.xml file to be processed.
    --n (int, optional): The number of URLs to fetch from the sitemap. If not specified,
    all URLs are fetched.
    --ef (str, choices=["default", "openai", "azure"], default="default"): The embedding
    function to be used for content saving in ChromaDB.

Workflow:
    1. Parse command line arguments.
    2. Select the appropriate embedding function based on user input.
    3. Fetch the sitemap XML from the specified URL.
    4. Parse the sitemap to extract URLs.
    5. Asynchronously fetch and save the HTML content of each URL to ChromaDB.
    6. Update the progress bar for each completed task.

Example Usage:
    python sitemap_content_fetcher.py "http://example.com/sitemap.xml" --n 100 --ef "openai"
"""

import argparse
import asyncio
import logging
from tqdm import tqdm
from SynthSpider import (
    fetch_sitemap,
    parse_sitemap,
    fetch_and_save_html,
    default_ef,
    openai_ef,
    azure_ef,
    chroma_client,
)

collection_name = "sitemap_collection"

async def main(sitemap_url, n, ef):
    """
    Main function to fetch, parse the sitemap, and save HTML content to ChromaDB.
    """

    # Select the embedding function based on the user input
    if ef == "openai":
        embedding_function = openai_ef
    elif ef == "azure":
        embedding_function = azure_ef
    else:
        embedding_function = default_ef

    # Get or create the collection with the selected embedding function
    collection = chroma_client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function
    )

    # Fetch the sitemap
    sitemap_xml = await fetch_sitemap(sitemap_url)
    if not sitemap_xml:
        logging.error("Failed to fetch sitemap.")
        return
    else:
        print(f"Successfully fetched: {sitemap_url}")

    # Parse the sitemap to get URLs
    urls = parse_sitemap(sitemap_xml, n)
    if not urls:
        logging.error("No URLs found in sitemap.")
        return

    # Set up the progress bar
    pbar = tqdm(total=len(urls))

    # Function to update the progress bar
    def update_progress():
        pbar.update(1)

    # Fetch and save HTML content of each URL
    tasks = [fetch_and_save_html(url, update_progress, collection) for url in urls]
    await asyncio.gather(*tasks)

    pbar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Sitemap Content.")
    parser.add_argument("sitemap_url", type=str, help="Full URL of sitemap.xml file.")
    parser.add_argument(
        "--n", type=int, default=None, help="Number of results to return."
    )
    parser.add_argument(
        "--ef",
        type=str,
        default="default",
        choices=["default", "openai", "azure"],
        help="Embedding function to use (default or openai).",
    )
    args = parser.parse_args()

    asyncio.run(main(args.sitemap_url, args.n, args.ef))
