import pandas as pd
from bs4 import BeautifulSoup
import xmltodict
import requests
import json
import re
import string
import numpy as np
import newspaper
import random

# keywords = [["theft", "kia"]] #get from the synonym maker

import requests
from bs4 import BeautifulSoup

input_keywords = ['theft', 'atm']
word = 'theft'
url = f'https://www.thesaurus.com/browse/{word}'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

synonyms_div = soup.find('ul', {'class': 'css-x6mqrn e1ccqdb60'})#css-1kg1yv8 eh475bn0 css-1wgnrap e1ccqdb60 css-ttoca5 e1ccqdb60
synonyms_list = synonyms_div.find_all('a')
synonyms = [s.text.strip() for s in synonyms_list]#.find_all('a')]

#print(f"Synonyms of {word}: {synonyms}")

def get_synonym_list(input_keywords):
    synonym_dict = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    for keyword in input_keywords:
        url = f'https://www.thesaurus.com/browse/{keyword}'
        r = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(r.content, "html.parser")
        a = soup.find_all('a',{"class" : ["css-1kg1yv8 eh475bn0", "css-1n6g4vv eh475bn0"]})
        synonyms = [word.text for word in a]
        # synonyms.append(keyword)
        synonym_dict[keyword] = synonyms
        
    return synonym_dict

def get_urls(keywords):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    urls = []
    news_count_limit = 10

    # for keyword in keywords:
    word = "+".join(keywords)
    url = 'https://news.google.com/rss/search?q='+ word +'&hl=en-US&gl=US&ceid=US:en' # crawl through google news   
    r = requests.get(url, headers=headers)
    xml_data = r.content
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data)
    json_obj = json.loads(json_data)
    # rj = r.json()
    link_count = 0
    for news in json_obj["rss"]["channel"]["item"]:
        urls.append(news["link"])
        link_count += 1
        if link_count > news_count_limit:
            break
    # print(news["title"], news["link"])
    return urls

def get_text(urls):  
    text = []
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0.774.45 Safari/537.36 Edg/89.0.774.45',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    
    
    for url in urls:
        # Extract web data
        config = newspaper.Config()
        config.browser_user_agent = random.choice(user_agent)
        try:
            url_i = newspaper.Article(url="%s" % (url), language='en', config=config)
            url_i.download()
            url_i.parse()
            # print(url_i)
            text.append({'title': url_i.title,
                         'text': url_i.text})
        except Exception as e:
            print(e)
        # Display scrapped data
        # print(len(url_i.text))
        
    return text

# Import required module


# Assign url
urls = get_urls(input_keywords)
print("urls exctracted")
articles = get_text(urls)
print(articles)
# exit(0)
print("text exctracted")
# urls = ['https://www.geeksforgeeks.org/top-5-open-source-online-machine-learning-environments/',
#         'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjI56vC3MH9AhUP8zgGHbryB0sQvOMEKAB6BAgOEAE&url=https%3A%2F%2Fwww.thehindu.com%2Fnews%2Finternational%2Fquad-foreign-ministers-take-aim-at-russia-and-china%2Farticle66577074.ece&usg=AOvVaw3G125a3AJkzEiMjMpC3Tt_',
#         'https://www.thehindu.com/news/national/better-infrastructure-has-put-remote-indian-villages-on-tourist-map-pm-modi/article66575058.ece',
#         'https://www.thehindu.com/sci-tech/health/avoid-antibiotics-for-seasonal-cold-and-cough-says-indian-medical-association-amid-rising-cases/article66579326.ece',
#         ]

# Extract web data
# articles = []
# for url in urls:
#     article = newspaper.Article(url="%s" % (url), language='en')
#     article.download()
#     article.parse()
#     articles.append({
#         'title': article.title,
#         'text': article.text
#     })

# Display scrapped data
#articles[0]







news_list = articles
keywords_dict = get_synonym_list(input_keywords)
print("synonyms exctracted")
# keywords_dict = {
#     'atm': ['any time money', 'automatic teller machine'],
#     'Machine Learning' : ['ml', 'ai'],
#     'theft': ['robbery', 'steal', 'larceny'],
#     'party': ['political', 'bjp', 'congress']
# }  



def removePunctuations(news_list):
    # if len(news_list) == 1:
    #     news_text = news_list['text']
    #     news_list['text'] = re.sub(r'[^\w\s]', '', news_text)
    #     news_title = news_list['title']
    #     news_list['title'] = re.sub(r'[^\w\s]', '', news_title)
    #     news_list = [news_list]
    # print("len=",len(news_list))
    for i in range(len(news_list)):
        # print(i)
        # print(news_list[1])
        news_text = news_list[i]['text']
        news_list[i]['text'] = re.sub(r'[^\w\s]', '', news_text)
        news_title = news_list[i]['title']
        news_list[i]['title'] = re.sub(r'[^\w\s]', '', news_title)
    
    return news_list


heading_priority = 10
content_priority = 8

priority = list(np.arange(len(keywords_dict))[::-1]+1)


def getScore(words, content_type):
    score = 0
    frequency_map = {}
    for keyword in keywords_dict:
        frequency_map[keyword] = 0

    for i in range(len(words)):
        for j in range(len(keywords_dict)):
            # keyword = list(keywords_dict.keys())[j]
            # lis = [keyword]+keywords_dict[keyword]
            for synonym in keywords_list[j]:
                #print(keywords_list)
                if len(synonym.split(' ')) < 2:
                    if words[i].lower() == synonym.lower():
                        frequency_map[keywords_list[j][0]] = min(threshold, frequency_map[keywords_list[j][0]] + 1)
                else:
                    l = 0
                    index = i
                    while(i < len(words) and l < len(synonym.split(' ')) and words[i].lower() == synonym.split(' ')[l].lower()):
                        i += 1
                        l += 1
                    if(l == len(synonym.split(' '))):
                        frequency_map[keywords_list[j][0]] = min(threshold, frequency_map[keywords_list[j][0]] + 1)
                    else:
                        i = index 
    
    if content_type == 'heading_priority':
        score += heading_priority*sum(list(frequency_map.values()))
    else:
        score += content_priority*sum(list(frequency_map.values()))

    return score


news_list = removePunctuations(news_list)
keywords_list = []
news_scores = []
threshold = 10

for j in range(len(keywords_dict)):
    keyword = list(keywords_dict.keys())[j]
    keywords_list.append([keyword]+keywords_dict[keyword])
    
for news in news_list:
    score = 0
    score += getScore(news['text'].split(' '), 'content_priority')
    score += getScore(news['title'].split(' '), 'heading_priority')   
    news_scores.append(score)

index = news_scores.index(max(news_scores))
# print(news_scores)
print('final')
print(news_list[index])