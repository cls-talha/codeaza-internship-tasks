import scrapy
import pandas as pd

import mysql.connector as connector
from sqlalchemy import create_engine
import time

import os

class Database:
    def __init__(self, username: str, password: str, database: str) -> None:
        self.username = username
        self.password = password
        self.database = database
        try:
            self.my_database = connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database=self.database
            )
            if self.my_database.is_connected():
                print("[INFO] Connected with database")
        except connector.Error as e:
            print("[INFO] Connection Failed")
            raise ValueError(str(e))

    def insert_data(self, dataframe):
        try:
            self.cursor = self.my_database.cursor()
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            print("Tables:", tables)
            engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@localhost/{self.database}")
            dataframe.to_sql(name='yahoo_records', con=engine, if_exists='replace', index=False)
            self.my_database.commit()
            print("[INFO] Data inserted successfully!")
        except connector.Error as e:
            print("[INFO] Connection Failed")
            raise ValueError(str(e))

    def show_database(self):
        self.cursor = self.my_database.cursor()
        query = "SELECT * FROM yahoo_records"  # Replace yahoo_records with the actual table name
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        result = [dict(zip(columns, record)) for record in records]
        return result

    def __del__(self):
        print("[INFO] Closing database connection")
        self.cursor.close()
        self.my_database.close()


class MyUniqueSpider(scrapy.Spider):
    name = 'scrapyahoo'
    start_urls = ['https://finance.yahoo.com/lookup']

    def parse(self, response):
        # Find the table with the specified class
        table = response.xpath('//table[contains(@class, "trending-table")]')

        # Lists to store data
        symbols = []
        names = []
        last_prices = []
        changes = []
        change_percentages = []

        # Extract data from each row
        for tr in table.xpath('.//tbody/tr'):
            symbols.append(tr.xpath('.//td[1]//a/text()').get())
            names.append(tr.xpath('.//td[2]/text()').get())
            last_prices.append(tr.xpath('.//td[3]/text()').get())
            changes.append(''.join(tr.xpath('.//td[4]//span/text()').getall()))
            change_percentages.append(''.join(tr.xpath('.//td[5]//span/text()').getall()))

        # Add a timestamp to the data
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Create a list of dictionaries representing the data
        data = []
        for i in range(len(symbols)):
            data.append({
                'timestamp': timestamp,
                'symbol': symbols[i],
                'name': names[i],
                'last_price': last_prices[i],
                'change': changes[i],
                'change_percentage': change_percentages[i],
            })

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(data)
        print(df.info())

        # Save the data to a CSV file named 'scraped_data.csv'
        df.to_csv('scraped_data.csv', index=1)
        
        # Store data in the database using the Database class
        db = Database(username=os.environ.get('DB_USERNAME'), password=os.environ.get('DB_PASSWORD'), database="practiceDB")
        db.insert_data(df)

if __name__ == "__main__":
    # Import the necessary libraries
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # Create a Scrapy process
    process = CrawlerProcess(get_project_settings())

    # Start the spider
    process.crawl(MyUniqueSpider)
    process.start()
