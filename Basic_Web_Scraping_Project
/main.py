import grequests
import pandas as pd 

url = "https://www.laufen.co.at/automatic-category-detail?p_p_id=ProductList_INSTANCE_80H5hgzHtYEp&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&roca_env=3vjR5WgLKZIHLB3Uu8eoUA%3D%3D"
header = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'Origin': 'https://www.laufen.co.at',
  'Connection': 'keep-alive',
  'Referer': 'https://www.laufen.co.at/produkte/waschtische',
  'Cookie': 'GUEST_LANGUAGE_ID=de_DE; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+11+2023+17%3A16%3A03+GMT%2B0500+(Pakistan+Standard+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=bd1dd69b-cd0c-41c7-8198-d0e367605c38&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0005%3A1%2CC0002%3A1%2CC0003%3A1%2CC0001%3A1&geolocation=%3B&AwaitingReconsent=false; OptanonAlertBoxClosed=2023-07-09T13:50:38.481Z; JSESSIONID=647253078B4F5E8655C8C9145B39699D; LFR_SESSION_STATE_20103=1689077763935; GUEST_LANGUAGE_ID=de_DE; JSESSIONID=3E8CF23D6B23F6AC5D8CBB8AD838B841',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

def get_data(url: str, header: dict) -> list:
    with open("pageload.txt", "r") as myfile:
        data = myfile.read().splitlines()

    data = str(*data)

    payload_lists = []

    for i in range(8):
        new_payload = data.replace(data[-1], str(i+1))
        payload_lists.append(new_payload)

    requests = (grequests.post(url, headers=header, data=payload) for payload in payload_lists)
    responses = grequests.map(requests, size=8)

    product_data = []
    
    for response in responses:
        if response is not None and response.status_code == 200:
            json_data = response.json()
            products = json_data.get("products", [])
            for product in products:
                category_1 = product.get("category1", "")
                category_2 = product.get("category2", "")
                series = product.get("series", "")
                name = product.get("name", "")
                article_number = product.get("code", "")
                length = product.get("dimensions", "").split(" x ")[0].strip() if product.get("dimensions") else ""
                width = product.get("dimensions", "").split(" x ")[1].strip() if product.get("dimensions") else ""
                height = product.get("dimensions", "").split(" x ")[2].strip() if product.get("dimensions") else ""
                color = product.get("name", "")
                product_type = product.get("type", "")
                short_description = product.get("description", "")
                material = ""
                datasheet = ""
                data_3d = ""
                long_description = ""
                main_image = product.get("image", "")
                gallery_image = ""
                product_url = product.get("url", "")

                product_data.append([category_1, category_2, series, name, article_number, length, width, height, color, product_type, short_description, material, datasheet, data_3d, long_description, main_image, gallery_image, product_url])
    
    return product_data

rs = get_data(url=url, header=header)

# Print the extracted data
df = pd.DataFrame(rs, columns=["Category 1", "Category 2", "Series", "Name", "Article Number", "L", "W", "H", "Color", "Type", "Short Description", "Material", "Datasheet", "3D Data", "Long Description", "Main image", "Gallery image", "Product Url"])

# Save the DataFrame to an Excel file
df.to_excel("product_data.xlsx", index=False)