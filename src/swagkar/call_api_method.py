from swagkar.store.method_store import MethodSpecificationStore
from swagkar.store.mongo_connection import MongoConnection
from swagkar.store.api_store import APISpecificationStore
from swagkar.utils import parse_parameters, HttpResult
from swagkar import config, logger
import argparse
import sys
import os


def invoke_service_operation(operation_id, payload=None, parameters=None, headers=None):
    MongoConnection(config['mongo'])

    api_spec_store = APISpecificationStore()
    method_spec_store = MethodSpecificationStore()
    method_spec = method_spec_store.get_by_operation_id(operation_id=operation_id)
    if not method_spec:
        logger.error(f'operation id -> `{operation_id}` <- does not exist!')
        sys.exit(0)

    logger.info(method_spec)
    parsed_parameters = parse_parameters(payload)
    required_params = filter(lambda x: x['required'], method_spec['parameters'])
    for required_param in required_params:
        if not payload or required_param not in parsed_parameters:
            logger.error(f'{required_param} is a required parameter')
            sys.exit(1)

    # TODO call remote api via requests
    # TODO ...

    # TODO fill this class with proper data
    return HttpResult(
        Status=200,
        Body={},
        Headers={}
    )


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

    operation_id = args.operation
    parameters = args.parameters
    payload = args.body
    headers = args.headers

    res = invoke_service_operation(operation_id, payload, parameters, headers)
    logger.info(f'remote service result: {res}')
