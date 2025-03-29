# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface THE DEFUALT CODE OF PIPEline
# from itemadapter import ItemAdapter


# class ScrapperNewsPhPipeline:
#     def process_item(self, item, spider):
#         return item

    # def __init__(self):
    #     self.conn = mysql.connector.connect(
    #         host='localhost',
    #         user='root',
    #         password=os.getenv('05242005#Kr_031225'),  
    #         database='mydb'
    #     )

    #     self.cur = self.conn.cursor()

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import os

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

class SaveToMySQLPipeline:
    def open_spider(self, spider):
        """Connect to MySQL when the spider opens."""
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD", "05242005#Kr_031225"),  # Get from env or fallback
            database="mydb"
        )
        self.cursor = self.conn.cursor()

        # Create the news table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Source VARCHAR(255),
                Title VARCHAR(255),
                Date_of_Published VARCHAR(255),
                Article_Link TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        """Insert items into MySQL."""
        self.cursor.execute(""" 
            INSERT INTO news (Source, Title, Date_of_Published, Article_Link)
            VALUES (%s, %s, %s, %s)
        """, (
            item["Source"],
            item["Title"],
            item["Date_of_Published"],
            item["Article_Link"]
        ))
        self.conn.commit()  
        print(f"✅ Saved to MySQL: {item['Title']}")
        return item  

    def close_spider(self, spider):
        """Close the database connection when the spider stops."""
        self.cursor.close()
        self.conn.close()





