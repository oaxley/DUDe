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

from flask import Blueprint, jsonify, request, abort, url_for
from app import app, db

from app.models import Team, Unit

from app.helpers import (
    authenticate, errorResponse,
    locationResponse, dataResponse
)


#----- Globals
blueprint = Blueprint('team', __name__, url_prefix="/teams")

# valid routes for this blueprint
ROUTE_1="/"
ROUTE_2="/<int:team_id>"
ROUTE_3="/<int:team_id>/users"
ROUTE_4="/<int:team_id>/rights"
ROUTE_5="/<int:team_id>/software"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_team():
    """Create a new team

    Returns:
        201 Location
        400 Bad Request
        404 Not Found
        500 Internal Server Error
    """
    data = request.get_json() or {}

    # check parameters
    if 'unit_id' not in data:
        return errorResponse(400, "Field 'unit_id' is missing from input data.")

    if 'name' not in data:
        return errorResponse(400, "Field 'name' is missing from input data.")

    # check if the unit exists
    unit: Optional[Unit] = Unit.query.filter_by(id=data['unit_id']).first()
    if unit is None:
        return errorResponse(404, f"Could not find unit with ID #{data['unit_id']}")

    # check if the team exists already or not
    team: Optional[Team] = Team.query.filter_by(name=data['name'], unit_id=unit.id).first()
    if team is not None:
        return errorResponse(400, "Team already existing for this unit.")

    try:
        team = Team(name=data['name'], unit_id=unit.id)

        db.session.add(team)
        db.session.commit()

        return locationResponse(team.id, url_for("team.get_single_team", team_id=team.id))

    except Exception as e:
        errorResponse(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_team():
    """Get all the teams

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_team():
    """Update all the teams - Not Implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_1, methods=["DELETE"])
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
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_team(team_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_team(team_id):
    """Retrieve details for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if team is None:
        errorResponse(404, f"Could not find team with ID #{team_id}")

    try:
        return dataResponse({
            'id': team.id,
            'name': team.name,
            'unit_id': team.unit_id
        })

    except Exception as e:
        return errorResponse(500, str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_team(team_id):
    """Update details for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["DELETE"])
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
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_team_users(team_id):
    """Create a new user and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_team_users(team_id):
    """Retrieve all users for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_team_users(team_id):
    """Update all users for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["DELETE"])
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
@blueprint.route(ROUTE_4, methods=["POST"])
@authenticate
def post_single_team_rights(team_id):
    """Create a new right and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_4, methods=["GET"])
@authenticate
def get_single_team_rights(team_id):
    """Retrieve all rights for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_4, methods=["PUT"])
@authenticate
def put_single_team_rights(team_id):
    """Update all rights for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_4, methods=["DELETE"])
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
@blueprint.route(ROUTE_5, methods=["POST"])
@authenticate
def post_single_team_software(team_id):
    """Create a new software and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_5, methods=["GET"])
@authenticate
def get_single_team_software(team_id):
    """Retrieve all software for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_5, methods=["PUT"])
@authenticate
def put_single_team_software(team_id):
    """Update all software for a team

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_5, methods=["DELETE"])
@authenticate
def delete_single_team_software(team_id):
    """Delete all software for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
