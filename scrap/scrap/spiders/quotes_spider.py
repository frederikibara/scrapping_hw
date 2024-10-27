import scrapy
import json
import os
from emoji import emoji_bank

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        self.quotes = []  
        self.authors_data = {}

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            author_name = quote.css('small.author::text').get()
            author_url = quote.css('small.author ~ a::attr(href)').get()

            self.quotes.append({
                'text': quote.css('span.text::text').get(),
                'author': author_name  
            })

            if author_url and author_name not in self.authors_data:

                yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_name = response.css('h3.author-title::text').get().strip()
        born_date = response.css('span.author-born-date::text').get()
        born_location = response.css('span.author-born-location::text').get()
        description = response.css('div.author-description::text').get().strip()

        self.authors_data[author_name] = {
            'fullname': author_name,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }

    def close(self, reason):
        self.save_data()

    def save_data(self):
        print("Збереження...")

        if not os.path.exists('data'):
            os.makedirs('data')

        with open('data/quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)

        authors_list = list(self.authors_data.values())

        with open('data/authors.json', 'w', encoding='utf-8') as f:
            json.dump(authors_list, f, ensure_ascii=False, indent=4)

        print(f"\n{emoji_bank.get_emoji(2)} Створено два файли : data/quotes.json і data/authors.json!\n")