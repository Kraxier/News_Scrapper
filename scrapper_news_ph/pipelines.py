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

# Before Importing i need to install the mysql connector thing 
# activate the venv news_venv\Scripts\activate
# pip install mysql-connector-python
# 
import mysql.connector

# Setting u 
class SaveToMySQLPipeline:
    '''
    def _init_(self) # What is this 
    self.conn = mysql.connector.connect( # Something more like a connection
            host = 'localhost', # name of the Laptop
            user = 'root', # Name of the User  
            password = '05242005#Kr_031225', # password of the Database
            database = 'mydb' # Name of the Data Base 

    '''
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '05242005#Kr_031225',
            database = 'mydb'
        )
        ## No Idea What this Mean is 
        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        '''
        Explanation : 
            * self.cur = self.conn.cursor() creates a cursor object (self.cur) from a database connection (self.conn).
            * A cursor lets you execute SQL queries (like SELECT, INSERT) and fetch results from MySQL.
            * self.conn = Active database connection (from mysql.connector.connect()).
            * self.cur = Tool to run SQL commands.
            # Basically in the Sense of Run any SQL command. in the VSCODE 
            # You can even run it in VS code the Mysql Part for Proper Fixing Things 


        '''
        ## Create books table if none exists

        # Learning the Data Itself Man 

        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS books(
        #     id int NOT NULL auto_increment, 
        #     url VARCHAR(255),
        #     title text,
        #     upc VARCHAR(255),
        #     product_type VARCHAR(255),
        #     price_excl_tax DECIMAL,
        #     price_incl_tax DECIMAL,
        #     tax DECIMAL,
        #     price DECIMAL,
        #     availability INTEGER,
        #     num_reviews INTEGER,
        #     stars INTEGER,
        #     category VARCHAR(255),
        #     description text,
        #     PRIMARY KEY (id)
        # )
        # """)
            

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