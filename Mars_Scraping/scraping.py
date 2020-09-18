#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(), 
        "hemispheres" : hemisphere_data(browser)
    }


    # Stop webdriver and return data
    browser.quit()
    return data

#Scrape Mars News
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #begin scraping
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

#Scrape hemisphere data
def hemisphere_data(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

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


    return hemisphere_image_urls


#Scrape Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()


    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling:
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# Fact scraping
def mars_facts():

    #Add try/except for error handling:
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    

    #Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


