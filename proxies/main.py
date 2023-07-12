import requests

# Read the proxy file
with open('proxies.txt', 'r') as file:
    proxies = file.read().splitlines()

# Iterate over each proxy
for proxy_url in proxies:
    proxy = {'http': 'http://' + proxy_url, 'https': 'https://' + proxy_url}

    try:
        # Make a request to Google using the current proxy
        response = requests.get('https://www.laufen.co.at/automatic-category-detail?p_p_id=ProductList_INSTANCE_80H5hgzHtYEp&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&roca_env=3vjR5WgLKZIHLB3Uu8eoUA%3D%3D', proxies=proxy)
        print(f"Proxy: {proxy_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        print("")

    except requests.RequestException as e:
        print(f"Proxy: {proxy_url}")
        print(f"Error: {str(e)}")
        print("")
