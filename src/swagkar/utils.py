from typing import NamedTuple, Any, Dict
from json import JSONDecodeError
import requests


class RequestWrapper:
    _ALLOWED_METHODS = ['get', 'post', 'put', 'delete', 'patch']

    def __init__(self, url, headers=None, payload=None):
        self.url = url
        self.headers = headers if headers else {}
        self.payload = payload if payload else {}

    def call(self, method):
        assert method in self._ALLOWED_METHODS, \
            f"Invalid method given: {method}"

        res = getattr(requests, method)(url=self.url,
                                        data=self.payload,
                                        headers=self.headers)

        try:
            data = res.json()
        except JSONDecodeError:
            data = {}

        return HttpResult(
            Status=res.status_code,
            Body=data,
            Headers=res.headers
        )


def parse_parameters(params):
    if not params:
        return {}

    parsed_params = {}
    params = map(lambda x: x.split('='), params.split('&'))
    for part in params:
        parsed_params[part[0]] = part[1]

    return parsed_params


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class HttpResult(NamedTuple):
    Status: int
    Body: Any
    Headers: Dict[str, str]
