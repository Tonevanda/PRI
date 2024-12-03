import sys
import json
import csv
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":

    csv_file = 'data.csv'  # Replace with your CSV file path
    json_file = 'data_embeddings.json'  # Replace with your desired JSON file path

    data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)


    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        title = document.get("title", "")
        objectives = document.get("objectives", "")
        learning_outcomes = document.get("learning_outcomes", "")

        combined_text = title + " " + objectives + " " + learning_outcomes
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    #json.dump(data, json_file, indent=4, ensure_ascii=False)
