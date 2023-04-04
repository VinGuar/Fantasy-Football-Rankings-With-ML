import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

def makeCommentTable(soup1):

    #finds all comments in soup. 
    comments = soup1.find_all(string=lambda text: isinstance(text, Comment) and "table_container" in text)
    roster_html = str(comments).replace('<!--', '').replace('-->', '')
    
    # Parse the HTML content using Beautiful Soup
    roster_soup = BeautifulSoup(roster_html, 'html.parser')

    # Find the roster table by its HTML id
    table = roster_soup.find('table', {'id': 'roster'})
    df = pd.read_html(str(table))[0]

    return df

    #this iterates through each of comments "things" and sees if it has table. If it is table, appends to table array.
    for things in comments:
        if 'table_container' in things:
            try:
                return pd.read_html(things)[0]
            except:
                continue

        return 0
    
x = requests.get("https://www.pro-football-reference.com/teams/crd/2023_roster.htm")
soup = BeautifulSoup(x.content, 'html.parser')
table = soup.find('table', {'class': 'sortable stats_table'})

table = makeCommentTable(soup)

print(table)