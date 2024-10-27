# import scrapy
# import json
# import os
# from emoji import emoji_bank

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = ['http://quotes.toscrape.com']

#     def __init__(self):
#         self.quotes = []  

#     def parse(self, response):
#         quotes = response.css('div.quote')
#         for quote in quotes:
#             self.quotes.append({
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('small.author::text').get(),
#                 'tags': quote.css('div.tags a.tag::text').getall(),
#             })

#         next_page = response.css('li.next a::attr(href)').get()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse)

#     def close(self, reason):
#         self.save_data()

#     def save_data(self):
#         print("Збереження...")
        
    
#         if not os.path.exists('data'):
#             os.makedirs('data')

       
#         with open('data/quotes.json', 'w', encoding='utf-8') as f:
#             json.dump(self.quotes, f, ensure_ascii=False, indent=4)
            
#         authors_data = {}
#         for quote in self.quotes:
#             author = quote['author']
#             if author not in authors_data:
#                 authors_data[author] = {
#                     'name': author,
#                     'quotes': []
#                 }
#             authors_data[author]['quotes'].append(quote['text'])

#         with open('data/authors.json', 'w', encoding='utf-8') as f:
#             json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=4)

#         print(f"\n{emoji_bank.get_emoji(2)} Створено два файли : data/quotes.json і data/authors.json!\n")
        
        
        
        
        
        
        
        
import scrapy
import json
import os
from emoji import emojize

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
                'author': {
                    'fullname': author_name,
                    'born_date': None,  
                    'born_location': None,  
                    'description': None  
                }
            })

            if author_name not in self.authors_data:
                self.authors_data[author_name] = {
                    'fullname': author_name,
                    'born_date': None,  
                    'born_location': None, 
                    'description': None  
                }

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

        authors_list = []
        for author, details in self.authors_data.items():
            authors_list.append({
                'fullname': details['fullname'],
                'born_date': details['born_date'],
                'born_location': details['born_location'],
                'description': details['description']
            })

        with open('data/authors.json', 'w', encoding='utf-8') as f:
            json.dump(authors_list, f, ensure_ascii=False, indent=4)

        print(f"\n{emojize(':clap:')} Створено два файли: data/quotes.json і data/authors.json!\n")
