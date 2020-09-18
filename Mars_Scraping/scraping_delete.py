#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[15]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# ### Mars Weather

# In[17]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[18]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[19]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[20]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[21]:


#Empty list
hemisphere_image_urls = []


#Cerberus
browser.links.find_by_partial_text('Cerberus').click()
html = browser.html
cerberus_soup = soup(html, 'html.parser')
cerberus_url = cerberus_soup.select_one('div.downloads a').get("href")
cerberus_title = cerberus_soup.select_one('h2', class_="title").text

#dictionary:
cerberus_dict = {
        "img_url": cerberus_url,
        "title": cerberus_title
    }

hemisphere_image_urls.append(cerberus_dict)


#Schiaparelli
browser.links.find_by_partial_text('Schiaparelli').click()
html = browser.html
schiaparelli_soup = soup(html, 'html.parser')
schiaparelli_url = schiaparelli_soup.select_one('div.downloads a').get("href")
schiaparelli_title = schiaparelli_soup.select_one('h2', class_="title").text

#dictionary:
schiaparelli_dict = {
        "img_url": schiaparelli_url,
        "title": schiaparelli_title
    }

hemisphere_image_urls.append(schiaparelli_dict)

#Syrtis
browser.links.find_by_partial_text('Syrtis').click()
html = browser.html
syrtis_soup = soup(html, 'html.parser')
syrtis_url = syrtis_soup.select_one('div.downloads a').get("href")
syrtis_title = syrtis_soup.select_one('h2', class_="title").text

#dictionary:
syrtis_dict = {
        "img_url": syrtis_url,
        "title": syrtis_title
    }

hemisphere_image_urls.append(syrtis_dict)

#Valles
browser.links.find_by_partial_text('Valles').click()
html = browser.html
valles_soup = soup(html, 'html.parser')
valles_url = valles_soup.select_one('div.downloads a').get("href")
valles_title = valles_soup.select_one('h2', class_="title").text

#dictionary:
valles_dict = {
        "img_url": valles_url,
        "title": valles_title
    }

hemisphere_image_urls.append(valles_dict)


# In[26]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[27]:


# 5. Quit the browser
browser.quit()


# In[ ]:




