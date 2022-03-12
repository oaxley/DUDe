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
# @brief	Helper functions

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional, TypeVar, Generic

from datetime import datetime, timezone

from functools import wraps

from flask import (
    request, abort, jsonify,
    make_response, Response
)

from app import app



#----- Functions

# decorator function to authenticate an endpoint with a token
def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # look for the X-API-Token header in the request
        try:
            token = request.headers['X-API-Token']
            if token != app.config['DUDE_SECRET_KEY']:
                raise Exception()
        except Exception:
            abort(403)

        # call the function
        return fn(*args, **kwargs)

    return wrapper

# always add these headers to each response
def addHeaders(resp: Response) -> Response:
    # API version
    resp.headers['X-API-Version'] = app.config['VERSION']

    return resp

# format the error messages
def errorResponse(code: int, message: str) -> Response:
    message = jsonify({
        "error": {
            "code": f"{code}",
            "message": message
        }
    })

    # create the response
    response = make_response(message, code)
    response = addHeaders(response)

    return response

# location return message
def locationResponse(item_id: int, url: str) -> Response:
    """Create the 201 HTTP Response"""
    message = jsonify({
        "id": f"{item_id}",
    })

    response = make_response(message, 201)
    response = addHeaders(response)
    response.headers['Location'] = url

    return response

def dataResponse(message) -> Response:
    """Create a 200 HTTP response"""
    response = make_response(jsonify(message), 200)
    response = addHeaders(response)
    return response
