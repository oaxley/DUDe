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

from flask import Blueprint, jsonify, request, url_for

from app import app, db
from app.models import Team, Right

from app.helpers import (
    authenticate, errorResponse,
    locationResponse, dataResponse, validate
)


#----- Globals
blueprint = Blueprint('right', __name__, url_prefix="/rights")

# valid routes for this blueprint
ROUTE_1="/"
ROUTE_2="/<int:right_id>"
ROUTE_3="/<int:right_id>/rights"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_right():
    """Create a new right

    Returns:
        201 Location
        400 Bad Request
        500 Internal Server Error
    """
    data = request.get_json() or {}

    # check parameters
    try:
        validate(data, [ 'name', 'team_id' ])
    except Exception as e:
        return errorResponse(400, str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if team is None:
        return errorResponse(404, f"Could not find team with ID #{data['team_id']}")

    # check if the right exists already or not
    right: Optional[Right] = Right.query.filter_by(name=data['name'], team_id=team.id).first()
    if right is not None:
        return errorResponse(400, "Right already existing for this team.")

    try:
        right = Right(name=data['name'], team_id=team.id)

        db.session.add(right)
        db.session.commit()

        return locationResponse(right.id, url_for("right.get_single_right", right_id=right.id))

    except Exception as e:
        return errorResponse(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_right():
    """Get all the rights

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_right():
    """Update all the rights - Not Implemented

    Returns:
        405 Method not allowed
    """
    return errorResponse(405, "Method not allowed")

@blueprint.route(ROUTE_1, methods=["DELETE"])
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
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_right(right_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    return errorResponse(405, "Method not allowed")

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_right(right_id):
    """Retrieve details for a right

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return errorResponse(404, f"Could not find right with ID #{right_id}")

    try:
        return dataResponse({
            'id': right.id,
            'name': right.name,
            'team_id': right.team_id
        })

    except Exception as e:
        return errorResponse(500, str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_right(right_id):
    """Update details for a right

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["DELETE"])
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
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_right_users(right_id):
    """Create a new user and associate it with the right

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_right_users(right_id):
    """Retrieve all users for a right

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_right_users(right_id):
    """Update all users for a right

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_right_users(right_id):
    """Delete all users for a right

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
