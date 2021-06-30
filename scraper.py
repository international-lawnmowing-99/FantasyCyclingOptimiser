import requests
from bs4 import BeautifulSoup

URL  = "https://www.procyclingstats.com/race/tour-de-france/startlist"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')



teams = soup.find_all(class_='team')

for team in teams:
    results = team.find_all(class_='blue')
    for result in results:
        print(result.text)


#splitText = results.text.split()
