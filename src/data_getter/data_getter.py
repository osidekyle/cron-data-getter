import pandas as pd
from bs4 import BeautifulSoup
import requests
import boto3
from io import StringIO
from datetime import date

def getData(event, context):
    newsUrls = [["https://rss.nytimes.com/services/xml/rss/nyt/US.xml", "NY Times"]]

    newsDataDictionary = {
        "title": [],
        "description": [],
        "author": [],
        "date": [],
        "link": [],
        "source": [],
        "createdDate": []
    }

    today = date.today()

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
            newsDataDictionary["createdDate"].append(today)

        dataframe = pd.DataFrame.from_dict(newsDataDictionary)
        pd.set_option('display.max_columns', None)

        bucket = "news-data-kvh"
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer)

        s3_resource = boto3.resource("s3")
        s3_resource.Object(bucket, f"{date.today()}.csv").put(Body=csv_buffer.getvalue())