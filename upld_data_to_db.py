import json
from pymongo import MongoClient
from emoji import emoji_bank

client = MongoClient("mongodb+srv://fredderf:fred555@cluster0.a03do.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['scrap_db']

with open('data/quotes.json', 'r', encoding='utf-8') as quotes_file:
    quotes = json.load(quotes_file)
    db.quotes.insert_many(quotes)  

with open('data/authors.json', 'r', encoding='utf-8') as authors_file:
    authors = json.load(authors_file)
    db.authors.insert_many(authors)  

print(f"\n{emoji_bank.get_emoji(2)} Все відмінно завантажено у MongoDB!\n")


