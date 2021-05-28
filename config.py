from os import environ
import configparser
from distutils.util import strtobool

CONFIG_SOURCE = strtobool(environ.get('CBLOG_ENV', 'False'))


if CONFIG_SOURCE:
    CBLOG_SA_DB_URI = environ.get('CBLOG_SA_DB_URI')
    CBLOG_FLASK_SECRET = environ.get('CBLOG_FLASK_SECRET', '')
else:
    config = configparser.ConfigParser()
    config.read('config.ini')
    CBLOG_SA_DB_URI = config['database'].get('uri', None)
    CBLOG_FLASK_SECRET = config['flask'].get('secret', '')
