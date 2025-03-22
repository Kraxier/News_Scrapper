# news_venv\Scripts\activate
# scrapy crawl news_spider -o march_23_2025_news.json
# i should crete that automatically get the current date and save it to the current csv files 

'''
I needed to Improve like What Site that currently it extracted like some sort of string thing 
'''

import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = [
        "www.philstar.com",
        "mb.com.ph",
        "www.manilatimes.net",
        "www.inquirer.net"
    ]
    start_urls = [
        "https://www.philstar.com/",
        "https://mb.com.ph/top-articles/most-viewed",  
        "https://mb.com.ph/top-articles/most-shared",  
        "https://www.manilatimes.net/news",
        "https://newsinfo.inquirer.net",
    ]

    def parse(self, response):
        if "philstar.com" in response.url:
            yield from self.parse_philstar(response)
        elif "mb.com.ph" in response.url:
            yield from self.parse_mb(response)
        elif "manilatimes.net" in response.url:
            yield from self.parse_manilatimes(response)
        elif "inquirer.net" in response.url:
            yield from self.parse_inquirer(response)


    def parse_philstar(self, response):
        article_links = response.css('.news_column.latest .ribbon_image a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_philstar,
                                    meta={'article_link': link}
                                  )
    
    def parse_article_philstar(self, response):
        article_link = response.meta['article_link']
        title = response.css('.article__title h1::text').get()
        author = response.css('.article__credits-author-pub a::text').get()
        date_published = response.css('.article__date-published::text').get()
        yield {
        'Source': 'Philstar',
        'Title': title,
        'Author': author,
        'Date_of_Published': date_published,
        'Article_Link': article_link,
        }
        
    def parse_manilatimes(self, response):
        article_links = response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_manilatimes,
                                    meta={'article_link': link}
                                  )

    def parse_article_manilatimes(self, response):
        article_link = response.meta['article_link']
        title = response.css('.col-1 h1::text').get()
        author = response.css('.article-author-name.roboto-a ::text').get()
        date_published = response.css('.article-publish-time.roboto-a ::text').get()
        yield {
        'Source': 'Manila Times',
        'Title': title,
        'Author': author,
        'Date_of_Published': date_published,
        'Article_Link': article_link,
        }
    def parse_inquirer(self, response):
        article_links = response.css('#ncg-info h1 a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, 
                                    callback=self.parse_article_inquirer,
                                    meta={'article_link': link}
                                  )
    def parse_article_inquirer(self, response):
        article_link = response.meta['article_link']
        title = response.css('h1::text').get()
        author = response.css('#art_author a::text').get()
        date_published = response.css('#art_plat ::text').getall()
        yield {
        'Source': 'Incquirer',    
        'Title': title,
        'Author': author,
        'Date_of_Published': date_published,
        'Article_Link': article_link,
        }

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
    def parse_article_mb(self, response):
        article_link = response.meta['article_link']
        title = response.css('h1::text').get()
        author = response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
        date_published = response.css('.mb-font-article-date::text').get()
        yield {
        'Source': 'Manila Bulletin',    
        'Title': title,
        'Author': author,
        'Date_of_Published': date_published,
        'Article_Link': article_link,
        }
            

# Manila Bulletin 
# Link of Article:
# response.css('.mb-font-article-title a::attr(href)').getall()
# Headers of Articles: 
# response.css('h1::text').get()
# Author of Articles:
# response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
# Date of Published Article:
# response.css('.mb-font-article-date::text').get()

# PHILSTAR
# Link of Article:
# response.css('.news_column.latest .ribbon_image a::attr(href)').getall()
# Headers of Articles: 
# response.css('.article__title h1::text').get()
# Author of Articles:
# response.css('.article__credits-author-pub::text').get()
# Date of Published Article:
# response.css('.article__date-published::text').get()

# Manila Times 
# Link of Article:
# response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()
# Headers of Articles: 
# response.css('.col-1 h1::text').get()
# Author of Articles:
# response.css('.article-author-name.roboto-a ::text').get()
# Date of Published Article:
# response.css('.article-publish-time.roboto-a ::text').get()

# Manila Bulletin 
# Link of Article:
# response.css('.mb-font-article-title a::attr(href)').getall()
# Headers of Articles: 
# response.css('h1::text').get()
# Author of Articles:
# response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
# Date of Published Article:
# response.css('.mb-font-article-date::text').get()

