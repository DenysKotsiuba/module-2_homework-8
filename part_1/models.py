from mongoengine import CASCADE, Document
from mongoengine.fields import DateTimeField, ListField, ReferenceField, StringField


class Author(Document):
    fullname = StringField(max_length=50)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()