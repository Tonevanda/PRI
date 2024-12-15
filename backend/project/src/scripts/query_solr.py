#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path


import requests

from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str


def fetch_solr_results(query, collection, params, solr_uri, useRqq):
    """
    Fetch search results from a Solr instance based on the query parameters.

    Arguments:
    - query_file: Path to the JSON file containing Solr query parameters.
    - solr_uri: URI of the Solr instance (e.g., http://localhost:8983/solr).
    - collection: Solr collection name from which results will be fetched.
    - useRqq: If we're meant to use the RQQ parameter.

    Output:
    - Prints the JSON search results to STDOUT.
    """

    # Construct the Solr request URL
    uri = f"{solr_uri}/{collection}/select"

    if(useRqq=="True"):
        embedding = text_to_embedding(query)
        rqq = '{!parent which=\"*:* -_nest_path_:*\" score=max}{!knn f=vector topK=100}' + str(embedding)
    else:
        rqq = None

    try:
        # Send the POST request to Solr

        if rqq is None:
            print("\n   rqq is empty\n")
            solr_params = {
                "q": query,
                "fl": "id, Episode, score",
                "useParams": params
            }
        else:
            print("\n   rqq is not empty\n")
            solr_params = {
                "q": query,
                "fl": "id, Episode, score",
                "useParams": params,
                "rqq": rqq
            }

        response = requests.post(uri, data=solr_params, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()  # Raise error if the request failed
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    # Fetch and print the results as JSON
    results = response.json()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    # Set up argument parsing for the command-line interface
    parser = argparse.ArgumentParser(
        description="Fetch search results from Solr and output them in JSON format."
    )

    # Add arguments for query file, Solr URI, and collection name
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Query",
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Collection",
    )
    parser.add_argument(
        "--useParams",
        type=str,
        required=True,
        help="Params",
    )
    parser.add_argument(
        "--uri",
        type=str,
        default="http://localhost:8983/solr",
        help="The URI of the Solr instance (default: http://localhost:8983/solr).",
    )
    parser.add_argument(
        "--useRqq",
        type=str,
        required=True,
        default="False",
        help="If we're meant to use the RQQ parameter.",
    )
    # Parse command-line arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    fetch_solr_results(args.query, args.collection, args.useParams, args.uri, args.useRqq)
