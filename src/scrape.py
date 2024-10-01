from bs4 import BeautifulSoup
import requests

url = "https://onepiece.fandom.com/wiki/Episode_Guide"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="Navigation")

print(results.prettify())
