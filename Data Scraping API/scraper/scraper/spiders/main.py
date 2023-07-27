from flask import Flask, jsonify
import logging

from yahooSpider import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import os

app = Flask(__name__)

def crawl_and_fetch_data():
    process = CrawlerProcess(get_project_settings())
    deferred = process.crawl(MyUniqueSpider)
    deferred.addCallback(on_crawl_finished)
    process.start()

def on_crawl_finished(_):
    # Read the scraped data from the CSV file (Scrapy exports data to a CSV)
    df = pd.read_csv('scraped_data.csv')

    # Return JSON response of the scraped data along with the success message
    response_data = {
        'message': '[INFO] Fetched successfully',
        'data': df.to_dict(orient='records')
    }
    return jsonify(response_data)

@app.route('/fetch-data/')
def fetch_data():
    crawl_and_fetch_data()
    logging.info("Data fetched successfully")
    return jsonify({'message': 'Sucessfully Fetched data and stored in the database'})

@app.route('/get-all-data/')
def get_all_data():
    # Fetch all data from the database
    db = Database(username=os.environ.get('DB_USERNAME'), password=os.environ.get('DB_PASSWORD'), database="practiceDB")
    return jsonify(db.show_database())

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    response_data = {
        'error': 'Invalid endpoint',
        'message': 'The requested endpoint does not exist.'
    }
    return jsonify(response_data), 404

if __name__ == "__main__":
    # Set up logging to log both successful and failed API requests
    logging.basicConfig(filename='api_logs.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    app.run()