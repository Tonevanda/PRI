import os
import re
import pandas as pd

def scrape_subtitle_files():
    subtitles_list = []
    directory = "full_ep_transcripts"
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []
    
    for i in range(1, 1122):
        ass_path = os.path.join(directory, f"{i}.ass")
        srt_path = os.path.join(directory, f"{i}.srt")
        
        if os.path.exists(ass_path):
            correct_path = ass_path
            
            with open(correct_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                dialogues = re.findall(r"Dialogue:.*?,(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),.*?,.*?,.*?,.*?,.*?,.*?,(.*)", content)
                cleaned_dialogues = []
                
                for start_time, end_time, dialogue in dialogues:
                    #isto vai ser cancro holy moly
                    if (i < 48 and time_to_seconds(end_time) >= 111) or (i >= 48 and i < 116 and time_to_seconds(end_time) >= (60+47)) or (i >= 116 and i < 169 and time_to_seconds(end_time) >= (60+49)) or (i >= 169  and i < 207 and time_to_seconds(end_time) >= (60+51)) or (i >= 207  and i < 239 and time_to_seconds(end_time) >= (120)) or (i >= 239  and i < 264) or (i >= 264 and i < 279) or (i >= 279 and i < 284 and time_to_seconds(end_time) >= (124)) or (i >= 284 and i < 326 and time_to_seconds(end_time) >= (120+42)) or (i >= 326  and i < 397 and time_to_seconds(end_time) >= (180+23)) or (i >= 397  and i < 426 and time_to_seconds(end_time) >= (180+30)) or (i == 426 and time_to_seconds(end_time) >= (120+44)) or (i >= 427 and i < 492 and time_to_seconds(end_time) >= (180+30)) or (i == 492) or (i >= 493  and i < 517 and time_to_seconds(end_time) >= (180+30)) or (i == 517) or (i >= 518 and i< 522 and time_to_seconds(end_time) >= (182)) or (i == 522 and time_to_seconds(end_time) >= (180)) or (i == 523 and time_to_seconds(end_time) >= (180 + 48)) or (i == 524 and time_to_seconds(end_time) >= (180 + 44)) or (i == 525 and time_to_seconds(end_time) >= (180 + 45)) or (i == 526 and time_to_seconds(end_time) >= (180 + 45)) or (i == 527 and time_to_seconds(end_time) >= (180 + 50)) or ((i == 528 or i == 529) and time_to_seconds(end_time) >= (180 + 47)) or ((i == 530 or i == 531) and time_to_seconds(end_time) >= (180 + 26)) or (i == 532 and time_to_seconds(end_time) >= (180 + 45)) or (i == 533 and time_to_seconds(end_time) >= (180 + 46)) or ((i == 534 or i == 535) and time_to_seconds(end_time) >= (180 + 27))  or (i >= 536 and i < 569 and time_to_seconds(end_time) >= (180 + 46)) or (i == 569 and time_to_seconds(end_time) >= (180 + 33)) or (i >= 570 and i<575 and time_to_seconds(end_time) >= (180 + 47)) or (i == 575 and time_to_seconds(end_time) >= (180 + 35)) or (i >= 576 and i < 579 and time_to_seconds(end_time) >= (180 + 54)) or (i == 579 and time_to_seconds(end_time) >= (240 + 5)) or (i >= 580 and i < 617 and time_to_seconds(end_time) >= (180 + 39)) or (i >= 617 and i < 625 and time_to_seconds(end_time) >= (180 + 56)) or (i >= 625 and i < 627 and time_to_seconds(end_time) >= (180 + 25)) or ((i == 627 or i == 628) and time_to_seconds(end_time) >= (180 + 52)) or (i == 629 and time_to_seconds(end_time) >= (180 + 55)) or (i >= 630 and i < 687 and time_to_seconds(end_time) >= (180 + 47)) or (i >= 687 and i < 705 and time_to_seconds(end_time) >= (180 + 57)) or (i >= 705 and i < 747 and time_to_seconds(end_time) >= (180 + 46)) or (i >= 747 and i < 753 and time_to_seconds(end_time) >= (180 + 38)) or (i >= 753 and i < 806 and time_to_seconds(end_time) >= (240 + 2)) or (i == 806 and time_to_seconds(end_time) >= (180 + 14)) or (i >= 807 and i < 825 and time_to_seconds(end_time) >= (180)) or (i == 825) or (i == 826 and time_to_seconds(end_time) >= (180 + 3)) or (i == 827) or (i >= 828 and i < 856 and time_to_seconds(end_time) >= (120 + 55)) or (i >= 856 and i < 892 and time_to_seconds(end_time) >= (180 + 30)) or (i >= 892 and i < 935 and time_to_seconds(end_time) >= (120 + 23)) or (i >= 935 and i < 1000 and time_to_seconds(end_time) >= (120 + 25)) or (i == 1000 and time_to_seconds(end_time) >= (120 + 14)) or (i >= 1001 and i < 1009 and time_to_seconds(end_time) >= (120 + 2)) or (i >= 1009 and i < 1073 and time_to_seconds(end_time) >= (120 + 23)) or (i == 1073 and time_to_seconds(end_time) >= (60 + 27)) or (i >= 1074 and i < 1076 and time_to_seconds(end_time) >= (60 + 50)) or (i >= 1076 and i < 1089 and time_to_seconds(end_time) >= (60 + 36)) or (i >= 1089 and time_to_seconds(end_time) >= (60 + 37)):
                        #406 is filler
                        cleaned_dialogues.append(re.sub(r"{.*?}", "", dialogue).replace("\\N", " "))  # Remove formatting tags and "\N"
                cleaned_dialogues = [re.sub(r"\.\.\.", " ", dialogue) for dialogue in cleaned_dialogues]
                subtitles_list.append(" ".join(cleaned_dialogues))  # Join dialogues into a single string
        elif os.path.exists(srt_path):
            print(".srt instead of ass")
            """
            correct_path = srt_path
            with open(correct_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                dialogues = re.findall(r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*)", content)
                cleaned_dialogues = [re.sub(r"{.*?}", "", dialogue).replace("\\N", " ") for dialogue in dialogues] 
                cleaned_dialogues = [re.sub(r"\.\.\.", " ", dialogue) for dialogue in cleaned_dialogues]
                subtitles_list.append(" ".join(cleaned_dialogues))  # Join dialogues into a single string
            """
        elif (i == 542):
            print("filler lmao")
        else:
            print(i)
            subtitles_list.append("")

    
    return subtitles_list

def time_to_seconds(time_str):
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

def clean_script(script, episode_name):
    """
    if pd.isnull(script) or pd.isnull(episode_name):
        return script
    print(episode_name)
    pattern = re.compile(r'.*?' + re.escape(episode_name), re.DOTALL)
    match = pattern.search(script)
    if match:
        return script[match.start():]
        """
    return script

if __name__ == "__main__":
    # Read the existing CSV file
    csv_file = "data.csv"
    df = pd.read_csv(csv_file)

    # Scrape subtitles
    subtitles_list = scrape_subtitle_files()

    # Clean each script by removing text before the episode name
    df["episode script"] = subtitles_list

    # Write the updated DataFrame to a new CSV file
    updated_csv_file = "updated_data.csv"
    df.to_csv(csv_file, index=False)