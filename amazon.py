from selectorlib import Extractor
import requests 
import json 
from time import sleep
import urllib.parse

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

def fix_url(s):
    s = urllib.parse.unquote(s)
    substring = "url="
    if substring in s:
        index = s.index(substring)
        uri = s[index:]
        s = uri.replace(substring, "https://www.amazon.com")   
    else:
        s = "https://www.amazon.com" + s
    # Add your own affiliate tag here
    url = s + "&tag=cagrisarigo03-20"
    return url


# product_data = []
with open("urls.txt",'r') as urllist, open('output.jsonl','a') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url) 
        if data:
            data["product_url"] = url
            if data["link_to_all_reviews"] is not None:
                print(data["link_to_all_reviews"])
                data["link_to_all_reviews"] = fix_url(data["link_to_all_reviews"])
            if data["number_of_reviews"] is not None:
                data["number_of_reviews"] = data["number_of_reviews"].replace(" ratings", "")
            json.dump(data,outfile)
            outfile.write("\n")
            # sleep(5)