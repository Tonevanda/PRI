import sys
import json
import csv
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()
def truncate_text(text, max_words=256):
    words = text.split()
    truncated_words = words[:max_words]
    return ' '.join(truncated_words)

def process_text_in_chunks(text, max_words=256):
    words = text.split()
    chunks = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    return [' '.join(chunk) for chunk in chunks]
if __name__ == "__main__":

    csv_file = '../../data/data.csv'  # Replace with your CSV file path
    json_file = '../../data/data_embeddings.json'  # Replace with your desired JSON file path

    data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)


    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        title = document.get("Title")
        season = document.get("Season")
        arc = document.get("Arc")
        saga = document.get("Saga")
        summary = document.get("Summary")
        anime_notes = document.get("anime notes")
        episode_script = document.get("episode script")

        combined_text = f"{title} {season} {arc} {saga} {summary} {anime_notes} {episode_script}"
        text_chunks = process_text_in_chunks(combined_text, max_words=256)

        # Initialize an empty list to store the combined embeddings
        combined_embeddings = []

        for chunk in text_chunks:
            embedding = get_embedding(chunk)
            combined_embeddings.extend(embedding)

        document["vector"] = combined_embeddings

    # Output updated JSON to STDOUT
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    #json.dump(data, json_file, indent=4, ensure_ascii=False)
