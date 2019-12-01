from swagkar.models.method_spec import MethodSpecification
from mongoengine import DoesNotExist
import json


class MethodSpecificationStore:
    def __init__(self):
        pass

    def save(self, data):
        method_spec = MethodSpecification(
            operation_id=data['operation_id'].lower(),
            method=data.get('method'),
            summary=data.get('summary'),
            path=data.get('path'),
            produces=data.get('produces'),
            parameters=data.get('parameters'),
            description=data.get('description'),
        )
        insert_result = method_spec.save()
        return str(insert_result.pk)

    def get(self, method_id):
        raise NotImplementedError(f"{__name__} method not implemented yet!")

    def get_by_operation_id(self, operation_id):
        try:
            api_doc = MethodSpecification.objects(operation_id=operation_id.lower()).first()
            api_doc = json.loads(api_doc.to_json())
            return api_doc
        except DoesNotExist as dne:
            print(dne)
            return None
