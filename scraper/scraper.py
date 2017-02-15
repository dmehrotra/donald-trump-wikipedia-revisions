from bs4 import BeautifulSoup
import urllib
import twitter

from pyvirtualdisplay import Display
from selenium import webdriver
from PIL import Image

url = 'https://en.wikipedia.org/w/index.php?title=Donald_Trump&action=history'
html = urllib.urlopen(url).read()

api = twitter.Api(
consumer_key='',
consumer_secret='',
access_token_key='',
access_token_secret=''
)

init_soup = BeautifulSoup(html, 'html.parser')
revision = init_soup.select('ul#pagehistory li')[0]
date = revision.select('a.mw-changeslist-date')[0].text
user = revision.select('a.mw-userlink')[0].text 
link = "https://en.wikipedia.org" + revision.select('span.mw-history-histlinks a')[0]['href']
comment = ""

new_revision = False
def prepare_options(d,u,c,l):
  medium = "From [ "+ u + " ] " + "- " + link 
  long =  medium  
  short =  link 
  return [short,medium,long]

options = prepare_options(date,user,comment,link)

tweet = "too long"

for o in options:
  if len(o) <= 140:
    tweet = o 

print tweet
with open("/root/scripts/repeater/scraper/current_revision.txt","r+") as current_revision:
  if current_revision.read() != tweet.encode('utf-8'):
    new_revision = True
    current_revision.seek(0)
    current_revision.write(tweet.encode('utf8'))
    current_revision.truncate()
    current_revision.close()  

if new_revision:
  display = Display(visible=0, size=(800,1500))
  display.start()
  browser = webdriver.Firefox(executable_path='/root/geckodriver')
  print "going to link"
  browser.get(link)
  input_element = browser.find_element_by_class_name('diff-deletedline')
  print "found element"
  element =  input_element.find_element_by_xpath('..')
  print "xpath" 
  location = element.location
  size = element.size
  browser.save_screenshot('screenie.png') # saves screenshot of entire page
  browser.quit()
  display.stop()
  print 'done with screenshot'
  im = Image.open('screenie.png') # uses PIL library to open image in memory
  print 'opened image'
  left = location['x']
  top = location['y']
  right = location['x'] + size['width']
  bottom = location['y'] + size['height']
  print 'cropping'
  print left + top + right + bottom
  im = im.crop((int(float(left)),int(float(top)),int(float(right)),int(float(bottom)))) # defines crop points
  im.save('screenshot.png')
  status = api.PostMedia(tweet,"screenshot.png") 



