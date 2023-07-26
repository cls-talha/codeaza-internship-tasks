import scrapy

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

        # Create DataFrame (optional)
        data = {
            'symbol': symbols,
            'name': names,
            'last_price': last_prices,
            'change': changes,
            'change_percentage': change_percentages,
        }
        
        print("INFO : Scraping Yahoo Finance \n\n\n\n\n")
        print(data)
        

if __name__ == "__main__":
    # Import the necessary libraries
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    # Create a Scrapy process
    process = CrawlerProcess(get_project_settings())
    
    # Start the spider
    process.crawl(MyUniqueSpider)
    process.start()
