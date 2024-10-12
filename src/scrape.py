from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# Converts the date in format "October 12, 2003" to "2003-10-12" (Pandas' preferred format)
def date_converter(date):
    months = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    date = date.split(" ")
    return f"{date[2]}-{months[date[0]]}-{date[1][:-1]}"
    

def scrape_episode(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    summary_item = soup.find(lambda tag: tag.name == "h2" and (tag.text == "Long Summary[]" or tag.text == "Summary[]"))
    content_dict={}

    long_summary = summary_item.find_next_sibling()
    summary_text = []
    while long_summary.name == "p":
        summary_text.append(long_summary.text)
        long_summary = long_summary.find_next_sibling()
    if len(summary_text) == 0:
        summary_item = soup.find(lambda tag: tag.name == "h2" and tag.text == "Short Summary[]")
        short_summary = summary_item.find_next_sibling()
        summary_text = []
        while short_summary.name == "p":
            summary_text.append(short_summary.text)
            short_summary = short_summary.find_next_sibling()

    content_dict["Summary"] = "\n".join(summary_text)

    air_date = soup.find(lambda tag: tag.name == "h3" and tag.text == "Airdate").find_next_sibling()
    content_dict["Airdate"] = air_date.text

    opening_ending = air_date.parent.parent.find_next_sibling().find_all("a")
    content_dict["Opening"] = opening_ending[0].text
    if len(opening_ending) > 1:
        content_dict["Ending"] = opening_ending[1].text
    else:
        content_dict["Ending"] = "N/A"

    season_piece=air_date.parent.parent.find_next_sibling().find_next_sibling()
    if len(season_piece) == 0 or 'pi-collapse' in season_piece['class']:
        content_dict["Season"] = "N/A"
    else:
        content_dict["Season"] = (season_piece.find_all("td"))[0].text
    return content_dict

url = "https://onepiece.fandom.com/wiki/Episode_Guide"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

article_tab = soup.find_all(class_="article-tabs")

li = article_tab[0].find_all("li")

saga_dict = {}

episode_data = {
    "Episode": [],
    "Title": [],
    "Season": [],
    "Arc": [],
    "Saga": [],
    "Air Date": [],
    "Opening": [],
    "Ending": [],
    "Summary": []
}

# Save in dictionary the name of the saga and the url
for item in li:
    if item.find("a"):
        saga = item.find("a").text
        url = "https://onepiece.fandom.com" + item.find("a")["href"]
        saga_dict[saga] = url

for saga, url in saga_dict.items():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # The id of the h2 is the name of the saga with spaces replaced by underscores, so this makes it easy to find the arcs
    h2_id = saga.replace(" ", "_")
    h2 = soup.find(id=h2_id)

    arcs = h2.find_all_next("h3")

    for arc in arcs:
        if("Arc" not in arc.text):
            continue
        episodes = arc.find_all_next("a", href = True)
        for episode in episodes:
            if(episode.find_previous("h3") != arc): # So the scrapper doesn't go to the episodes of the next arc
                break
            href = episode["href"]
            if "Film" in href:
                continue
            # Check if href contains "Episode_" followed by a number to avoid recaps, movies, etc.
            match = re.search(r"Episode_(\d+)", href)
            
            if match:
                episode_number = match.group(1)
                if int(episode_number) == 542:
                    continue
                episode_name = episode.text
                episode_url = "https://onepiece.fandom.com" + href
                print(episode_name, episode_url)
                content_dict = scrape_episode(episode_url)
                episode_data["Episode"].append(episode_number)
                episode_data["Title"].append(episode.text)
                episode_data["Season"].append(content_dict["Season"])
                episode_data["Arc"].append(arc.text[:-2])
                episode_data["Saga"].append(saga)
                episode_data["Air Date"].append(date_converter(content_dict["Airdate"]))
                episode_data["Opening"].append(content_dict["Opening"])
                episode_data["Ending"].append(content_dict["Ending"])
                episode_data["Summary"].append(content_dict["Summary"])

df = pd.DataFrame(episode_data)

df.to_csv("data.csv", index=False)