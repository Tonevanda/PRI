import subprocess
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

def plot_pr_curve():
    queries = [
        "sh_childhood",
        "luffy_fight",
        "bounty",
        "ancient_weapon"
    ]
    commands = [
        "rm -rf diagrams",
        "mkdir diagrams",
    ]
    for command in commands:
        subprocess.run(command, shell=True, check=True)

    for query in queries:
        command = (
            f"python plot_pr.py --qrels ./qrels/{query}.txt --def_qrels None --m2_qrels None --emb_qrels None --output ./diagrams/{query}.png"
        )
        subprocess.run(command, shell=True, check=True)

def evaluate_results(metric):
    queries = [
        "sh_childhood",
        "luffy_fight",
        "bounty",
        "ancient_weapon"
    ]
    query_metric = 0
    for query in queries:
        qrels_file = f"./qrels/{query}.txt"
        y_true = read_qrels(qrels_file)
        y_pred = read_predictions(qrels_file.replace("qrels", "results"))
        precision, recall, map_score, auc_score, recall_levels, interpolated_precision = calculate_precision_recall(y_true, y_pred)
        if metric == "MAP":
            query_metric += map_score

    return query_metric / len(queries)
    




# Define the shell commands
commands = [
    "rm -rf results",
    "rm -rf qrels",
    "mkdir results",
    "mkdir qrels"
]

# Execute each command


topks = [520, 450]
scores = ["avg", "max", "total"]
reRankDocs = [30, 40]
reRankWeights = [75, 95]
metric = "MAP"


best_result = 0
while(True):
    for topk in topks:
        for score in scores:
            for reRankDoc in reRankDocs:
                for reRankWeight in reRankWeights:
                    for command in commands:
                        subprocess.run(command, shell=True, check=True)
                        

                    query_command = f"python pipeline.py --query ./grid_search.json --topk {topk} --score {score} --reRankDocs {reRankDoc} --reRankWeight {reRankWeight} --gridSearch True"
                    subprocess.run(query_command, shell=True, check=True)
                    result = evaluate_results(metric)
                    if result > best_result:
                        best_result = result
                        plot_pr_curve()
                        print("The best " + metric + " is: " + str(best_result) + " with params: \n")
                        print("   -topk: " + str(topk) + ";")
                        print("   -scores: " + score + ";")
                        print("   -reRankDocs: " + str(reRankDoc) + ";")
                        print("   -reRankWeights: " +str(reRankWeight) + ";")








