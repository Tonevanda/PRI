import os
import re
import pandas as pd

def scrape_ass_files():
    subtitles_list = []
    directory = "full_ep_transcripts"
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return {}
    
    for i in range(1, 932):
        ass_path = os.path.join(directory, f"{i}.ass")
        srt_path = os.path.join(directory, f"{i}.srt")
        
        if os.path.exists(ass_path):
            correct_path = ass_path
            with open(correct_path, 'r', encoding='utf-8') as file:
                content = file.read()
                dialogues = re.findall(r"Dialogue:.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,.*?,(.*)", content)
                cleaned_dialogues = [re.sub(r"{.*?}", "", dialogue).replace("\\N", " ") for dialogue in dialogues]  # Remove formatting tags and "\N"
                cleaned_dialogues = [re.sub(r"\.\.\.", " ", dialogue) for dialogue in cleaned_dialogues]
                subtitles_list.append(" ".join(cleaned_dialogues))  # Join dialogues into a single string
        elif os.path.exists(srt_path):
            print(".srt instead of ass")
            '''
            correct_path = srt_path
            with open(correct_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                dialogues = re.findall(r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*)", content)
                cleaned_dialogues = [re.sub(r"{.*?}", "", dialogue).replace("\\N", " ") for dialogue in dialogues]  # Remove formatting tags and "\N"
                cleaned_dialogues = [re.sub(r"\.\.\.", " ", dialogue) for dialogue in cleaned_dialogues]
                subtitles_list.append(" ".join(cleaned_dialogues))  # Join dialogues into a single string
            '''
        else:
            subtitles_list.append("")

    #loop from 932 to 1121 this will be removed later
    for i in range(932,1122):
        subtitles_list.append("not yet done")
    return subtitles_list

if __name__ == "__main__":
    # Read the existing CSV file
    csv_file = "data.csv"
    df = pd.read_csv(csv_file)

    # Scrape subtitles
    subtitles_list = scrape_ass_files()

    #print(subtitles_list[110],[111],[112])

    df["episode script"] = subtitles_list

    # Write the updated DataFrame to a new CSV file
    updated_csv_file = "updated_data.csv"
    df.to_csv(updated_csv_file, index=False)

    print(f"Subtitles added and saved to {updated_csv_file}")
    