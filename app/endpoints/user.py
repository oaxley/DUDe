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
# @brief	Flask route for the "users" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import User
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('user', __name__, url_prefix="/users")

# valid routes for this blueprint
ROUTE_1="/"
ROUTE_2="/<int:user_id>"
ROUTE_3="/<int:user_id>/rights"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_user():
    """Create a new user

    Returns:
        201 Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_user():
    """Get all the users

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_user():
    """Update all the users - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_user():
    """Delete all the users

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for a single user
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_user(user_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_user(user_id):
    """Retrieve details for a user

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_user(user_id):
    """Update details for a user

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_user(user_id):
    """Delete a user

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for rights
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_user_rights(user_id):
    """Create a new right and associate it with the user

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_user_rights(user_id):
    """Retrieve all rights for a user

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_user_rights(user_id):
    """Update all rights for a user

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_user_rights(user_id):
    """Delete all rights for a user

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
