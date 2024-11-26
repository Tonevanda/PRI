#!/usr/bin/env python3

import sys
import argparse


def qrels_to_trec(qrels: list) -> None:
    """
    Converts qrels (query relevance judgments) to TREC evaluation format.

    Arguments:
    - qrels: A list of qrel lines (document IDs) from standard input.
    """
    for line in qrels:
        doc_id = line.strip()
        print(f"0 0 {doc_id} 1")


if __name__ == "__main__":
    """
    Read qrels from stdin and output them in TREC format.
    """

    parser = argparse.ArgumentParser(
        description="Fetch search results from Solr and output them in JSON format."
    )
    parser.add_argument(
        "--qrels",
        type=str,
        required=True,
        help="Qrels",
    )
    args = parser.parse_args()

    qrels = args.qrels.split('-')
    qrels_to_trec(qrels)
