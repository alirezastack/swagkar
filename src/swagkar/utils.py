from typing import NamedTuple, Any, Dict


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