# Inquirer.net 
# Link of Article:
# response.css('#ncg-info h1 a::attr(href)').getall()
# Headers of Articles: 
# response.css('h1::text').get()
# Author of Articles:
# response.css('#art_author a::text').get()
# Date of Published Article:
# response.css('#art_plat ::text').getall() # Clean this Part 


'''
Scrapping HTML 

ABSCBN [Protected]
GMA News 
Inquirer 
Manila Bulletin 
Manila Times 
Philstar
'''

'''
Reflection 
1. Opening a Scrapy Shell 
# how i can Fetch something ignoring the Robot

ABSCBN is the Problem # Let's think about this later

I think the Problem the i currently Facing is there are to many sites
i should focus on things 
    * Focus on the Latest News [Breaking News, Latest Updates]
    * Scrape only 20 - 50 Articles per Website?
    * What Specific News or Niche?
        What i'm Currently Interested? [Sports,Politics,Technology]
            [Nation News, and Politics]
    * Trending Article or Most Read Articles

# Even having a User Agent and Ignoring the Robot.txt it freaking stop me from Javscript
_________________________________________________________________


2. Second Problem is Checking if wether it is a javascript or html
What is the Other way of Checking a Website and not Downloading it ?
    fetch('https://www.gmanetwork.com/news/topstories/') # javscript Website 

    # Yep It's definitely Javascript Website Man 


'''


'''
fetch('https://www.philstar.com/')
response.css('.news_column.latest .ribbon_image a::attr(href)').getall()

fetch('') # Fetch the Article itself 
In [2]: response.css('.article__title h1::text').get()
Out[2]: "No grand conspiracy in Duterte's arrest – Año"

2025-03-21 05:11:24 [asyncio] DEBUG: Using selector: SelectSelector
In [3]: response.css('.article__credits-author-pub::text').get()
Out[3]: ' - The Philippine Star'

2025-03-21 05:12:13 [asyncio] DEBUG: Using selector: SelectSelector
In [4]: response.css('.article__credits-author-pub a::text').get()
Out[4]: 'Marc Jayson Cayabyab'

2025-03-21 05:12:34 [asyncio] DEBUG: Using selector: SelectSelector
In [5]: response.css('.article__date-published::text').get()
Out[5]: 'March 21, 2025 | 12:00am'

# PHILSTAR
# Link of Article:
response.css('.news_column.latest .ribbon_image a::attr(href)').getall()
Headers of Articles: 
response.css('.article__title h1::text').get()
Author of Articles:
response.css('.article__credits-author-pub::text').get()
Date of Published Article:
response.css('.article__date-published::text').get()
'''

'''
fetch('https://www.manilatimes.net/news')
response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()

response.css('.col-1 h1::text').get()
2025-03-22 04:31:04 [asyncio] DEBUG: Using selector: SelectSelector
In [3]: response.css('.col-1 h1::text').get()
Out[3]: '\n                ICC credibility could come under scrutiny\n            '

2025-03-22 04:31:24 [asyncio] DEBUG: Using selector: SelectSelector
In [4]: response.css('.article-author-name.roboto-a ::text').get()
Out[4]: '\n                                By Franco Jose C. Baroña\n                            '

2025-03-22 04:32:12 [asyncio] DEBUG: Using selector: SelectSelector
In [5]: response.css('.article-publish-time.roboto-a ::text').get()
Out[5]: '\n                                March 22, 2025\n                            '

# Manila Times 
Link of Article:
response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()
Headers of Articles: 
response.css('.col-1 h1::text').get()
Author of Articles:
response.css('.article-author-name.roboto-a ::text').get()
Date of Published Article:
response.css('.article-publish-time.roboto-a ::text').get()

'''

