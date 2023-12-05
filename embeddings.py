"""
This script is designed for extracting and saving data from a database using the chromadb library. It retrieves
documents, embeddings, and metadata from a specified collection within a PersistentClient database, and then
writes this data to two separate files: 'embeddings.tsv' and 'metadata.tsv'.

Key Steps:
1. Initializes a PersistentClient from chromadb, pointing to a database located at 'db/'.
2. Retrieves or creates a collection named 'sitemap_collection'.
3. Fetches documents, embeddings, and metadata from the collection.
4. Processes and combines the fetched data into a structured format.
5. Writes the embeddings data to 'embeddings.tsv'.
6. Writes the combined metadata to 'metadata.tsv'.

Output Files:
- 'embeddings.tsv': Contains the embeddings data, with each embedding represented as a row of tab-separated values.
- 'metadata.tsv': Contains metadata for each document, with each row representing a document and its metadata,
  formatted as tab-separated values.

Requirements:
- chromadb: A Python library for interacting with Chrome Database.
- tqdm: Provides a progress bar for the processing.

Usage:
- Run the script in an environment where 'chromadb' and 'tqdm' libraries are installed.
- Ensure the database path 'db/' is correctly set up with the required collection and data.

Example:
    `python script_name.py` (Replace 'script_name.py' with the actual script name)

Note:
- The script assumes the presence of certain fields ('documents', 'embeddings', 'metadatas') in the database collection.
- The script will overwrite 'embeddings.tsv' and 'metadata.tsv' if they exist in the current directory.
"""

from tqdm.auto import tqdm
import chromadb
import csv


client = chromadb.PersistentClient(path="db/")

collection = client.get_or_create_collection(name=f"sitemap_collection")


results = collection.get(include=["documents", "embeddings", "metadatas"])

metadatas = [
    {"id": id, "document": doc, **meta}
    for id, doc, meta in zip(results["ids"], results["documents"], results["metadatas"])
]

with open("./embeddings.tsv", "w", encoding="utf-8") as f:
    for embedding in results["embeddings"]:
        f.write("\t".join(map(str, embedding)) + "\n")

# Extracting keys from the first item of combined_metadata as headers
headers = metadatas[0].keys()

with open("./metadata.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t")
    writer.writeheader()
    for data in metadatas:
        writer.writerow(data)
