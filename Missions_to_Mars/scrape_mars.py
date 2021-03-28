from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
from webdriver_manager.chrome import ChromeDriverManager
warnings.filterwarnings('ignore')

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

mars_info = {}

#News
def scrape_mars_news():

        browser = init_browser()

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        html = browser.html

        news_info = bs(html, 'html.parser')

        news_title = news_info.find_all('div', class_='content_title')[1].text
        news_paragraph = news_info.find_all('div', class_='article_teaser_body')[0].text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_paragraph

        return mars_info


#Image
def scrape_mars_image():
 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        jpl_url ='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        jpl_url_modified = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
        browser.visit(jpl_url)


        image_html = browser.html
        image_info = bs(image_html, 'html.parser')

       
        image_path = image_info.find_all('img', class_='headerimage fade-in')[0]["src"]
        featured_image_url = jpl_url_modified + image_path 

        # Dictionary entry from FEATURED IMAGE
        mars_info['image_url'] = featured_image_url 
        
        browser.quit()

        return mars_info

        
        
# Mars Facts
def scrape_mars_facts():

        browser = init_browser()

        url = 'http://space-facts.com/mars/'
        browser.visit(url)

        tables = pd.read_html(url)
        #Find Mars Facts DataFrame in the lists of DataFrames
        df = tables[1]
        #Assign the columns
        df.columns = ['Description', 'Value']
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)



        mars_info['tables'] = html_table

        return mars_info

# Mars Hemisphere

def scrape_mars_hemispheres():

        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        soup = bs(html_hemispheres, 'html.parser')

        items = soup.find_all('div', class_='item')

        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            browser.visit(hemispheres_main_url + partial_img_url)
            
            partial_img_html = browser.html
            
            soup = bs( partial_img_html, 'html.parser')
            
             
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        
       
        browser.quit()

        # Return mars_data dictionary 

        return mars_info