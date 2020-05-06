# coding: utf-8

#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup

#Site Navigation
executable_path = {"executable_path": "/Users/sharonsu/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

def marsNews():
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    html = browser.html
    soup = bs(html, "html.parser")
    slide_element = soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
    output = [news_title, news_p]
    return output

def marsImage():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = bs(html, "html.parser")
    mars_weather = slide_element.find("div", lang_= "en", dir_= "auto", class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()

    return mars_weather

def marsFacts():
    physical_facts = 'http://space-facts.com/mars/'
    browser.visit(physical_facts)
    mars_physical = pd.read_html(physical_facts)
    mars_physical = mars_physical[0]
    mars_html = mars_physical.to_html()
    mars_html = mars_html.replace("\n", "")
    return mars_html

def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    
    return mars_hemisphere 

    

