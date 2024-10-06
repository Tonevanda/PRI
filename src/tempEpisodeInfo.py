from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://onepiece.fandom.com/wiki/Episode_1"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

long_summary_item = soup.find(lambda tag: tag.name == "h2" and tag.text == "Long Summary[]")
content_dict={}

sibling = long_summary_item.find_next_sibling()
long_summary_text = []
while sibling.name == "p":
    long_summary_text.append(sibling.text)
    sibling = sibling.find_next_sibling()
content_dict["Long Summary"] = "\n".join(long_summary_text)

air_date = soup.find(lambda tag: tag.name == "h3" and tag.text == "Airdate").find_next_sibling()
content_dict["Airdate"] = air_date.text

opening_ending = air_date.parent.parent.find_next_sibling().find_all("a")
content_dict["Opening"] = opening_ending[0].text
content_dict["Ending"] = opening_ending[1].text

season_piece=air_date.parent.parent.find_next_sibling().find_next_sibling().find_all("td")
content_dict["Season"] = season_piece[0].text
content_dict["Piece"] = season_piece[1].text

print(content_dict)
