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
# @brief	Flask route for the "teams" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Team
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('team', __name__, url_prefix="/teams")


#----- Functions
#
# generic routes
#
@blueprint.route("/", methods=["POST"])
@authenticate
def post_team():
    """Create a new team

    Returns:
        201 + Location
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["GET"])
@authenticate
def get_team():
    """Get all the teams

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route("/", methods=["PUT"])
@authenticate
def put_team():
    """Update all the teams - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route("/", methods=["DELETE"])
@authenticate
def delete_team():
    """Delete all the teams

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for a single team
#
@blueprint.route("/<int:team_id>", methods=["POST"])
@authenticate
def post_single_team(team_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """

@blueprint.route("/<int:team_id>", methods=["GET"])
def get_single_team(team_id):
    """Retrieve details for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>", methods=["PUT"])
@authenticate
def put_single_team(team_id):
    """Update details for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>", methods=["DELETE"])
@authenticate
def delete_single_team(team_id):
    """Delete a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """

#
# routes for users
#
@blueprint.route("/<int:team_id>/users", methods=["POST"])
@authenticate
def post_single_team_users(team_id):
    """Create a new user and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/users", methods=["GET"])
@authenticate
def get_single_team_users(team_id):
    """Retrieve all users for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/users", methods=["PUT"])
@authenticate
def put_single_team_users(team_id):
    """Update all users for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/users", methods=["DELETE"])
@authenticate
def delete_single_team_users(team_id):
    """Delete all users for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """

#
# routes for rights
#
@blueprint.route("/<int:team_id>/rights", methods=["POST"])
@authenticate
def post_single_team_rights(team_id):
    """Create a new right and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/rights", methods=["GET"])
@authenticate
def get_single_team_rights(team_id):
    """Retrieve all rights for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/rights", methods=["PUT"])
@authenticate
def put_single_team_rights(team_id):
    """Update all rights for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/rights", methods=["DELETE"])
@authenticate
def delete_single_team_rights(team_id):
    """Delete all rights for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """

#
# routes for software
#
@blueprint.route("/<int:team_id>/software", methods=["POST"])
@authenticate
def post_single_team_software(team_id):
    """Create a new software and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/software", methods=["GET"])
@authenticate
def get_single_team_software(team_id):
    """Retrieve all software for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/software", methods=["PUT"])
@authenticate
def put_single_team_software(team_id):
    """Update all software for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route("/<int:team_id>/software", methods=["DELETE"])
@authenticate
def delete_single_team_software(team_id):
    """Delete all software for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
