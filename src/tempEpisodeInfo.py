from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://onepiece.fandom.com/wiki/Episode_336"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

summary_item = soup.find(lambda tag: tag.name == "h2" and tag.text == "Long Summary[]" or tag.text == "Summary[]")
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
#if season_piece has class pi-collapse , season is named as "N/A"
if 'pi-collapse' in season_piece['class']:
    content_dict["Season"] = "N/A"
else:
    content_dict["Season"] = (season_piece.find_all("td"))[0].text

print(content_dict)
