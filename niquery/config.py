import os


class Config(object):
    """
    Default configuration
    """
    # Flask Configuration
    DEBUG = False
    PORT = 5000
    HOST = '0.0.0.0'
    URL_PREFIX = '/api'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    #TEMPLATE_FOLDER = path.join(PROJECT_ROOT, 'templates')

    # Celery Configuration
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
    CELERYD_POOL_RESTARTS = True  # Required for /worker/pool/restart API
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'America/Los_Angeles'
    CELERY_ENABLE_UTC = True
    CELERY_TRACK_STARTED = True
    CELERY_TASK_RESULT_EXPIRES = 3600
    #CELERY_IMPORTS = ('api', )
    #CELERY_ROUTES = {'proj.tasks.add': {'queue': 'hipri'}}
    #CELERY_QUEUES =['']

    # Virtuoso Configuration
    VIRTUOSO = 'DRIVER=/usr/local/lib/virtodbc.so;HOST=192.168.59.103:1111;UID=dba;PWD=dba'
    VIRTUOSO_SQLALCHEMY = 'virtuoso://dba:dba@VOS'
    VIRTUOSO_RDFLIB = 'DSN=VOS;UID=dba;PWD=dba;WideAsUTF16=Y'

    # SPARQL/UPDATE Store URIs
    SPARQL_URI = 'http://localhost:8890/sparql'
    UPDATE_URI = 'http://localhost:8890/sparql-auth'
    

class Development(Config):
    """
    Development configuration
    """
    DEBUG = True
    SECRET_KEY = 'development'


class Production(Config):
    """
    Production configuration
    """
    pass


class Docker(Config):
    """
    Docker configuration

    Docker exposes links between services using environment variables with a
    set prefix. Here we use MQ for the message queue and VIRT for Virtuoso.
    """
    # Celery Configuration
    host = os.environ.get('MQ_PORT_5672_TCP_ADDR', None)
    port = os.environ.get('MQ_PORT_5672_TCP_PORT', None)
    broker = 'amqp://{0}:{1}//'.format(host, port)
    CELERY_BROKER_URL = broker
    CELERY_RESULT_BACKEND = broker
    DEBUG = True

    # Virtuoso Configuration
    # TODO: Dockerfile adds VOS or use full connect string?


class Testing(Config):
    """
    Testing configuration
    """
    TESTING = True
    SECRET_KEY = 'testing'