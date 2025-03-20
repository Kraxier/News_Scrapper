import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["www.gmanetwork.com"]
    start_urls = ["https://www.gmanetwork.com/news/"]

    def parse(self, response):
        pass

'''
https://www.philstar.com/
https://mb.com.ph/
https://www.gmanetwork.com/news/
https://www.abs-cbn.com/news
https://www.manilatimes.net/
https://www.inquirer.net/
'''


'''
Scrapping HTML 

ABSCBN 

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

2. Second Problem is Checking if wether it is a javascript or html
What is the Other way of Checking a Website and not Downloading it ?
    fetch('https://www.gmanetwork.com/news/topstories/') # javscript Website 

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

'''

'''
fetch('https://www.manilatimes.net/news')
response.css('.item-row.item-row-2.flex-row a::attr(href)').getall()

fetch() # the Article Itself 
    # Big Problem here , maybe this website have anti Web Scrapping Measure of the Links 
    # a Broken link for the Bot 
    # I'm going to Jump from this man 
'''

'''
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

New chat

'''