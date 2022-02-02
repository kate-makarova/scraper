import math
import textract
import tempfile

import requests
from bs4 import BeautifulSoup


class OalibScraper:
    per_page = 10
    pages = 0
    number = 0
    count = 0
    base = 'https://www.oalib.com/'
    output_folder = 'oalib-output'
    topics = {
       'linguistics': 'search?type=0&oldType=0&kw=linguistics&searchField=All&__multiselect_searchField=&fromYear=&toYear=&pageNo=1'
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
        links = soup.select('table#paperContent td span a')
        for link in links:
            if self.count < self.number and link.text.strip() == '[PDF]':
                self.extract_text_from_pdf_stream(link.get('href'))
                self.count += 1

    def extract_text_from_pdf_stream(self, url):
        content = requests.get(url).content
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp.write(content)
        temp.close()
        text = textract.process(temp.name)
        text = text.decode("utf8")
        splitted = url.split('=')
        with open(self.output_folder + '/' + splitted[len(splitted)-1]+'.txt', 'w') as file:
            file.write(text)

    def load_article_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.title)


scraper = OalibScraper()
scraper.scrape(1)

