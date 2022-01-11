#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd


def scrape_all():
    # sets executable path - aka what to open and how -- using chrome browser here
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # runs scrapes and saves to dictionary named 'data'
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # stops webdriver and returns data
    browser.quit()
    return data


# creates function for first scrape:

def mars_news(browser):
    # tells browser to visit NASA site
    url = 'http://redplanetscience.com'
    browser.visit(url)
    # sets optional delay for loading page
    browser.is_element_present_by_css('div.list_text',wait_time = 1)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # adds try/except for error handling on scrapes
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    #end error check
    
    return news_title, news_p

# ### IMAGE SCRAPING

# define image scraping function
def featured_image(browser):
    # visits URL for image scraping
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # finds and clicks the full-size image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parses full-size image with SOUP
    html = browser.html
    img_soup = soup(html,'html.parser')

    # checks img scrape for errors
    try: 
        # finds the relative image url so that we can grab the featured picture even as it changes 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    #end error check

    # creates absolute url from base 'img_url_rel'    
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

   
    #returns image
    return img_url

#  ### DATA SCRAPING FROM TABLE
#define function to scrape table
def mars_facts():
    # adds try/except for error handling on table scrape
    try:
        # uses 'read_html' pandas function to scrape facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    #end error check
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def mars_hemispheres():
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write5 code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    urls_soup = soup(html,'html.parser')

    divs = urls_soup.find("div", class_='collapsible results')
    anchors = divs.find_all('a')
    rel_urls = set([anchor['href'] for anchor in anchors])
    print(rel_urls)
    base_url = 'https://marshemispheres.com/'

    for rel_url in rel_urls:
        # creates dictionary to store hemispheres information
        hemispheres = {}
        # creates full urls and point browser to correct link
        url_full = f'{base_url}{rel_url}'
        browser.visit(url_full)

        # parses full links to images and titles
        html = browser.html
        urls_soup = soup(html, 'html.parser')
        
        browser.links.find_by_text('Sample').click()
        challenge_img_url_rel = urls_soup.find('img').get('src')
        challenge_img_url_rel
        
        browser.visit(url_full)
        title_elem = urls_soup.select_one('div.content') #issues here
        title = title_elem.find('h2', class_='title').get_text()
   
        hemispheres = {
            'img_url': challenge_img_url_rel,
            'title': title,
            }
        hemisphere_image_urls.append(hemispheres)

    # quits the browser
    browser.quit()
    
    # Returns the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

    



