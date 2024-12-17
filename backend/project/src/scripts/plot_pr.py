#!/usr/bin/env python3

import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

def read_qrels(file_path):
    with open(file_path, "r") as f:
        return {line.strip().split()[2] for line in f}

def read_predictions(file_path):
    with open(file_path, "r") as f:
        return [line.strip().split()[2] for line in f]

def calculate_precision_recall(y_true, y_pred):
    precision = []
    recall = []
    relevant_ranks = []
    relevant_count = 0

    for i in range(1, len(y_pred) + 1):
        if y_pred[i - 1] in y_true:
            relevant_count += 1
            relevant_ranks.append(relevant_count / i)

        precision.append(relevant_count / i)
        recall.append(relevant_count / len(y_true))

    map_score = np.sum(relevant_ranks) / len(y_true) if relevant_ranks else 0
    recall_levels = np.linspace(0.0, 1.0, 11)
    interpolated_precision = [
        max([p for p, r in zip(precision, recall) if r >= r_level], default=0)
        for r_level in recall_levels
    ]
    auc_score = np.trapz(interpolated_precision, recall_levels)

    return precision, recall, map_score, auc_score, recall_levels, interpolated_precision

def plot_curve(name, map, auc, interpolated_precision):
    plt.plot(
        np.linspace(0.0, 1.0, 11),
        interpolated_precision,
        drawstyle="steps-post",
        label=f"{name} AvP: {map:.4f}, AUC: {auc:.4f}",
        linewidth=1,
    )

def plot_pr_curve(qrels_file, output_file):
    y_true = read_qrels(qrels_file)
    y_pred = read_predictions(qrels_file.replace("qrels", "results"))
    precision, recall, map_score, auc_score, recall_levels, interpolated_precision = calculate_precision_recall(y_true, y_pred)
    if qrels_file.endswith("sh_childhood.txt"):
        plot_curve("Normal", 0.3880952380952381, 0.44000000000000006, [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0, 0, 0, 0, 0])

    if qrels_file.endswith("luffy_fight.txt"):
        plot_curve("Normal", 0.7000000000000001, 0.685, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.1, 0.1, 0.1, 0.1])

    if qrels_file.endswith("bounty.txt"): 
        plot_curve("Normal", 0.6432339265672599, 0.6366666666666667, [1.0, 1.0, 1.0, 1.0, 0.5833333333333334, 0.5833333333333334, 0.5833333333333334, 0.5833333333333334, 0.5333333333333333, 0, 0])

    if qrels_file.endswith("ancient_weapon.txt"):
        plot_curve("Normal", 0.5119047619047619, 0.5357142857142857, [1.0, 1.0, 0.5714285714285714, 0.5714285714285714, 0.5714285714285714, 0.5714285714285714, 0.5714285714285714, 0.5, 0.5, 0, 0])

    plt.plot(
        recall_levels,
        interpolated_precision,
        drawstyle="steps-post",
        label=f"Grid Search AvP: {map_score:.4f}, AUC: {auc_score:.4f}",
        linewidth=1,
    )

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})
    plt.title("Precision-Recall Curve")
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Precision-Recall plot saved to {output_file}")

def plot_pr_curve_all(qrels_file, def_qrels_file, m2_qrels_file, emb_qrels_file, output_file):
    y_true = read_qrels(qrels_file)
    def_y_true = read_qrels(def_qrels_file)
    m2_y_true = read_qrels(m2_qrels_file)
    emb_y_true = read_qrels(emb_qrels_file)

    y_pred = read_predictions(qrels_file.replace("qrels", "results"))
    def_y_pred = read_predictions(def_qrels_file.replace("qrels", "results"))
    m2_y_pred = read_predictions(m2_qrels_file.replace("qrels", "results"))
    emb_y_pred = read_predictions(emb_qrels_file.replace("qrels", "results"))

    precision, recall, map_score, auc_score, recall_levels, interpolated_precision = calculate_precision_recall(y_true, y_pred)
    def_precision, def_recall, def_map_score, def_auc_score, def_recall_levels, def_interpolated_precision = calculate_precision_recall(def_y_true, def_y_pred)
    m2_precision, m2_recall, m2_map_score, m2_auc_score, m2_recall_levels, m2_interpolated_precision = calculate_precision_recall(m2_y_true, m2_y_pred)
    emb_precision, emb_recall, emb_map_score, emb_auc_score, emb_recall_levels, emb_interpolated_precision = calculate_precision_recall(emb_y_true, emb_y_pred)


    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})
    plt.title("Precision-Recall Curve")
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Precision-Recall plot saved to {output_file}")

    plt.plot(
        recall_levels,
        interpolated_precision,
        drawstyle="steps-post",
        label=f"Normal AvP: {map_score:.4f}, AUC: {auc_score:.4f}",
        linewidth=1,
    )
    plt.plot(
        m2_recall_levels,
        m2_interpolated_precision,
        drawstyle="steps-post",
        label=f"M2 AvP: {m2_map_score:.4f}, AUC: {m2_auc_score:.4f}",
        linewidth=1,
    )
    plt.plot(
        def_recall_levels,
        def_interpolated_precision,
        drawstyle="steps-post",
        label=f"Def AvP: {def_map_score:.4f}, AUC: {def_auc_score:.4f}",
        linewidth=1,
    )
    plt.plot(
        emb_recall_levels,
        emb_interpolated_precision,
        drawstyle="steps-post",
        label=f"Emb AvP: {emb_map_score:.4f}, AUC: {emb_auc_score:.4f}",
        linewidth=1,
    )
    

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})
    plt.title("Precision-Recall Curve")
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Precision-Recall plot saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Precision-Recall curve from Solr results (in TREC format) and qrels."
    )
    parser.add_argument(
        "--qrels",
        type=str,
        required=True,
        help="Path to the qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument(
        "--def_qrels",
        type=str,
        required=True,
        help="Path to the def qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument(
        "--m2_qrels",
        type=str,
        required=True,
        help="Path to the m2 qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument(
        "--emb_qrels",
        type=str,
        required=True,
        help="Path to the emb qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument("--output", type=str, required=True, help="Path to the output PNG file")
    args = parser.parse_args()

    if(args.def_qrels == "None"):
        plot_pr_curve(args.qrels, args.output)
    else:
        plot_pr_curve_all(args.qrels, args.def_qrels, args.m2_qrels, args.emb_qrels, args.output)