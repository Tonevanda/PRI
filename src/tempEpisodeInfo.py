from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://onepiece.fandom.com/wiki/Episode_1"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")


mw_content_text = soup.find_all(class_=["mw-body-content","mw-content-ltr"])

mw_parser_output = mw_content_text[0].find_all(class_="mw-parser-output")

h2_list = mw_parser_output[0].find_all("h2")

content_dict={}

for h2 in h2_list:
    sibling = h2.find_next_sibling()
    while sibling.name == "p" or sibling.name == "ul":
        if sibling.name == "ul":
            for characters in sibling.find_all("a"):
                content_dict.update({h2.text:characters.text})
            sibling=sibling.find_next_sibling()
        else:
            content_dict.update({h2.text:sibling.text})
            sibling=sibling.find_next_sibling()

print(content_dict)

