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
# @brief	Flask route for the "rights" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Right
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('right', __name__, url_prefix="/rights")


#----- Functions
#
# generic routes
#
@blueprint.route("/", methods=["POST"])
@authenticate
def post_right():
    """Create a new right

    Returns:
        201 Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["GET"])
@authenticate
def get_right():
    """Get all the right

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["PUT"])
@authenticate
def put_right():
    """Update all the rights - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route("/", methods=["DELETE"])
@authenticate
def delete_right():
    """Delete all the rights

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for a single right
#
@blueprint.route("/<int:right_id>", methods=["POST"])
@authenticate
def post_single_right(right_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """

@blueprint.route("/<int:right_id>", methods=["GET"])
def get_single_right(right_id):
    """Retrieve details for a right

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:right_id>", methods=["PUT"])
@authenticate
def put_single_right(right_id):
    """Update details for a right

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:right_id>", methods=["DELETE"])
@authenticate
def delete_single_right(right_id):
    """Delete a right

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """

#
# routes for users relationship
#
@blueprint.route("/<int:right_id>/users", methods=["POST"])
@authenticate
def post_single_right_users(right_id):
    """Create a new user and associate it with the right

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:right_id>/users", methods=["GET"])
@authenticate
def get_single_right_users(right_id):
    """Retrieve all users for a right

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:right_id>/users", methods=["PUT"])
@authenticate
def put_single_right_users(right_id):
    """Update all users for a right

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:right_id>/users", methods=["DELETE"])
@authenticate
def delete_single_right_users(right_id):
    """Delete all users for a right

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """