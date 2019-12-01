from swagkar.models.api_spec import ApiSpecification
import json


class APISpecificationStore:
    def __init__(self):
        pass

    def save(self, data):
        api_spec = ApiSpecification(
            server_url=data.get('server_url'),
            version=data.get('version'),
            consumes=data.get('consumes'),
            produces=data.get('produces'),
            operations=data.get('operations'),
            title=data.get('title'))
        insert_result = api_spec.save()
        return str(insert_result.pk)

    def get(self, api_id):
        api_doc = ApiSpecification.objects(id=api_id).get()
        api_doc = json.loads(api_doc.to_json())
        return api_doc

    def get_by_operation_id(self, operation_id):
        print(operation_id)
        api_doc = ApiSpecification.objects(operations=operation_id).get()
        api_doc = json.loads(api_doc.to_json())
        return api_doc
