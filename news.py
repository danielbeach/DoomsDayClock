import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime
import os

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run():
    urls = ['http://www.cnn.com',
            'http://www.foxnews.com',
            'http://www.nbcnews.com',
            'http://www.abcnews.com',
            'http://www.usatoday.com/news',
            'https://www.bbc.com/news/world']
    tasks = []

    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


def get_response_text(response):
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        page = soup.find().getText()
        return page

def get_sentiment(text):
    opinion = TextBlob(text)
    return opinion.sentiment[0] #polarity 1 very postive, -1 negative


if __name__ == '__main__':
    date = datetime.now()
    cwd = os.getcwd()
    filename = 'news-{year}-{month}-{day}-{minute}'.format(year=date.year, month=date.month, day=date.day, minute=date.minute)
    file = open("{cwd}/doomsday/{file_name}.txt".format(cwd=cwd, file_name=filename), "w")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    responses = loop.run_until_complete(future)
    setiment_list = []
    for response in responses:
        text = get_response_text(response)
        output = get_sentiment(text)
        setiment_list.append(output)
    for setiment in setiment_list:
        file.write(str(setiment) + ' \n')
    file.close()
