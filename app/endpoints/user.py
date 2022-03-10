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


#----- Functions
#
# generic routes
#
@blueprint.route("/", methods=["POST"])
@authenticate
def post_unit():
    """Create a new user

    Returns:
        201 Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["GET"])
@authenticate
def get_unit():
    """Get all the users

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["PUT"])
@authenticate
def put_unit():
    """Update all the users - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route("/", methods=["DELETE"])
@authenticate
def delete_unit():
    """Delete all the users

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


