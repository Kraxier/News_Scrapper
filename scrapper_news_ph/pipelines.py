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


'''

Understanding the Code 
    1. Why it did what it Did 
    2. What things i should implement 
    3. Learning Mysql Thing 

class RelearnScrapyV2Pipeline:
    def process_item(self, item, spider):


        ## Strip all whitespaces from strings
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()


        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()



        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)


        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])



        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)


        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5


        return item
    
# Pipeline you can do it diretcly to data base 

import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '05242005#Kr_031225', #add your password here if you have one set 
            database = 'mydb'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

'''