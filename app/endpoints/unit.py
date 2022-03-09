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
# @brief	Flask route for the "companies" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Unit
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('unit', __name__, url_prefix="/units")


#----- Functions
#
# generic routes
#
@blueprint.route("/", methods=["POST"])
@authenticate
def post_unit():
    """Create a new unit

    Returns:
        201 + Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["GET"])
@authenticate
def get_unit():
    """Get all the units

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["PUT"])
@authenticate
def put_unit():
    """Update all the units - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route("/", methods=["DELETE"])
@authenticate
def delete_unit():
    """Delete all the units

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for a single unit
#
@blueprint.route("/<int:unit_id>", methods=["POST"])
@authenticate
def post_single_unit(unit_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """

@blueprint.route("/<int:unit_id>", methods=["GET"])
def get_single_unit(unit_id):
    """Retrieve details for a unit

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:unit_id>", methods=["PUT"])
@authenticate
def put_single_unit(unit_id):
    """Update details for a unit

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:unit_id>", methods=["DELETE"])
@authenticate
def delete_single_unit(unit_id):
    """Delete a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for teams
#
@blueprint.route("/<int:unit_id>/teams", methods=["POST"])
@authenticate
def post_single_unit_teams(unit_id):
    """Creata a new team and associate it with the unit

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:unit_id>/teams", methods=["GET"])
@authenticate
def get_single_unit_teams(unit_id):
    """Retrieve all teams for a unit

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:unit_id>/teams", methods=["PUT"])
@authenticate
def put_single_unit_teams(unit_id):
    """Update all teams for a unit

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:unit_id>/teams", methods=["DELETE"])
@authenticate
def delete_single_unit_teams(unit_id):
    """Delete all teams for a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
