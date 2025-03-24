# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# Case Sensitive Man 
import scrapy

class ScrapperNewsPhItem(scrapy.Item):
    Source = scrapy.Field()               # Must match exactly
    Title = scrapy.Field()                # Case-sensitive
    Author = scrapy.Field()
    Date_of_Published = scrapy.Field()    # Note the underscore
    Article_Link = scrapy.Field()