'''

Manila Bulletin [DONE]

https://mb.com.ph/top-articles/most-viewed
response.css('.mb-font-article-title a::attr(href)').getall()

https://mb.com.ph/top-articles/most-shared
response.css('.mb-font-article-title a::attr(href)').getall()

# Scrapping the ARticle Itself 
In [2]: response.css('h1::text').get()
Out[2]: 'Paolo Tantoco of Rustan Commercial Corp. has passed away'

In [8]: response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
Out[8]: 'John Legaspi'

In [9]: response.css('.mb-font-article-date::text').get()
Out[9]: 'Mar 9, 2025 06:08 AM'


Link of Article:
response.css('.mb-font-article-title a::attr(href)').getall()
Headers of Articles: 
response.css('h1::text').get()
Author of Articles:
response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
Date of Published Article:
response.css('.mb-font-article-date::text').get()
_________________________________________________

The reason why response.css('.mb-font-author-name.overflow-nowrap a span::text').get() works is because it accurately targets the specific HTML structure of the webpage you're scraping. Let me break it down for you:

1. Understanding the Selector
The selector .mb-font-author-name.overflow-nowrap a span::text can be broken down as follows:

.mb-font-author-name.overflow-nowrap: Targets an element with both classes mb-font-author-name and overflow-nowrap.

a: Targets an <a> tag that is a descendant of the above element.

span::text: Targets the text inside a <span> tag that is a child of the <a> tag.

This selector works because the author name ("John Legaspi") is likely nested inside a <span> within an <a> tag, which itself is inside an element with the classes mb-font-author-name and overflow-nowrap.

2. Why Other Selectors Didn't Work
Here’s why the other selectors you tried might have failed:

a. Selector: .mb-font-author-name.overflow-nowrap a::text
This selector targets the text directly inside the <a> tag.

If the author name is inside a <span> within the <a> tag (e.g., <a><span>John Legaspi</span></a>), this selector won't work because it doesn't account for the nested <span>.

b. Selector: .mb-font-author-name.overflow-nowrap span a::text
This selector assumes that the <a> tag is inside a <span>, which is not the case in your HTML structure.

In your case, the <span> is inside the <a> tag, not the other way around.

c. Selector: custom-text-link.uppercase.author-name-link.pb-0.mt-1
This selector is incorrect because it doesn't start with a . (for class) or # (for ID). It also doesn't target the text node.

3. Why This Selector Works
The selector .mb-font-author-name.overflow-nowrap a span::text works because:

It correctly navigates the HTML structure:

html
Copy
<div class="mb-font-author-name overflow-nowrap">
    <a href="/author/johnlegaspi">
        <span>John Legaspi</span>
    </a>
</div>
Run HTML
It targets the <span> inside the <a> tag, which contains the author name.

4. Key Takeaway
When writing CSS selectors for web scraping:

Inspect the HTML structure carefully: Use your browser's developer tools (right-click → Inspect) to see the exact nesting of elements.

Target the correct text node: If the text is inside a nested element (e.g., a <span>), include that element in your selector.

Test and debug: Use .extract() to see all matching elements and refine your selector accordingly.

5. Example Workflow
Here’s how you can debug and confirm the correct selector:

python
Copy
# Print the HTML to inspect the structure
print(response.text)

# Try the working selector
author_name = response.css('.mb-font-author-name.overflow-nowrap a span::text').get()
print("Author Name:", author_name)

# Extract all matching elements for debugging
all_matching_elements = response.css('.mb-font-author-name.overflow-nowrap a span::text').extract()
print("All Matching Elements:", all_matching_elements)
If you have further questions or need help with other parts of your scraping project, feel free to ask! 😊


'''

'''
# GMA Network 

In [1]: fetch('https://www.gmanetwork.com/news/archives/topstories/')
2025-03-22 03:52:43 [scrapy.core.engine] INFO: Spider opened
2025-03-22 03:52:43 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.gmanetwork.com/robots.txt> (referer: None)
2025-03-22 03:52:43 [scrapy.downloadermiddlewares.robotstxt] DEBUG: Forbidden by robots.txt: <GET https://www.gmanetwork.com/news/archives/topstories/>
'''

'''
Inquirer.net
In [1]: fetch('https://newsinfo.inquirer.net/')
2025-03-22 04:05:02 [scrapy.core.engine] INFO: Spider opened
2025-03-22 04:05:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://newsinfo.inquirer.net/robots.txt> (referer: None)
2025-03-22 04:05:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://newsinfo.inquirer.net/> (referer: None)


2025-03-22 04:05:56 [asyncio] DEBUG: Using selector: SelectSelector
In [3]: response.css('#ncg-info h1 a::attr(href)').getall()

# Inquirer.net 
Link of Article:
response.css('#ncg-info h1 a::attr(href)').getall()
Headers of Articles: 
response.css('h1::text').get()
Author of Articles:
response.css('#art_author a::text').get()
Date of Published Article:
response.css('#art_plat ::text').getall() # Clean this Part 

Collect all the Possible Node in this HTML instead of .get()

<div id="art_plat"> 
    <a href="https://newsinfo.inquirer.net/source/inquirer-net" rel="tag">INQUIRER.net</a> / 10:23 PM March 21, 2025
</div>

'''



'''
Focusing on What Currently MAtter man 
'''
