from mongoengine import Document, StringField, EmbeddedDocumentField, \
    ListField, DynamicEmbeddedDocument
from mongoengine.fields import DateTimeField
import datetime


class Parameters(DynamicEmbeddedDocument):
    path = StringField(required=False)
    name = StringField(required=False)
    description = StringField(required=False)


class MethodSpecification(Document):
    operation_id = StringField(required=True, min_length=3)
    method = StringField(required=False)
    summary = StringField(required=False)
    description = StringField(required=False)
    path = StringField(required=False)
    produces = ListField(field=StringField(required=False), required=False)
    parameters = ListField(field=EmbeddedDocumentField(Parameters, required=False), required=False)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
