# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import re
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #
    ### NASA Mars News 
    #

    # Visit url for NASA Mars News -- Latest News
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    first_news_node = browser.find_by_css('li.slide').first
    news_title = first_news_node.find_by_css('div.content_title').text
    news_para = first_news_node.find_by_css('div.article_teaser_body').text

    #
    ### JPL Mars Space Images
    #

    # Visit url for JPL Featured Space Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Go to 'FULL IMAGE'
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Go to 'more info'
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()   

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = bs(html, "html.parser")

    # Get featured image
    featured_img_url = image_soup.select_one("figure.lede a img").get("src")
    full_img_url = f'https://www.jpl.nasa.gov{featured_img_url}'

    #
    ### Mars Weather
    #

    # Visit Twitter url for latest Mars Weather
    clear_url = 'https://twitter.com/logout'
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(clear_url)
    time.sleep(3)
    browser.visit(weather_url)
    time.sleep(3)

    # Search Within Tweet for <p> Tag Containing Tweet Text
    no_weather_msg = "Failed to extract weather information"
    mars_weather = no_weather_msg

    # Elaborate approach: going down the DOM tree...
    soup = bs(browser.html, 'lxml')
    tweet_nodes = soup.select('div[data-testid="tweet"]')

    for tweet_node in tweet_nodes:
        # tweet_node has 2 child nodes: [0] - left sidebar, [1] - right tweet body
        tweet_right_part = tweet_node.contents[1]

        # tweet_right_part has 2 child nodes: [0] - header part, [1] - tweet contents part
        tweet_contents_part = tweet_right_part.contents[1]

        # tweet_contents_part has 3 child nodes: [0] - text, [1] - image, [2] - controls (reply/retweet/like)
        tweet_text = tweet_contents_part.contents[0]

        mars_weather = tweet_text.text
        match = re.search(r'^InSight', mars_weather)
        if match:
            mars_weather = mars_weather.replace('\n', ' ')
            break
       
    
    #
    ### Mars Facts
    #

    # Visit Mars Facts webpage for interesting facts about Mars
    physical_facts = 'http://space-facts.com/mars/'
    browser.visit(physical_facts)

    # Use Pandas to scrape the table containing facts about Mars
    mars_physical = pd.read_html(physical_facts)
    mars_physical = mars_physical[1]

    # Reset Index to be description
    mars_physical = mars_physical.set_index('Mars - Earth Comparison')

    # Use Pandas to convert the data to a HTML table string
    mars_physical = mars_physical.to_html(classes="table table-striped")

    #
    ### Mars Hemispheres
    #

    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    mars_hemisphere = []

    # Retrieve all elements that contain image information
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    #
    ### Store Data
    #

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_para,
        "featured_image_url": full_img_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_physical,
        "hemisphere_image_urls": mars_hemisphere
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()