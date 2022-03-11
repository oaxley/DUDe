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
# @brief	Flask route for the "software" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Software
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('software', __name__, url_prefix="/software")

# valid routes for this blueprint
ROUTE_1="/"
ROUTE_2="/<int:software_id>"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_software():
    """Create a new software

    Returns:
        201 Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_software():
    """Get all the software

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_software():
    """Update all the software - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_software():
    """Delete all the software

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for a single software
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_software(software_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_software(software_id):
    """Retrieve details for a software

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_software(software_id):
    """Update details for a software

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_software(software_id):
    """Delete a software

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
