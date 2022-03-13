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
from typing import Any, List, Dict, Optional, Tuple

from datetime import datetime, timezone

from functools import wraps

from flask import (
    request, abort, jsonify,
    make_response, Response, Request
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


#----- Classes

class Validator:
    """This class regroups all the methods to validate inputs data or parameters"""

    def __init__(self):
        pass

    @staticmethod
    def data(input: Dict[str, Any], fields: List[str]) -> None:
        """Validate input JSON data

        Args:
            input: the json input
            fields: the list of fields that should be present in the input

        Raises:
            'KeyError' if a field is missing from the the input
        """
        for field in fields:
            if field not in input:
                raise KeyError(f"Field '{field}' is missing from input data.")

    @staticmethod
    def parameters(request: Request, fields: List[Tuple[str, Any]]):
        """Validate input parameters from query

        Args:
            request: the HTTP request
            fields: a list of Tuple with the name of the parameter and its default value

        Raises:
            'ValueError' if the parameter cannot be cast to a proper value

        Returns:
            a Dict[str, Any] with the parameter values
        """
        results: Dict[str, Any] = {}
        for field, default in fields:
            value = request.args.get(field)

            if value is None:
                results[field] = default
            else:
                if type(default) is int:
                    try:
                        results[field] = int(value)
                        continue
                    except ValueError:
                        raise ValueError(f"Field {field} cannot be converted to an int.")

                if type(default) is str:
                    try:
                        results[field] = str(value)
                        continue
                    except ValueError:
                        raise ValueError(f"Field {field} cannot be converted to a str.")

                if type(default) is bool:
                    results[field] = bool(value)
                    continue

        return results

class HTTPResponse:
    """This class regroups all the HTTP responses"""

    def __init__(self):
        pass

    @staticmethod
    def headers(resp: Response) -> Response:
        """Add custom header fields to the response

        Args:
            resp: the response object

        Returns:
            the response object with extra headers
        """
        # API version
        resp.headers['X-API-Version'] = app.config['VERSION']

        return resp

    @staticmethod
    def error(code: int, message: str) -> Response:
        """Format an error response with the code and value provided

        Args:
            code: the HTTP code for the error (4xx or 5xx)
            value: the message to add the error response

        Returns:
            a Response object
        """
        # create the JSON value for this error
        value = jsonify({
            "error": {
                "code": f"{code}",
                "message": value
            }
        })

        # create the response and add extra headers
        response = make_response(value, code)
        response = HTTPResponse.headers(response)

        return response

    @staticmethod
    def location(item_id: int, url: str) -> Response:
        """Create a HTTP 201 (Created) response

        Args:
            item_id: the ID of the new item created
            url: the url for the Location header

        Returns:
            a Response object
        """
        value = jsonify({
            "id": f"{item_id}",
        })

        # create the response and add extra headers
        response = make_response(value, 201)
        response = HTTPResponse.headers(response)
        response.headers['Location'] = url

        return response

    @staticmethod
    def noContent() -> Response:
        """Create a HTTP 204 (No Content) response

        Returns:
            a Response object
        """
        # create the response and add extra headers
        response = make_response(jsonify({}), 204)
        response = HTTPResponse.headers(response)

        return response

    @staticmethod
    def ok(message) -> Response:
        """Create a HTTP 200 (OK) response

        Args:
            message: the data for the response

        Returns:
            a Response object
        """
        # create the response and add extra headers
        response = make_response(jsonify(message), 200)
        response = HTTPResponse.headers(response)

        return response

    @staticmethod
    def notAllowed() -> Response:
        """Create a HTTP 405 (Method not allowed) response

        Returns:
            a Response object
        """
        return HTTPResponse.error(405, "Method not allowed.")
