import pandas as pd
from bs4 import BeautifulSoup
import requests

def getData(event, context):
    print("Hello world")


    newsUrls = [["https://rss.nytimes.com/services/xml/rss/nyt/US.xml", "NY Times"]]

    newsDataDictionary = {
        "title": [],
        "description": [],
        "author": [],
        "date": [],
        "link": [],
        "source": []
    }

    for [url, source] in newsUrls:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
        articles = soup.find_all("item")
        for article in articles:
            newsDataDictionary["title"].append(article.title.string)
            newsDataDictionary["description"].append(article.description.string)
            try:
                if len(article.find_all("media:credit")) > 0:
                    newsDataDictionary["author"].append(article.find_all("media:credit")[0].string)
                else:
                    newsDataDictionary["author"].append(article.find_all("dc:creator")[0].string)
            except Exception as e:
                newsDataDictionary["author"].append("")
            newsDataDictionary["date"].append(article.pubdate.string)
            newsDataDictionary["link"].append(article.link.string)
            newsDataDictionary["source"].append(source)

        dataframe = pd.DataFrame.from_dict(newsDataDictionary)
        pd.set_option('display.max_columns', None)

        print(dataframe.head(5))


