from connect import client
from models import Author, Quote

from datetime import datetime
import json


def insert_authors():
    with open("authors.json", "r") as file:
        authors = json.load(file)

    for author in authors:
        Author(fullname=author.get("fullname"), 
               born_date=datetime.strptime(author.get("born_date"), "%B %d, %Y").date(), 
               born_location=author.get("born_location"), 
               description=author.get("description")).save()
        

def insert_quotes():
    with open("quotes.json", "r") as file:
        quotes = json.load(file)

    for quote in quotes:
        author = Author.objects(fullname=quote.get("author")).first()
        print(author.born_location)
        """
        Quote(tags=quote.get("tags"),
              author=author,
              quote = quote.get("quote")).save()"""
        

if __name__ == "__main__":
    #insert_authors()
    insert_quotes()