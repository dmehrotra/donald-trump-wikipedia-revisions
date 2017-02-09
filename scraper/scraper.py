from bs4 import BeautifulSoup
import urllib
import twitter

url = 'https://en.wikipedia.org/w/index.php?title=Donald_Trump&action=history'
html = urllib.urlopen(url).read()

init_soup = BeautifulSoup(html, 'html.parser')
revision = init_soup.select('ul#pagehistory li')[0]
date = revision.select('a.mw-changeslist-date')[0].text
user = revision.select('a.mw-userlink')[0].text
comment = revision.select('span.comment span')[0].text
new_revision = False
def prepare_options(d,u,c):
  medium = "[ "+ u + " ] " + "- " + c 
  long = "On " + d + " by " + medium  
  short =  medium[:136] +"..." 
  return [short,medium,long]

options = prepare_options(date,user,comment)

tweet = "too long"

for o in options:
  if len(o) <= 140:
    tweet = o 

with open("current_revision.txt","r+") as current_revision:
  if current_revision.read() != tweet:
    new_revision = True
    current_revision.seek(0)
    current_revision.write(tweet)
    current_revision.truncate()
    current_revision.close()  

if new_revision:
  status = api.PostUpdate(tweet)
    







