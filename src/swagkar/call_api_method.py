from swagkar.store.method_store import MethodSpecificationStore
from swagkar.store.mongo_connection import MongoConnection
from swagkar.utils import parse_parameters, RequestWrapper
from swagkar.store.api_store import APISpecificationStore
from swagkar import config, logger
from urllib.parse import urlencode
import argparse
import sys


def invoke_service_operation(operation_id, payload=None, parameters=None, headers=None):
    MongoConnection(config['mongo'])

    api_spec_store = APISpecificationStore()
    api_spec = api_spec_store.get_by_operation_id(operation_id)

    method_spec_store = MethodSpecificationStore()
    method_spec = method_spec_store.get_by_operation_id(operation_id=operation_id)
    if not method_spec:
        logger.error(f'operation id -> `{operation_id}` <- does not exist!')
        sys.exit(0)

    logger.info(method_spec)

    parsed_parameters = parse_parameters(parameters)
    absolute_url = f'{api_spec["server_url"]}{method_spec["path"]}'
    logger.info(f'target URL: {absolute_url}')
    logger.info(f'Given parameters: {parsed_parameters}')

    parsed_payload = parse_parameters(payload)
    required_params = filter(lambda x: x['required'], method_spec['parameters'])
    for required_param in required_params:
        if payload is None and parameters is None:
            logger.error(f'parameters and payload is both empty. {required_param} is required!')
            sys.exit(1)

        required_parameter_name = required_param['name']
        if required_parameter_name not in parsed_payload \
                and required_parameter_name not in parsed_parameters:
            logger.error(f'{required_parameter_name} is a required parameter')
            sys.exit(1)

    for p in parsed_parameters:
        # excess given parameters will be ignored
        absolute_url = absolute_url.replace('{{{}}}'.format(p), str(parsed_parameters[p]))

    parsed_headers = parse_parameters(headers)
    logger.info(f'parsed headers: {parsed_headers}')
    logger.info(f'HTTP Method: {method_spec["method"]}')
    if parsed_parameters:
        absolute_url = f'{absolute_url}?{urlencode(parsed_parameters)}'

    logger.debug(f'sending request to [{method_spec["method"]}] {absolute_url}...')
    req_wrapper = RequestWrapper(url=absolute_url,
                                 headers=parsed_headers,
                                 payload=payload)
    res = req_wrapper.call(method_spec['method'])

    return res


def main():  # pylint: disable=W0102
    """
    main function is the entry-point of the call api method
    :return: remote rest api response
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation',
                        required=True,
                        help='OperationId of your desired call')
    parser.add_argument('--parameters',
                        help='parameters used in URL')
    parser.add_argument('--body',
                        help='body content of the request payload')
    parser.add_argument('--headers',
                        help='headers of your request')
    args = parser.parse_args()

    operation_id = args.operation.lower()
    parameters = args.parameters
    payload = args.body
    headers = args.headers

    res = invoke_service_operation(operation_id, payload, parameters, headers)
    logger.info(f'remote service result: {res}')
