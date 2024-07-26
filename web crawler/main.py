import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Crawler:

    def __init__(self, urls=[]):
        self.visitedUrls = []
        self.urlsToVisit = urls
        self.bookData = []

    def getUrl(self, url):
        response = requests.get(url)
        return response
    
    def getLinks(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            # print(f"Title: {title}, Price: {price}")
            try:
                print(f"Title: {title.encode('utf-8').decode('utf-8')}, Price: {price.encode('utf-8').decode('utf-8')}")
            except UnicodeEncodeError as e:
                print(f"Error encoding: {e}")

        links = soup.findAll('a')
        for link in links:
            path = link.get('href')
            if path:
                absolute_url = urljoin(url, path)
                #print(path, "and", url)
            if absolute_url not in self.visitedUrls and absolute_url not in self.urlsToVisit:
                self.urlsToVisit.append(absolute_url)

    def getBookDetails(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1').text if soup.find('h1') else 'No title'
        price = soup.find('p', class_='price_color').text if soup.find('p', class_='price_color') else 'No price'
        self.bookData.append({
            'title': title,
            'price': price,
            'url': url
        })

    def crawl(self):
        while self.urlsToVisit:
            url = self.urlsToVisit.pop(0)
            if url not in self.visitedUrls:
                print(f"Crawling: {url}")
                response = self.getUrl(url)
                if response and response.status_code == 200:
                    self.visitedUrls.append(url)
                    self.getLinks(url, response.text)

if __name__ == '__main__':
    initial_urls = ["https://books.toscrape.com/"]
    crawler = Crawler(urls=initial_urls).crawl()
    
   