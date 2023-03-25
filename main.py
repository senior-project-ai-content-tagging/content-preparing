from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

topic_name = 'projects/senior-project-364818/topics/general-backend.submit-web-link'
subscription_name = 'projects/senior-project-364818/subscriptions/general-backend.submit-web-link-sub'
def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, src="th", dest="en")
    return translation.text

def scrap(url: str):
    res = requests.get(url=url)
    contents = res.text
    soup = BeautifulSoup(contents, 'html.parser')

    article_box = soup.find('div', class_="EntryReaderInner")
    title = soup.find('h1', class_="title").text

    paragraphs = article_box.find_all('p')
    text = ""
    for paragraph in paragraphs:
        text += paragraph.get_text().replace("&nbsp", " ")
    print(title)
    print(text)
    # print(translate_text(text))

def callback(message):
    data = message.data.decode('utf-8')
    url = json.loads(data)["url"]
    print(url)
    scrap(url)
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

print("OK")

