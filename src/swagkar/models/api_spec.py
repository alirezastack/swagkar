from mongoengine import Document, StringField, ListField
from mongoengine.fields import DateTimeField
import datetime


class ApiSpecification(Document):
    server_url = StringField(required=True, min_length=3)
    title = StringField(required=False)
    version = StringField(required=False)
    consumes = ListField(field=StringField(required=False), required=False)
    produces = ListField(field=StringField(required=False), required=False)
    operations = ListField(field=StringField(required=False), required=False)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
