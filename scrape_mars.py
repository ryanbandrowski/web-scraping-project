def scrape():
    # import dependencies
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser


    ### NASA Mars News
    # get the url, retrieve the page with the requests module, and create BeautifulSoup object
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # find the news article title and save to a variable: news_title
    news_title = soup.find('div', class_='content_title').a.text.strip()

    # find the news article teaser text and save to a variable: news_p
    news_p = soup.find('div', class_='image_and_description_container').div.text.strip()


    ### JPL Mars Space Images - Featured Image
    # setup Splinter
    executable_path = {'executable_path': 'C:/Users/ryban/Anaconda3/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # open website and navigate to the page containing the featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_not_present_by_text('more info', wait_time=1)
    browser.click_link_by_partial_text('more info')

    # scrape the html for the url for the large-size image and save to a variable: featured_image_url
    html = browser.html
    soup = bs(html, 'html.parser')
    img_link = soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov'+img_link


    ### Mars Weather
    # get the url, retrieve the page with the requests module, and create BeautifulSoup object
    url = 'https://twitter.com/MarsWxReport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # find the text for the latest tweet and save to a variable: mars_weather
    pic_a_tag = soup.find('p', class_='TweetTextSize').a.decompose()
    mars_weather = soup.find('p', class_='TweetTextSize').text


    ### Mars Facts
    # url for Mars Facts webpage
    url = 'https://space-facts.com/mars/'

    # read html table and store to a variable
    facts = pd.read_html(url)

    # save the desired table to a dataframe and name the columns
    facts_df = facts[1]
    facts_df.columns=['description','value']
    facts_df = facts_df.set_index('description')

    # write the dataframe to an html table string
    facts_table = facts_df.to_html()


    ### Mars Hemispheres
    # get the url, retrieve the page with the requests module, and create BeautifulSoup object
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # create list of sections containing images and store to a variable: image_items
    image_items = soup.find_all('div',class_='item')

    # initialze list to store image title and url dictionaries
    hemisphere_image_urls = []

    # loop through the items and append the image title and url to the list as a dictionary
    for item in image_items:
        img_title = item.h3.text    
        img_link = 'https://astrogeology.usgs.gov'+item.a['href']
        browser.visit(img_link)
        img_url = browser.find_link_by_text('Sample')['href']
        hemisphere_image_urls.append({'title':img_title,'img_url':img_url})
    browser.quit()

    # store all scraped data to a dictionary
    scraped_data = {'news_title':news_title,'news_p':news_p,'featured_image_url':featured_image_url,
                'mars_weather':mars_weather,'facts_table':facts_table,
                'hemisphere_image_urls':hemisphere_image_urls}
    
    return scraped_data
