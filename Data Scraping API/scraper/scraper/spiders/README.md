# Scrapy Flask API

Scrapy Flask API is a Python project that demonstrates the integration of Scrapy and Flask to create a seamless workflow for API-based web scraping. Scrapy is a powerful web scraping framework written in Python, while Flask is a lightweight web framework that allows us to create APIs for managing and requesting scraping tasks.

## Setup

1. Install the required packages:

```py
pip install Flask pandas mysql-connector-python scrapy
```


2. Environment Variables:
- Set the following environment variables before running the application:
  ```
  export DB_USERNAME="your_database_username"
  export DB_PASSWORD="your_database_password"
  ```

3. Run the Flask API:

```py
gunicorn -w 4 main:app
```


## Endpoints

- `GET /fetch-data/`: Initiates the Scrapy spider to fetch data from 'https://finance.yahoo.com/lookup'. The scraped data is stored in both a CSV file and a MySQL database. The response will contain a success message.
- `GET /get-all-data/`: Retrieves all the scraped data from the MySQL database and returns it in JSON format.

## Spider

The Scrapy spider, named `MyUniqueSpider`, extracts data from the Yahoo Finance website. It scrapes information from the 'trending-table' and stores it in a pandas DataFrame. The data is then saved to a CSV file named 'scraped_data.csv' and inserted into the MySQL database.

## Database

The `Database` class is responsible for handling the database operations. It connects to the MySQL database using the provided credentials (retrieved from environment variables) and inserts the scraped data into the 'yahoo_records' table.

## Logging

The application uses Python's logging module to log both successful and failed API requests. The log messages are written to the 'api_logs.log' file.
