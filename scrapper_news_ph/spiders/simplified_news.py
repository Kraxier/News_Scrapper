# Simplifed Version of News
'''
I had no Idea how this Work but it Work 
# DRY ( Don't Repeat Yourself ) Principles 
# Your SITE_CONFIG approach is industry-standard for multi-site scrapers. It’s used by:
'''

# class NewsSpider(scrapy.Spider):
#     name = "news_spider"
#     allowed_domains = [
#         "www.philstar.com",
#         "mb.com.ph",
#         "www.manilatimes.net",
#         # "www.inquirer.net",
#     ]
    
#     start_urls = [
#         "https://www.philstar.com/",
#         "https://mb.com.ph/top-articles/most-viewed",
#         "https://mb.com.ph/top-articles/most-shared",
#         "https://www.manilatimes.net/news",
#     ]

#     # Configuration for each site's selectors and parsing rules
#     SITE_CONFIG = {
#         'philstar.com': {
#             'article_links': '.news_column.latest .ribbon_image a::attr(href)',
#             'article_parser': {
#                 'title': '.article__title h1::text',
#                 'author': '.article__credits-author-pub a::text',
#                 'date': '.article__date-published::text',
#                 'source': 'Philstar'
#             }
#         },
#         'manilatimes.net': {
#             'article_links': '.item-row.item-row-2.flex-row a::attr(href)',
#             'article_parser': {
#                 'title': '.col-1 h1::text',
#                 'author': '.article-author-name.roboto-a ::text',
#                 'date': '.article-publish-time.roboto-a ::text',
#                 'source': 'Manila Times'
#             }
#         },
#         'mb.com.ph': {
#             'article_links': '.mb-font-article-title a::attr(href)',
#             'article_parser': {
#                 'title': 'h1::text',
#                 'author': '.mb-font-author-name.overflow-nowrap a span::text',
#                 'date': '.mb-font-article-date::text',
#                 'source': 'Manila Bulletin'
#             },
#             'special_pages': ['most-viewed', 'most-shared']
#         },
#         # 'inquirer.net': {
#         #     'article_links': '#ncg-info h1 a::attr(href)',
#         #     'article_parser': {
#         #         'title': 'h1::text',
#         #         'author': '#art_author a::text',
#         #         'date': '#art_plat ::text',
#         #         'source': 'Inquirer'
#         #     }
#         # }
#     }

#     def parse(self, response):
#         """Main parse method that routes to appropriate handler"""
#         domain = self._get_domain(response.url)
#         if domain in self.SITE_CONFIG:
#             yield from self._parse_article_list(response, domain)

#     def _get_domain(self, url):
#         """Extract the domain from URL"""
#         for domain in self.SITE_CONFIG:
#             if domain in url:
#                 return domain
#         return None

#     def _parse_article_list(self, response, domain):
#         """Parse list of articles for a specific domain"""
#         config = self.SITE_CONFIG[domain]
#         article_links = response.css(config['article_links']).getall()
        
#         for link in article_links:
#             yield response.follow(
#                 link,
#                 callback=self._parse_article,
#                 meta={'domain': domain}
#             )

#     def _parse_article(self, response):
#         """Parse individual article page"""
#         domain = response.meta['domain']
#         config = self.SITE_CONFIG[domain]['article_parser']
        
#         article_data = {
#             'Source': config['source'],
#             'Title': response.css(config['title']).get(),
#             'Author': response.css(config['author']).get(),
#             'Date_of_Published': response.css(config['date']).get(),
#             'Article_Link': response.url
#         }

#         if article_data['Title']:  # Only yield items with titles
#             yield article_data