#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup as bs, Tag
from splinter import Browser
import pandas as pd
import datetime as dt
from IPython.display import HTML
import tweepy


#################################################
# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "C:/webdrivers/chromedriver"}
browser = Browser("chrome", **executable_path)


#################################################
# NASA Mars News
#################################################
# NASA Mars News Site Web Scraper Function
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, "html.parser")

    #This code searches the soup object for all <div> tags with the attribute class="content_title" & class="rollover_description_inner".
    #It returns a special Beautiful Soup objects (called "news_title", news_p) containing the search results.
    
    try:
        news_title = soup.find_all('div' , attrs={'class': 'content_title'})
        news_p = soup.find_all('div' , attrs={'class': 'rollover_description_inner'})
    
        # Extract the first records in the page that start with the latest article
        latest_news_title_block = news_title[0]
        latest_news_paragraph_block = news_p[0] 

        # Extract the latest title using find method & slice notation 
        latest_news_title = latest_news_title_block.find('a').text[0:]

        # Extract the latest title using contents method & slice notation
        latest_news_paragraph = latest_news_paragraph_block.contents[0]
    except AttributeError:
        return None, None
    return latest_news_title, latest_news_paragraph


#################################################
# JPL Mars Space Images - Featured Image
#################################################
# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Use Splinter to Go to Site and Click Button "FULL IMAGE" with Class Name full_image
    # <button class="full_image">Full Image</button>
    #full_image_button.click()
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    
    # Using method "is_element_present_by_text" to check the presensce of "More Info" Button and Click It
    #browser.is_element_present_by_text("more info", wait_time=1)
    more_info_page = browser.links.find_by_partial_text("more info")
    more_info_page.click()
    
    # Create BeautifulSoup object parse with 'html.parser'
    html = browser.html
    image_page_soup = bs(html, "html.parser")

    # This code searches the soup object for all <a> tags with the attribute class="lede"
    # It returns a special Beautiful Soup objects (called "top_img_class") containing the principal image.

    try:
        top_img_class = image_page_soup.find('figure' , attrs={'class': 'lede'})
    
        #Extracting PARTIAL img src URL
        partial_featured_image_url = top_img_class.find('img')['src']
    
        #This code searches the soup object for FIRST <div> tags with the attribute class="jpl_logo"
        #It returns a special Beautiful Soup objects (called "featured_jpl_logo_class") containing the principal image.
        featured_jpl_logo_class =  image_page_soup.find('div', attrs={'class': 'jpl_logo'})
    
        # Extracting the href of jpl site (equivalent to domain site URL)
        # Using slice notation to remove the last slash (/)
        domain_jpl_site_url =  featured_jpl_logo_class.find('a')['href'][0:-1]
    except AttributeError:
        return None
    # Create final featured img url 
    featured_image_url = f"https:{domain_jpl_site_url}{partial_featured_image_url}"
    
    return featured_image_url


#################################################
# Mars Weather
#################################################
# Mars Weather Twitter Account Web Scraper
def twitter_weather():
    # Web Scraping din't work for me due to changes in CSS from Twitter page (I always get a null value)
    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler('cWTIICR3wkkw2PmKoP7Azwmjx', 'CHp4fcZMM726OiZY7bPCepfFNZ6zyZSxK2C8QHY7YQWp8dOtv0')
    auth.set_access_token('1223057473151684609-LLUs8DXZavwtonqe4liqQ9IAKq964w', '9IgMyORcmcZeGLcNf5YC01nXWdGGkKE2iO50N6TRdtxP5')


    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "MarsWxReport"
    tweet = api.user_timeline(target_user, count =1)
    mars_weather = ((tweet)[0]['text'])
    return mars_weather



#################################################
# Mars Facts
#################################################
# Mars Facts Web Scraper
def mars_facts():
    # Read with Pandas Mars Facts page using read_html method
    try:
        mars_facts_df = pd.read_html('https://space-facts.com/mars/')
    except BaseException:
        return None
    # Let print the first data frame or table found in Mars Facts page (information required)
    # Let rename columns and remove index 

    mars_planet_profile_df = mars_facts_df[0]
    mars_planet_profile_df.columns=['Metrics', 'Values']

    # Convert previous data frame to a HTML table string
    # Use a Bootstrap nice table template & remove index 

    return mars_planet_profile_df.to_html(classes=['table table-striped'], index=False)
    


#################################################
# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.links.find_by_partial_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# scrape hemisphere Function
def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


#################################################
# Main Web Scraping BotFunction
#################################################
def scrape_all():
    executable_path = {"executable_path": "C:/webdrivers/chromedriver"}
    browser = Browser("chrome", **executable_path)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather()
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())