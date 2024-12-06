#!/usr/bin/env python3

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np


def main(qrels_file: str, output_file: str):
    """
    Read predicted document IDs from stdin in TREC format and qrels (ground truth IDs) from a file,
    Plot precision-recall curve and save it to a .PNG file.

    Arguments:
        qrels_file -- Path to the qrels file containing ground truth document IDs in TREC format.
        output_file -- Name of the output PNG file where the precision-recall curve will be saved.
    """

    # Read qrels (ground truth) from the specified file in TREC format
    with open(qrels_file, "r") as f:
        y_true = {
            line.strip().split()[2] for line in f
        }  # Use a set for fast lookup of relevant document IDs

    # Read predicted document IDs from stdin (TREC format: assume the third column contains the doc_id)
    y_pred = [
        line.strip().split()[2] for line in sys.stdin
    ]  # Extract document IDs from TREC format

    # Edge case: Handle empty inputs
    if not y_pred or not y_true:
        print("Error: No predictions or qrels found. Please provide valid input.")
        sys.exit(1)

    # Calculate precision, recall, and keep track of relevant ranks for MAP calculation
    precision = []
    recall = []
    relevant_ranks = []  # To hold precision values at ranks where relevant documents are retrieved
    relevant_count = 0

    for i in range(1, len(y_pred) + 1):
        # Check how many predicted documents so far are relevant
        if y_pred[i - 1] in y_true:
            relevant_count += 1
            relevant_ranks.append(relevant_count / i)  # Precision at this rank (relevant document)

        # Precision: relevant docs so far / total docs retrieved so far
        precision.append(relevant_count / i)

        # Recall: relevant docs so far / total relevant docs in qrels
        recall.append(relevant_count / len(y_true))

    # Compute Mean Average Precision (MAP) as the mean of precision values for relevant documents
    map_score = np.sum(relevant_ranks) / len(y_true) if relevant_ranks else 0

    # Compute the 11-point interpolated precision-recall curve
    recall_levels = np.linspace(0.0, 1.0, 11)
    interpolated_precision = [
        max([p for p, r in zip(precision, recall) if r >= r_level], default=0)
        for r_level in recall_levels
    ]

    # Compute the Area Under Curve (AUC) for the precision-recall curve
    auc_score = np.trapz(interpolated_precision, recall_levels)

    # Plot the 11-point interpolated precision-recall curve
    plt.plot(
        recall_levels,
        interpolated_precision,
        drawstyle="steps-post",
        label=f"MAP: {map_score:.4f}, AUC: {auc_score:.4f}",
        linewidth=1,
    )

    # Customize plot appearance
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})

    # Keep the title as "Precision-Recall Curve"
    plt.title("Precision-Recall Curve")

    # Save the plot to the specified output PNG file
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Precision-Recall plot saved to {output_file}")


if __name__ == "__main__":
    # Argument parser to handle the qrels file and output file as command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate a Precision-Recall curve from Solr results (in TREC format) and qrels."
    )
    parser.add_argument(
        "--qrels",
        type=str,
        required=True,
        help="Path to the qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument("--output", type=str, required=True, help="Path to the output PNG file")
    args = parser.parse_args()

    # Run the main function with the provided qrels file and output file
    main(args.qrels, args.output)
