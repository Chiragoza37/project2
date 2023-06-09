# imported libraries
import scrapy
import re
from scrapy.http import Request

class bbc_scrape(scrapy.Spider):
    name = "bbc"

    start_urls = ['https://www.bbc.com']

    def parse(self, response):
        urls = response.css("a.media__link::attr(href)").getall()
        tags = response.css("a.media__tag::text").getall()
        titles = response.css("a.media__link::text").getall()

        titles = [re.sub(r'\s+', ' ', t.strip()) for t in titles]
       
        for i, (url, tag, title) in enumerate(zip(urls, tags, titles)):
            if not url.startswith("https://"):
                url = "https://www.bbc.com" + url

            yield Request(url, callback=self.parse_article, cb_kwargs={'url': url, 'tag': tag, 'title': title, 'i': i})

    def parse_article(self, response, url, tag, title, i):
        image = response.css("meta[property='og:image']::attr(content)").get()

        yield {
            'number': i,
            'URL': url,
            'Tag': tag,
            'Title': title,
            'Image': image if "live" not in url else "LIVE" 
        }

