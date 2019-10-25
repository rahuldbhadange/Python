# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import logging
import signal
import sys
import os
import pkg_resources

import connexion
from flask import jsonify
from flask_cors import CORS

from ioticlabs.dt.api.util import NestedConfig

from rrps.dt.follower.rest_follower import encoder
from rrps.dt.follower.rest_follower.DataAccess import DataAccess
from rrps.dt.follower.rest_follower.auth import AuthError
from rrps.dt.follower.rest_follower.controllers.default_controller import BadRequest, NotFound, InternalServerError
from rrps.dt.follower.rest_follower.follower import FollowerDataHandler

logger = logging.getLogger(__name__)


def handle_error_response(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def signal_handler(follower, data_access):
    follower.stop()

    if data_access:
        data_access.close()

    sys.exit(0)


def set_response_headers(response):

    response.headers["Server"] = " "
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store, no-cache"

    return response


def main(config, agent_config):
    version = pkg_resources.get_distribution("rrps.dt.follower.rest-follower").version

    connection_string = config['rest_follower']['cache_db']['connection_string']
    database = config['rest_follower']['cache_db'].get('db', 'rr_database')

    data_access = None

    try:
        data_access = DataAccess(connection_string, database=database)
        data_access.open()

        if config['rest_follower']['inject_test_data']:
            data_access.check_inject_dummy_data()
    except:  # pylint: disable=broad-except
        logger.exception("Failed connecting to database")

    data_access.remove_legacy_documents()

    follower_status = "ok"
    follower = None
    try:
        follower = FollowerDataHandler(config, agent_config, data_access)
        follower.run(background=True)
    except Exception as ex:  # pylint: disable=broad-except
        logger.exception("Failed creating follower data handler")
        follower_status = "failed: {}".format(ex)

    # catch the ctrl+C to stop the follower gracefully
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(follower, data_access))

    app = connexion.App(__name__, specification_dir='./swagger/')

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'rr b2c'})
    app.add_error_handler(AuthError, handle_error_response)
    app.add_error_handler(BadRequest, handle_error_response)
    app.add_error_handler(NotFound, handle_error_response)
    app.add_error_handler(InternalServerError, handle_error_response)

    # set some settings used by the api calls in the app's config
    app.app.config['connection_string'] = connection_string
    app.app.config['database'] = database
    app.app.config['disable_auth'] = NestedConfig.get(config, 'rest_follower.disable_auth', required=False,
                                                      default=False, check=bool)
    app.app.config['audiences'] = NestedConfig.get(config, 'rest_follower.audiences', required=False, default=[],
                                                   check=list)
    app.app.config['status'] = {"status": follower_status, "version": version}
    app.app.config['follower'] = follower
    app.app.config['cors_origins'] = NestedConfig.get(config, 'rest_follower.cors_origins', required=True, default=[],
                                                      check=list)

    app.app.after_request(set_response_headers)

    # enable CORS including where Request.credentials is include
    # where credentials are cookies, authorization headers or TLS client certificates.
    CORS(app.app, supports_credentials=True, origins=app.app.config['cors_origins'])

    app.run(port=os.environ.get('FLASK_PORT', 8080))
