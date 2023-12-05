"""
This script is designed to interact with a ChromaDB database, extracting and processing data for analysis and storage.
It utilizes the `chromadb` package to access a persistent database client, retrieves a specific collection of data,
and processes the results for output.

The script performs the following key operations:
1. Connects to the ChromaDB database and accesses a collection named "sitemap_collection".
2. Retrieves data from the collection, including documents, embeddings, and metadata.
3. Processes the retrieved data to format and combine metadata with documents.
4. Outputs the embeddings data to a TSV (Tab-Separated Values) file named 'embeddings.tsv'.
5. Similarly, outputs the combined metadata to another TSV file named 'metadata.tsv'.

Modules Used:
- os: Provides a way of using operating system dependent functionality.
- json: Provides JSON encoder and decoder.
- ipdb: Provides an interactive Python debugger.
- replicate: Not explicitly used in the script, but likely for replicating data or processes.
- tqdm.auto: Provides a fast, extensible progress bar for loops and iterations.
- chromadb: Used for interacting with ChromaDB database.
- csv: Used for writing data to TSV files.

Usage:
    Run the script as a standalone Python script. Ensure that the ChromaDB database is accessible and
    the 'db/' directory exists. The script outputs 'embeddings.tsv' and 'metadata.tsv' in the current directory.
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
