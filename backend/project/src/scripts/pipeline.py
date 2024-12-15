import argparse
import sys
import subprocess
import json
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str


def feedForward(query_file):
    # Load the query parameters from the JSON file
    try:
        query_json = json.load(open(query_file))
    except FileNotFoundError:
        print(f"Error: Query file {query_file} not found.")
        sys.exit(1)

    for query_name, params in query_json.items():
        params['q'] = params['q'].replace('"', '\\"')
        rqq = "False"
        if(not query_name.startswith("m2") and not query_name.startswith("def")):
            rqq = "True"

        command = (
            f"python query_solr.py --query \"{params['q']}\" --collection {params['collection']} --useParams {params['useParams']} --uri http://localhost:8983/solr --useRqq {rqq} |"
            f"python solr2trec.py > ./results/{query_name}.txt"
        )
        subprocess.run(command, shell=True, check=True)
        
        qrel_str = "-".join(str(qrel_item) for qrel_item in params['qrel'])


        command = (
            f"python qrels2trec.py --qrels {qrel_str} > ./qrels/{query_name}.txt"
        )

        subprocess.run(command, shell=True, check=True)


        
def plot_pr_curve():
    queries = [
        "sh_childhood",
        "luffy_fight",
        "bounty",
        "ancient_weapon"
    ]

    for query in queries:
        command = (
            f"python plot_pr.py --qrels ./qrels/{query}.txt --def_qrels ./qrels/def_{query}.txt --m2_qrels ./qrels/m2_{query}.txt --output ./diagrams/{query}.png"
        )
        subprocess.run(command, shell=True, check=True)



if __name__ == "__main__":
    # Argument parser to handle the query file as command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate a Precision-Recall curve from Solr results (in TREC format) and qrels."
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Path to the query json file",
    )
    
    args = parser.parse_args()


    feedForward(args.query)
    plot_pr_curve()
