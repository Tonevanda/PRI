import argparse
import sys
import subprocess
import json



def feedForward(query_file):
    # Load the query parameters from the JSON file
    try:
        query_json = json.load(open(query_file))
    except FileNotFoundError:
        print(f"Error: Query file {query_file} not found.")
        sys.exit(1)

    for query_name, params in query_json.items():
        params['q'] = params['q'].replace('"', '\\"')
        command = (
            f"python ../src/scripts/query_solr.py --query \"{params['q']}\" --collection {params['collection']} --useParams {params['useParams']} --uri http://localhost:8983/solr |"
            f"python ../src/scripts/solr2trec.py > ./results/{query_name}.txt"
        )
        subprocess.run(command, shell=True, check=True)
        
        qrel_str = "-".join(str(qrel_item) for qrel_item in params['qrel'])


        command = (
            f"python ../src/scripts/qrels2trec.py --qrels {qrel_str} > ./qrels/{query_name}.txt"
        )

        subprocess.run(command, shell=True, check=True)




        command = (
            f"cat ./results/{query_name}.txt |"
            f"python ../src/scripts/plot_pr.py --qrels ./qrels/{query_name}.txt --output ./diagrams/{query_name}.png"
        )

        subprocess.run(command, shell=True, check=True)

        '''try:
            result = subprocess.run(['python', '../src/scripts/query_solr.py','--query', params['q'], '--collection', params['collection'], '--useParams', params['useParams'], '--uri', 'http://localhost:8983/solr'], check=True, capture_output=True, text=True)
            print(result.stdout)
            # If the command succeeds, you can access the output using result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing the command: {e}")
            print(f"Error output: {e.stderr}")
        
        with open('./results/results_bounty_trec.txt', 'w') as output_file:
            # Run the command and redirect output to the file
            subprocess.run(['python', '../src/scripts/solr2trec.py'], stdout=output_file, check=True)'''
        
        



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
