import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True

    _db_user = os.environ.get('DB_USER', 'root')
    _db_password = os.environ.get('DB_PASSWORD', '')
    _db_host = os.environ.get('DB_HOST', 'localhost')
    _db_name = os.environ.get('DB_NAME', 'skeleton')
    _db_cloudsql_connection_name = os.environ.get('CLOUDSQL_CONNECTION_NAME')

    _local_db = 'mysql://{0}:{1}@{2}/{3}'.format(_db_user, _db_password, _db_host, _db_name)

    LOCAL_SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', _local_db)

    # When running on App Engine a unix socket is used to connect to the cloudsql instance.
    LIVE_SQLALCHEMY_DATABASE_URI_UNIX_SOCKET = (
        'mysql+pymysql://{user}:{password}@/{database}'
        '?unix_socket=/cloudsql/{connection_name}').format(
        user=_db_user, password=_db_password,
        database=_db_name, connection_name=_db_cloudsql_connection_name)

    LIVE_SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@/{database}').format(
        user=_db_user, password=_db_password, database=_db_name)

    if os.environ.get('APP_SETTINGS') == 'config.LiveConfig':
        SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
    else:
        SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # Disable track modifications, as it unnecessarily uses memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    _mongo_user = os.environ.get('MONGO_USER', 'skeleton')
    _mongo_password = os.environ.get('MONGO_PASSWORD', '')
    _mongo_db_name = os.environ.get('MONGO_DB', 'skeleton-dev')
    _mongo_hosts = os.environ.get('MONGO_HOSTS', 'localhost')
    _mongo_options = os.environ.get('MONGO_OPTIONS', 'localhost')
    MONGO_URI = "mongodb://{user}:{password}@{hosts}/{database}?{options}".format(
                user=_mongo_user, password=_mongo_password, hosts=_mongo_hosts, database=_mongo_db_name, options=_mongo_options)
    if not _mongo_password:
        MONGO_URI = "mongodb://{hosts}/{database}".format(hosts=_mongo_hosts, database=_mongo_db_name)

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.environ.get('OAUTH_CREDENTIALS_FB_ID'),
            'secret': os.environ.get('OAUTH_CREDENTIALS_FB_SECRET'),
        },
        'twitter': {
            'id': os.environ.get('OAUTH_CREDENTIALS_TW_ID'),
            'secret': os.environ.get('OAUTH_CREDENTIALS_TW_SECRET'),
        },
        'google': {
            'id': os.environ.get('OAUTH_CREDENTIALS_GOOG_ID'),
            'secret': os.environ.get('OAUTH_CREDENTIALS_GOOG_SECRET'),
        },
    }

    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    SENTRY_DNS = os.environ.get('SENTRY_DNS')

    SENDGRID_USER = os.environ.get('SENDGRID_USER')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    HASHIDS_SALT = os.environ.get('HASHIDS_SALT', 'hashy_ids')

    USER_AUTH_SECRET_KEY = os.environ.get('USER_AUTH_SECRET_KEY', 'test seekret key')
    SERVICE_AUTH_SECRET_KEY = os.environ.get('SERVICE_AUTH_SECRET_KEY', 'test seekeret key')

    # SERVER_NAME = os.environ['SERVER_NAME']

    SLACK_POST_CHANNEL_URL_INFRA = os.environ.get('SLACK_POST_CHANNEL_URL_INFRA')
    SLACK_POST_CHANNEL_URL_UX = os.environ.get('SLACK_POST_CHANNEL_URL_UX')
    SLACK_POST_CHANNEL_URL_USAGE = os.environ.get('SLACK_POST_CHANNEL_URL_USAGE')
    SLACK_POST_CHANNEL_URL_DEBUG = os.environ.get('SLACK_POST_CHANNEL_URL_DEBUG')

    CONST_DISABLE_EVENT_SLACK = bool(int(os.environ.get('CONST_DISABLE_EVENT_SLACK', 0)))
    CONST_DISABLE_EVENT_NOTIFY_SYS = bool(int(os.environ.get('CONST_DISABLE_EVENT_NOTIFY_SYS', 0)))
    CONST_DISABLE_EVENT_AUDIT = bool(int(os.environ.get('CONST_DISABLE_EVENT_AUDIT', 0)))

    CONST_UX_USER_AUTH_TOKEN_EXPIRE_DAY_COUNT = int(os.environ.get('CONST_UX_USER_AUTH_TOKEN_EXPIRE_DAY_COUNT', 1))

    CONST_DISABLE_DEBUG_LOGS = os.environ.get('CONST_DISABLE_DEBUG_LOGS')


class LiveConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
