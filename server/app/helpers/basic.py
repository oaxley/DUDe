# -*- coding: utf-8 -*-
# vim: set ft=python
#
# This source file is subject to the Apache License 2.0
# that is bundled with this package in the file LICENSE.txt.
# It is also available through the Internet at this address:
# https://opensource.org/licenses/Apache-2.0
#
# @author	Sebastien LEGRAND
# @license	Apache License 2.0
#
# @brief	Basic helper functions

#----- Imports
from functools import wraps

from flask import request, abort
from app import app

from .http_response import HTTPResponse

#----- Functions

# decorator function to authenticate an endpoint with a token
def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # look for the X-API-Token header in the request
        token = request.headers.get('X-API-Token', '')
        if token != app.config['DUDE_SECRET_KEY']:
            return HTTPResponse.error(403, "API token is missing or invalid.")

        # call the function
        return fn(*args, **kwargs)

    return wrapper
