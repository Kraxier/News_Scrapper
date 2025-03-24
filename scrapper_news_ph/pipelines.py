# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface THE DEFUALT CODE OF PIPEline
# from itemadapter import ItemAdapter


# class ScrapperNewsPhPipeline:
#     def process_item(self, item, spider):
#         return item

'''
$ from scrapy.exceptions import DropItem
Purpose: A special exception that tells Scrapy to silently discard an item (without crashing the spider).

When to use: When you encounter:

Invalid/missing data

Duplicate items

Low-quality content (e.g., empty fields)
'''


from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ScrapperNewsPhPipeline:
    def __init__(self):
        self.seen_articles = set()  # Track duplicates

    def process_item(self, item, spider):
        # 1. Validate required fields
        if not item.get('Title') or not item.get('Article_Link'):
            raise DropItem(f"Missing title or URL in {item}")

        # 2. Remove duplicates
        article_id = f"{item['Source']}-{item['Article_Link']}"
        if article_id in self.seen_articles:
            raise DropItem(f"Duplicate article: {item['Title']}")
        self.seen_articles.add(article_id)

        # 3. Clean whitespace from text fields
        for field in ['Title', 'Author', 'Date_of_Published']:
            if field in item and item[field]:
                item[field] = item[field].strip()

        return item
    

# def __init__(self):
#     self.seen_articles = set()  # Track duplicates
    '''
Initialization:

When the spider starts, __init__() creates an empty set() (optimized for fast lookups)
    '''

'''
set()
Key Properties

Memory Efficiency	Sets use hashing for O(1) lookups (faster than lists)
Persistence	Only lasts for current spider run (reset when spider restarts)
Uniqueness Guarantee	Same article won't be processed twice in the same run
Thread-Safe	Scrapy pipelines are single-threaded per item
'''