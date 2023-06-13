from mongoengine import Document
from mongoengine.fields import BooleanField, EmailField, StringField


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    email = EmailField()
    send_status = BooleanField(default=False)