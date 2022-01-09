#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



#sets executable path - aka what to open and how -- using chrome browser here
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# tells browser to visit NASA site
url = 'http://redplanetscience.com'
browser.visit(url)
# sets optional delay for loading page
browser.is_element_present_by_css('div.list_text',wait_time = 1)
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# uses parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# uses parent element to find paragraph text
news_p = slide_elem.find('div', class_ ='article_teaser_body').get_text()
news_p

# ### IMAGE SCRAPING
# visits URL for image scraping
url = 'https://spaceimages-mars.com'
browser.visit(url)

# finds and clicks the full-size image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parses full-size image with SOUP
html = browser.html
img_soup = soup(html,'html.parser')

# finds the relative image url so that we can grab the featured picture even as it changes
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#  ### DATA SCRAPING FROM TABLE
# creates df from reading website
df = pd.read_html('https://galaxyfacts-mars.com')[0]4
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# converts data frame to usable html code to allow us to add to a web page
df.to_html()

# IMPORTANT! Turns off the automatic scraping once the scrape is finished. IMPORTANT!
browser.quit()





