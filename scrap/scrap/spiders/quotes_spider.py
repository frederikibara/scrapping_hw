import scrapy
import json
import os

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        self.quotes = []  

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            self.quotes.append({
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            })

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def close(self, reason):
        self.save_data()

    def save_data(self):
        print("Збереження...")
        
    
        if not os.path.exists('data'):
            os.makedirs('data')

       
        with open('data/quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)
            
        authors_data = {}
        for quote in self.quotes:
            author = quote['author']
            if author not in authors_data:
                authors_data[author] = {
                    'name': author,
                    'quotes': []
                }
            authors_data[author]['quotes'].append(quote['text'])

        with open('data/authors.json', 'w', encoding='utf-8') as f:
            json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=4)

        print("Все ок! Створено два файли : data/quotes.json і data/authors.json!")
