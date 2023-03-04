import pandas as pd
from bs4 import BeautifulSoup
import xmltodict
import requests
import json
import newspaper

# keywords = [["theft", "kia"]] #get from the synonym maker

def get_synonym_list(keywords):
    synonym_list = []

    for keyword in keywords:
        url = f'https://www.thesaurus.com/browse/{keyword}'
        r = requests.get(url)
        
        soup = BeautifulSoup(r.content, "html.parser")
        a = soup.find_all('a',{"class" : ["css-1kg1yv8 eh475bn0", "css-1n6g4vv eh475bn0"]})
        synonyms = [word.text for word in a]
        synonyms.append(keyword)
        synonym_list.append(synonyms)
        
    return synonym_list

def get_urls(keywords):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    urls = []

    for keyword in keywords:
        word = "+".join(keyword)
        url = 'https://news.google.com/rss/search?q='+ word +'&hl=en-US&gl=US&ceid=US:en' # crawl through google news   
        r = requests.get(url, headers=headers)
        xml_data = r.content
        dict_data = xmltodict.parse(xml_data)
        json_data = json.dumps(dict_data)
        json_obj = json.loads(json_data)
        # rj = r.json()
        
        for news in json_obj["rss"]["channel"]["item"]:
            urls.append(news["link"])
        # print(news["title"], news["link"])
    return urls

def get_text(urls):  
    text = []
    for url in urls:
        # Extract web data
        url_i = newspaper.Article(url="%s" % (url), language='en')
        url_i.download()
        url_i.parse()

        text.append(url_i.text)
        # Display scrapped data
        # print(len(url_i.text))
        
    return text