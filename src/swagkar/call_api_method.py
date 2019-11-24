from swagkar import logger
import sys
import os


def call_api_method(operation_id, params=None):
    pass


def usage(argv):
    """Print script usage."""
    cmd = os.path.basename(argv[0])
    s = """
    Usage: {prog} YourOperationId [param1=x&param2=y&...]

    `YourOperationId` is a unique id referring to the method you are willing to call from 3rd-party API.
    In case the specified operation id has parameters include them in front of the operation as mentioned in the usage.
    It is script's responsibility to send params as JSON body, in path or combined.

    Examples:
        {prog} GetRoomById room_id=12

    If valid, remote request will be called and response will be returned
    """.format(prog=cmd)
    logger.error(s)


def main(argv=sys.argv):  # pylint: disable=W0102
    """Script entrypoint."""
    if len(argv) < 2:
        usage(argv)
        sys.exit(1)

    operation_id = sys.argv[1]
    params = argv[2] if len(argv) > 2 else None

    call_api_method(operation_id, params)
