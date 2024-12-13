import sys
import json
import csv
import re
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

def process_text_phrase_by_phrase(text):
    phrases = re.split(r'[.!?]\s+', text)
    return [phrase.strip() for phrase in phrases if phrase.strip()]

if __name__ == "__main__":

    csv_file = '../../data/data.csv' 
    #json_file = '../../data/data_embeddings.json' 
    json_file = './summary_embeddings.json'

    data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)


    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        #title = document.get("Title", "")
        #season = document.get("Season", "")
        #arc = document.get("Arc", "")
        #saga = document.get("Saga", "")
        summary = document.get("Summary", "")
        #anime_notes = document.get("anime notes", "")
        #episode_script = document.get("episode script", "")

        # Generate embeddings for each field
        #title_embedding = get_embedding(title)
        #season_embedding = get_embedding(season)
        #arc_embedding = get_embedding(arc)
        #saga_embedding = get_embedding(saga)

        # Generate embeddings phrase by phrase for Summary, Anime Notes, and Episode Script
        summary_phrases = process_text_phrase_by_phrase(summary)
        #anime_notes_phrases = process_text_phrase_by_phrase(anime_notes)
        #episode_script_phrases = process_text_phrase_by_phrase(episode_script)

        summary_embeddings = [get_embedding(phrase) for phrase in summary_phrases]
        #anime_notes_embeddings = [get_embedding(phrase) for phrase in anime_notes_phrases]
        #episode_script_embeddings = [get_embedding(phrase) for phrase in episode_script_phrases]

        # Combine all embeddings into a single vector
        combined_embeddings = (
            [item for sublist in summary_embeddings for item in sublist]
        )

        document["vector"] = combined_embeddings

    # Output updated JSON to STDOUT
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    #json.dump(data, json_file, indent=4, ensure_ascii=False)
