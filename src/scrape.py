from bs4 import BeautifulSoup
import requests
import pandas as pd

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

print (saga_dict)