import requests
from bs4 import BeautifulSoup

# Melissa
from melissa.config import tts_engine


class BusinessNewsReader(object):
    WORDS = {'news_reader': {'groups': [['business', 'news']]}}

    def news_reader(self, text):
        fixed_url = 'http://profit.ndtv.com/news/latest/'
        news_headlines_list = []
        news_details_list = []
        for i in range(1, 2):
            changing_slug = '/page-' + str(i)
            url = fixed_url + changing_slug
            r = requests.get(url)
            data = r.text

            soup = BeautifulSoup(data, "html.parser")

            for news_headlines in soup.find_all('h2'):
                news_headlines_list.append(news_headlines.get_text())

            del news_headlines_list[-2:]

            for news_details in soup.find_all('p', 'intro'):
                news_details_list.append(news_details.get_text())

        news_headlines_list_small = [
            element.lower().replace(
                "(", "").replace(
                    ")", "").replace(
                        "'", "") for element in news_headlines_list]
        news_details_list_small = [
            element.lower().replace(
                "(", "").replace(
                    ")", "").replace(
                        "'", "") for element in news_details_list]

        news_dictionary = dict(zip(
            news_headlines_list_small, news_details_list_small
        ))
        for key, value in news_dictionary.items():
            tts_engine.speak('Headline, ' + key)
            tts_engine.speak('News, ' + value)
