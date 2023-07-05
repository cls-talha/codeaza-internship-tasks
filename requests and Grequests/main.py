from gevent import monkey

monkey.patch_all(thread=False, select=False)

import requests
import grequests
from bs4 import BeautifulSoup
class WebScraper:
    def __init__(self, urls):
        self.urls = urls
        self.responses = []

    def fetch_titles(self):
        # Create a list of grequests.get() calls for each URL
        requests = (grequests.get(url) for url in self.urls)

        # Send the requests asynchronously
        self.responses = grequests.map(requests)

    def print_titles(self):
        for response in self.responses:
            if response is not None:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                if title:
                    print(title.text)


# Main program
if __name__ == '__main__':
    # URLs to scrape
    urls = ['https://www.tutorialspoint.com',
            'https://www.google.com',
            'https://www.openai.com']

    # Create an instance of WebScraper
    scraper = WebScraper(urls)

    # Fetch the titles asynchronously
    scraper.fetch_titles()

    # Print the titles
    scraper.print_titles()
