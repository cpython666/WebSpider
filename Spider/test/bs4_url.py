import requests
from bs4 import BeautifulSoup

# url = "https://www.huxiu.com/"
#
# response = requests.get(url)
# html = response.content
# print(html)
with open("../utils/虎嗅主页.html", 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")
links = []
for link in soup.find_all("a"):
    links.append(link.get("href"))

for link in links:
    print(link)