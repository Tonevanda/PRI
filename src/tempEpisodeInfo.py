from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from rake_nltk import Rake

#import nltk

#nltk.download('stopwords')
#nltk.download('punkt_tab')
#nltk.download('punkt')

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

rake = Rake()
rake.extract_keywords_from_text(content_dict["Summary"])
keywordsDict = {}
for score, keyword in rake.get_ranked_phrases_with_scores():
    if(score > 5.0):
        keywordsDict[keyword] = score

keywords = ""
isFirst = True
for keyword, score in keywordsDict.items():
    if isFirst:
        isFirst = False
    else:
        keywords += ", "
    keywords += keyword
content_dict['keywords'] = keywords

print(content_dict)

