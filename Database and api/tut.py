from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Initialize the Chrome WebDriver in headless mode
driver = webdriver.Chrome(options=options)

product = "laptop"  # Specify the product name here
daraz_url = 'https://www.daraz.pk/catalog/?q={}'.format(product)
print('URL:', daraz_url, '\n')

# Open the Daraz website
driver.get(daraz_url)

# Print the page source
print(driver.page_source)

# Quit the WebDriver
driver.quit()
