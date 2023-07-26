# Import the necessary libraries
from yahooSpider import MyUniqueSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Create a Scrapy process
process = CrawlerProcess(get_project_settings())

# Start the spider and retrieve the scraped data
data = process.crawl(MyUniqueSpider)
process.start()

# Print the scraped data
print(data)
