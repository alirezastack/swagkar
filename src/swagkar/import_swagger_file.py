from swagkar.store.method_store import MethodSpecificationStore
from swagkar.store.mongo_connection import MongoConnection
from swagkar.store.api_store import APISpecificationStore
from swagger_parser import SwaggerParser
from swagkar import config, logger
import sys
import os


def import_file(file_path):
    # TODO read swagger from URL too
    sp = SwaggerParser(swagger_path=file_path)
    assert len(sp.specification['schemes']) > 0, "scheme property is mandatory"

    MongoConnection(config['mongo'])
    api_spec_store = APISpecificationStore()
    method_spec_store = MethodSpecificationStore()

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

    out = api_spec_store.save({
        'server_url': base_server_url,
        'title': spec_info.get('title'),
        'version': spec_info.get('version'),
        'consumes': sp.specification.get('consumes'),
        'produces': sp.specification.get('produces'),
        'operations': sp.operation.keys()
    })
    logger.info(f'api spec document has been saved {out}')

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
            'summary': operation_sub_method[part[1]].get('summary'),
            'description': operation_sub_method[part[1]].get('description'),
            'produces': operation_sub_method[part[1]].get('produces'),
            'parameters': operation_sub_method.get('parameters'),
        })
        logger.info(f'method document has been saved {out}')


def usage(argv):
    """Print script usage."""
    cmd = os.path.basename(argv[0])
    s = """
    Usage: {prog} your_swagger_file_path.yml

    `your_swagger_file_path.yml` is a valid YAML file format containing Swagger API Spec

    Examples:
        {prog} snapproom_api_spec.yml

    If valid, all paths and its corresponding methods will be imported into MongoDB database for future usage.
    """.format(prog=cmd)
    logger.error(s)


def main(argv=sys.argv):  # pylint: disable=W0102
    """Script entrypoint."""
    if len(argv) < 2:
        usage(argv)
        sys.exit(1)

    swagger_file_path = sys.argv[1]
    import_file(swagger_file_path)
