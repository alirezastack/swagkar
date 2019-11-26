from swagkar.store.method_store import MethodSpecificationStore
from swagkar.store.mongo_connection import MongoConnection
from swagkar.store.api_store import APISpecificationStore
from swagger_parser import SwaggerParser
from swagkar import config, logger
import argparse
import sys


def import_file(file_path):
    # TODO read swagger from URL too
    sp = SwaggerParser(swagger_path=file_path)
    assert len(sp.specification['schemes']) > 0, "scheme property is mandatory"

    spec_info = sp.specification.get('info', {})

    default_scheme = 'http'
    for scheme in sp.specification['schemes']:
        default_scheme = scheme
        # https is a preferred scheme over http
        if scheme == 'https':
            break

    if not sp.specification.get("host"):
        logger.error(f"host property of {file_path} is a required property!")
        sys.exit(1)

    base_server_url = f'{default_scheme}://{sp.specification["host"]}'

    MongoConnection(config['mongo'])

    api_spec_store = APISpecificationStore()
    out = api_spec_store.save({
        'server_url': base_server_url,
        'title': spec_info.get('title'),
        'version': spec_info.get('version'),
        'consumes': sp.specification.get('consumes'),
        'produces': sp.specification.get('produces'),
        'operations': sp.operation.keys()
    })
    logger.info(f'api spec document has been saved {out}')

    method_spec_store = MethodSpecificationStore()
    for operationId in sp.operation.keys():
        part = sp.operation[operationId]
        logger.debug(part)
        operation_sub_method = sp.specification['paths'][part[0]]
        logger.debug(operation_sub_method)
        logger.info(f'HTTP Method: {part[1]}')
        if 'parameters' in operation_sub_method:
            logger.info(f"Parameters include: {operation_sub_method['parameters']}")

        out = method_spec_store.save({
            'operation_id': operationId,
            'method': part[1],
            'path': part[0],
            'summary': operation_sub_method[part[1]].get('summary'),
            'description': operation_sub_method[part[1]].get('description'),
            'produces': operation_sub_method[part[1]].get('produces'),
            'parameters': operation_sub_method.get('parameters'),
        })
        logger.info(f'method document has been saved {out}')

    sys.exit()


def main():  # pylint: disable=W0102
    """
    main function is the entry-point of the import file method
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--swagger-file',
                        required=True,
                        help='absolute path of your desired swagger file')
    args = parser.parse_args()
    import_file(args.swagger_file)
