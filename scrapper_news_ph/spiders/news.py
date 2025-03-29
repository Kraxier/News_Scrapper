# news_venv\Scripts\activate
# scrapy crawl news_spider -o march_25_2025_news.json
# scrapy crawl news_spider
# i should crete that automatically get the current date and save it to the current csv files 
# scrapy crawl news_spider -o inquirer_news.json

'''
Finishing up the Project of Scrapping Multiple News Site 

    1. Data Cleaning and Formatting [ DONE ]
    2. Create a Function where it Automatically get the Current Date of the Local System and create a Name for it [ DONE ]
    3. Store this in Mysql Server of Mine [DONE]
    4. Error Handling in Scrapy ( Although it said that it can take care of itself in terms of Error handling )
    


    Learning Things is the Last
    Reflection
    Proper README.md
    Public the newscrapping.py

'''
from scrapper_news_ph.items import ScrapperNewsPhItem
import scrapy
from datetime import date

# Get the Current Date when Saving a File 
current_date = date.today().strftime("%Y-%m-%d") 
json_file = f"{current_date}.json"
csv_file = f"{current_date}.csv"

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = [
        "www.philstar.com",
        "mb.com.ph",
        "www.manilatimes.net",
        # "www.inquirer.net",
        # "*.inquirer.net"
        # "newsinfo.inquirer.net",
        # "globalnation.inquirer.net",
        # "cebudailynews.inquirer.net",
        # "lifestyle.inquirer.net",
        # "pep.inquirer.net"

    ]
    start_urls = [
        "https://www.philstar.com/",
        "https://mb.com.ph/top-articles/most-viewed",  
        "https://mb.com.ph/top-articles/most-shared",  
        "https://www.manilatimes.net/news",
    ]
    
    custom_settings = {
        "FEEDS": {
            json_file: {"format": "json"},
            csv_file: {"format": "csv"},
        }
    }

    def parse(self, response):
        if "philstar.com" in response.url:
            yield from self.parse_philstar(response)
        elif "mb.com.ph" in response.url:
            yield from self.parse_mb(response)
        elif "manilatimes.net" in response.url:
            yield from self.parse_manilatimes(response)
        # elif "inquirer.net" in response.url:
        #     yield from self.parse_inquirer(response)

    def parse_philstar(self, response):
        article_links = response.css('.news_column.latest .ribbon_image a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_philstar,
                                    meta={'article_link': link}
                                  )
    def parse_manilatimes(self, response):
        article_links = response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_manilatimes,
                                    meta={'article_link': link}
                                  )
    # Parsing logic for Manila Bulletin
    def parse_mb(self, response):
        if "most-viewed" in response.url:
            yield from self.parse_mb_site(response)
        elif "most-shared" in response.url:
            yield from self.parse_mb_site(response)

    # Parsing logic for Manila Bulletin - Most Viewed Articles
    def parse_mb_site(self, response):
        article_links = response.css('.mb-font-article-title a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_mb,
                                    meta={'article_link': link}
                                  )
    def parse_article_philstar(self, response):
        item = ScrapperNewsPhItem()
        item['Source'] = 'Philstar'
        item['Title'] = response.css('.article__title h1::text').get()
        item['Author'] = response.css('.article__credits-author-pub a::text').get()
        item['Date_of_Published'] = response.css('.article__date-published::text').get()
        item['Article_Link'] = response.meta['article_link']
        yield item

    def parse_article_manilatimes(self, response):
        item = ScrapperNewsPhItem()
        item['Source'] = 'Manila Times'
        item['Title'] = response.css('.col-1 h1::text').get()
        item['Author'] = response.css('.article-author-name.roboto-a ::text').get()
        item['Date_of_Published'] = response.css('.article-publish-time.roboto-a ::text').get()
        item['Article_Link'] = response.meta['article_link']
        yield item

    def parse_article_mb(self, response):
        item = ScrapperNewsPhItem()
        item['Source'] = 'Manila Bulletin'
        item['Title'] = response.css('h1::text').get()
        item['Author'] = response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
        item['Date_of_Published'] = response.css('.mb-font-article-date::text').get()
        item['Article_Link'] = response.meta['article_link']
        yield item