import os

from flask import Flask, Blueprint, request
from flask_cors import CORS
from flask_pymongo import PyMongo
# from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids

from src.helpers import log
from src.helpers.api_response import return_packet_fail
from src.helpers.constants import Reason


# db = SQLAlchemy()
hashids = Hashids(salt=os.environ['HASHIDS_SALT'], min_length=8)
mongo = PyMongo()


def create_app(config=None):
    app = Flask(__name__)
    _ = CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(config if config else os.environ['APP_SETTINGS'])

    from src import depot  # noqa: E402,F401
    from src.micro_services.system import apis  # noqa: E402,F401
    from src.micro_services.users import apis  # noqa: E402,F401

    # db.init_app(app)
    mongo.init_app(app)

    app.register_blueprint(no_path_api_v1_bp, url_prefix='/')
    app.register_blueprint(users_api_v1_bp, url_prefix='/api/v1/users')
    app.register_blueprint(generics_api_v1_bp, url_prefix='/api/v1/generics')

    @app.before_request
    def before():
        pass

    @app.after_request
    def after(response):
        # 'mimetype', 'path', 'query_string', 'referrer', 'url', 'url_charset', 'url_root', 'user_agent',
        req_keys = ['endpoint', 'full_path', 'method', ]
        req_data = {k: getattr(request, k) for k in req_keys}

        # 'headers', 'location', 'mimetype',
        resp_keys = ['status_code', ]
        resp_data = {k: getattr(response, k) for k in resp_keys}

        app.logger.info('REQ: {} -- RESP: {}'.format(req_data, resp_data))
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        return return_packet_fail(Reason.NOT_FOUND, response_code=404)

    @app.errorhandler(500)
    def internal_error(exp):
        message = exp.message if hasattr(exp, 'message') else None
        return return_packet_fail(Reason.EXCEPTION, message=message, response_code=500)

    return app


no_path_api_v1_bp = Blueprint('no_path_apis', __name__)
generics_api_v1_bp = Blueprint('generics_apis', __name__)
users_api_v1_bp = Blueprint('users_apis', __name__)
