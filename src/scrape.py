from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://onepiece.fandom.com/wiki/Episode_Guide"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

article_tab = soup.find_all(class_="article-tabs")

li = article_tab[0].find_all("li")

saga_dict = {}

# Save in dictionary the name of the saga and the url
for item in li:
    if item.find("a"):
        saga = item.find("a").text
        url = "https://onepiece.fandom.com" + item.find("a")["href"]
        saga_dict[saga] = url

for saga, url in saga_dict.items():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    h2_id = saga.replace(" ", "_")
    h2 = soup.find(id=h2_id)

    arcs = h2.find_all_next("h3")
    for arc in arcs:
        if("Arc" not in arc.text):
            continue
        episodes = arc.find_all_next("a", href = True)
        for episode in episodes:
            if(episode.find_previous("h3") != arc):
                break
            href = episode["href"]
            # Check if href contains "Episode_" followed by a number to avoid recaps, movies, etc.
            if re.search(r"Episode_\d+", href):
                episode_name = episode.text
                episode_url = "https://onepiece.fandom.com" + href
                print(episode_name, episode_url)