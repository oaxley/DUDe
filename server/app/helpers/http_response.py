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
# @brief	Standard HTTP Response class

#----- Imports
from __future__ import annotations
from typing import Any, List, Dict

from flask import Response, make_response, jsonify

from app import app
from app.localization import getMessage


#----- Class
class HTTPResponse:
    """This class regroups all the HTTP responses"""

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
    # def error(code: int, message: str) -> Response:
    def error(code: int, **kwargs) -> Response:
        """Format an error response with the code and value provided

        Args:
            code: the message code
            kwargs: the list of keyword arguments for the message

        Returns:
            a Response object
        """

        # retrieve the HTTP code
        d1 = (code >> 4) & 0x0f
        d2 = (code >> 8) & 0x0f
        d3 = (code >> 12) & 0x0f
        http_code = int(f"{d3}{d2}{d1}")

        # create the JSON value for this error
        value = jsonify({
            "error": {
                "code": f"{http_code}",
                "message": getMessage(code, **kwargs)
            }
        })

        # create the response and add extra headers
        response = make_response(value, http_code)
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
    def ok(message: str) -> Response:
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
    def notAllowed(allowed: str = "GET, PUT, DELETE") -> Response:
        """Create a HTTP 405 (Method not allowed) response

        Returns:
            a Response object
        """
        response = HTTPResponse.error(0x4050)
        response.headers['Allow'] = allowed
        return response

    @staticmethod
    def internalError(message: str):
        """Create a HTTP 500 (Internal Server Error) response

        Returns:
            if debug mode is active, return the Python trace, otherwise returns the standard message
        """
        if app.config["DEBUG"] == True:
            return HTTPResponse.error(0x5001, trace=message)

        return HTTPResponse.error(0x5000)
