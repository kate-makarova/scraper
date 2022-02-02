import math
import textract
import tempfile

import requests
from bs4 import BeautifulSoup


class LeninkaScraper:
    per_page = 20
    pages = 0
    number = 0
    count = 0
    base = 'https://cyberleninka.ru'
    output_folder = 'leninka-output'
    topics = {
       'linguistics': '/article/c/languages-and-literature/'
    }

    def scrape(self, number):
        self.number = number
        self.pages = math.ceil(number / self.per_page)
        for i in range(1, self.pages+1):
            url = self.base + self.topics['linguistics'] + str(i)
            self.load_list_page(url)

    def load_list_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('div.main ul.list li a')
        for article in articles:
            if self.count < self.number:
                self.extract_text_from_pdf_stream(article.get('href'))
                self.count += 1

    def extract_text_from_pdf_stream(self, url):
        content = requests.get(self.base + url+'/pdf').content
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp.write(content)
        temp.close()
        text = textract.process(temp.name)
        text = text.decode("utf8")
        splitted = url.split('/')
        with open(self.output_folder + '/' + splitted[len(splitted)-1]+'.txt', 'w') as file:
            file.write(text)

    def load_article_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.title)


scraper = LeninkaScraper()
scraper.scrape(1)

