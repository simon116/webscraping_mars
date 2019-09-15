#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs

import requests
import pymongo


# In[2]:


url = 'https://mars.nasa.gov/news'
url


# In[3]:


get_ipython().system('which chromedriver')


# In[4]:


# ex_path = {'executable_path': 'chromedriver.exe'}
# For mac
ex_path_mac = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **ex_path_mac, headless=False)


# In[5]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[6]:


# Define database and collection
db = client.nasa_db
collection = db.items


# In[7]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news'

# Retrieve page with the requests module
#response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
#soup = BeautifulSoup(response.text, 'lxml')


# ### Latest Mars News

# In[8]:


# Go to this link using our browser module
browser.visit(url)


# In[9]:


# Grab the html code
url_html = browser.html


# In[10]:


# Parse (converting string to consumable html code)
url_scraper = bs(url_html, 'html.parser')


# In[11]:


# Find the container that holds the value that we want, and specify the class so that it's specific
title_element = url_scraper.find('div', {'class': 'content_title'}).findChild()

title_text = title_element.get_text()
title_text


# In[12]:


# Find the paragraph (teaser)
body_element = url_scraper.find('div', {'class': 'article_teaser_body'})
body_element

body_text = body_element.get_text()
body_text


# ### Mars Images

# In[13]:


# Visit the Browser and capture the html of that particular page
images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

browser.visit(images_url)


# In[14]:


# Capture the new html from the new page
image_html = browser.html
# Create and feed a new scraper the new html
image_scraper = bs(image_html, 'html.parser')


# In[15]:


# Go to next image page by clicking on the "full image" button
full_image_btn_element = image_scraper.find('a', {'class': 'button fancybox'})
full_image_btn_element


# In[16]:


# Click the 'full image' button
browser.click_link_by_id('full_image')


# In[18]:


# Click the 'more info' button
browser.is_element_present_by_text('more info', wait_time=1)
browser.click_link_by_partial_text('more info')


# In[19]:


# Scrape the image from the img element
jpl_image_html = browser.html

jpl_image_scraper = bs(jpl_image_html, 'html.parser')

jpl_image = jpl_image_scraper.find('img', {'class': 'main_image'})

jpl_image_url = jpl_image.get('src')
jpl_image_url


# In[20]:


# Scrape 4 different hemisphere images and their titles
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[ ]:




# url_jpl = https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars


# In[25]:


# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."}
# ]
    
    
m_urls = [
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
]
    
hs_image_data = []    

# for loop through m_urls list and perform some web scraping logic for each link
for url in m_urls:
    print(url)
    # DO ALL SCRAPING LOGIC HERE
    # create empty dictionary
    album = {}
    
    # click link
    browser.visit(url)
    
    # scrape the title and image url
    # Scrape the image from the img element
    m_html = browser.html

    m_scraper = bs(m_html, 'html.parser')

    m_title = m_scraper.find('h2', {'class': 'title'}).get_text()
    
    # add title to album
    album['title'] = m_title
    
    # repeat scraping and extracting steps for image src
    m_image_href = m_scraper.find('div', {'class': 'downloads'}).find('a').get('href')
    album['link'] = m_image_href
    
    # add album to the list
    hs_image_data.append(album)
    
    # go back a page in the browser
    browser.back()


# In[26]:


hs_image_data


# In[ ]:




