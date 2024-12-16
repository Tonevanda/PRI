import sys
import json
import csv
import re
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats

    embedding = model.encode(text, convert_to_tensor=False, normalize_embeddings=True).tolist()
    return embedding

def truncate_text(text, max_words=256):
    words = text.split()
    truncated_words = words[:max_words]
    return ' '.join(truncated_words)

def process_text_in_chunks(text, arcs, sagas, max_words=256):
    words = text.split()
    chunks = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    return [' '.join(chunk) for chunk in chunks]

def process_text_phrase_by_phrase(text):
    phrases = re.split(r'[.!?]\s+', text)
    return [phrase.strip() for phrase in phrases if phrase.strip()]

if __name__ == "__main__":

    csv_file = '../../data/data.csv' 
    json_file = '../../data/data_embeddings.json' 

    data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    combined_embeddings = []
    
    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        summary = document.get("Summary", "")
        document["vectors"] = []


        # Generate embeddings phrase by phrase for Summary, Anime Notes, and Episode Script
        summary_phrases = process_text_phrase_by_phrase(summary)

        for phrase in summary_phrases:
            # Generate embeddings for each phrase
            embedding = get_embedding(phrase)
            document["vectors"].append({
                "vector": embedding
            })
    

    # Output updated JSON to STDOUT
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    #json.dump(data, json_file, indent=4, ensure_ascii=False)
