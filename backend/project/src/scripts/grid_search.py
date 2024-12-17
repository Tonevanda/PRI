import subprocess
import numpy as np
import matplotlib.pyplot as plt


def read_qrels(file_path):
    with open(file_path, "r") as f:
        return {line.strip().split()[2] for line in f}

def read_predictions(file_path):
    with open(file_path, "r") as f:
        return [line.strip().split()[2] for line in f]
    
def pk(y_true, y_pred, k):
    positive = 0
    for i in range(1, k+1):
        if y_pred[i - 1] in y_true:
            positive += 1
    return positive/k


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


    while len(y_pred) < 30:
        y_pred.append(0)

    pks = []
    for k in range(3, len(y_pred)+1, 3):
        pks.append(round(pk(y_true, y_pred, k), 2))



    return precision, recall, map_score, auc_score, recall_levels, interpolated_precision, pks

def plot_pr_curve(queries):
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

def evaluate_results(queries, metric):

    query_metric = 0
    query_metric1 = 0
    query_metric2 = 0
    pks_store = []
    for query in queries:
        qrels_file = f"./qrels/{query}.txt"
        y_true = read_qrels(qrels_file)
        y_pred = read_predictions(qrels_file.replace("qrels", "results"))
        precision, recall, map_score, auc_score, recall_levels, interpolated_precision, pks = calculate_precision_recall(y_true, y_pred)
        if metric == "MAP":
            query_metric1 += map_score
        elif metric == "AUC":
            query_metric2 += auc_score
        elif metric == "MAP_AND_AUC":
            query_metric1 += map_score
            query_metric2 += auc_score
            query_metric += (map_score + auc_score) / 2
        pks_store.append(pks)

    pk_averages = []
    for i in range(0, len(pks_store[0])):
        pk_values = 0
        for pk_store in pks_store:
            pk_values += pk_store[i]
        pk_averages.append(pk_values/len(pks_store))


    return query_metric / len(queries), query_metric1 / len(queries), query_metric2 / len(queries), pks_store, pk_averages
    



# Define the shell commands
commands = [
    "rm -rf results",
    "rm -rf qrels",
    "mkdir results",
    "mkdir qrels"
]

# Execute each command


topks = [520]
scores = ["avg"]
reRankDocs = [40]
reRankWeights = [95]
metric = "MAP_AND_AUC"   #MAP, AUC, MAP_AND_AUC
system = "m2"



queries = [
    "sh_childhood",
    "luffy_fight",
    "bounty",
    "ancient_weapon"
]

for i in range(0, len(queries)):
    if system != "":
        queries[i] = system + "_" + queries[i]


best_result = 0
for topk in topks:
    for score in scores:
        for reRankDoc in reRankDocs:
            for reRankWeight in reRankWeights:
                for command in commands:
                    subprocess.run(command, shell=True, check=True)
                    

                query_command = f"python pipeline.py --query ./grid_search.json --topk {topk} --score {score} --reRankDocs {reRankDoc} --reRankWeight {reRankWeight} --gridSearch True"
                subprocess.run(query_command, shell=True, check=True)
                result, map, auc, pks_store, pk_averages = evaluate_results(queries, metric)
                if result > best_result:
                    best_result = result
                    plot_pr_curve(queries)
                    print("The best " + metric + " is: " + str(best_result) + " with params: \n")
                    print("   -topk: " + str(topk) + ";")
                    print("   -scores: " + score + ";")
                    print("   -reRankDocs: " + str(reRankDoc) + ";")
                    print("   -reRankWeights: " +str(reRankWeight) + ";")
                    print(map)
                    print(auc)
                    print("pks: ")
                    for pks in pks_store:
                        print(pks)
                    print(pk_averages)








