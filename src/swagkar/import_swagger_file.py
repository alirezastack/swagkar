from swagkar import logger
import sys
import os


def import_file(file_path):
    pass


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
