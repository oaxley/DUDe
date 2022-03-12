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

from flask import Blueprint, jsonify, request, url_for

from app import app, db
from app.models import Team, User

from app.helpers import (
    authenticate, errorResponse,
    locationResponse, dataResponse, validate
)


#----- Globals
blueprint = Blueprint('user', __name__, url_prefix="/users")

# valid routes for this blueprint
ROUTE_1=""
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
        404 Not Found
        500 Internal Server Error
    """
    data = request.get_json() or {}

    # check parameters
    try:
        validate(data, [ 'name', 'email', 'team_id' ])
    except Exception as e:
        return errorResponse(400, str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if team is None:
        return errorResponse(404, f"Could not find team with ID #{data['team_id']}")

    # check if the user exists already or not
    user: Optional[User] = User.query.filter_by(name=data['name'], email=data['email'], team_id=team.id).first()
    if user is not None:
        return errorResponse(400, f"User already existing for this team.")

    try:
        user = User(name=data['name'], email=data['email'], team_id=team.id)

        db.session.add(user)
        db.session.commit()

        return locationResponse(user.id, url_for("user.get_single_user", user_id=user.id))

    except Exception as e:
        return errorResponse(500, str(e))

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
    return errorResponse(405, "Method not allowed")

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
    return errorResponse(405, "Method not allowed")

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_user(user_id):
    """Retrieve details for a user

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return errorResponse(404, f"Could not find user with ID #{user_id}")

    try:
        return dataResponse({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'team_id': user.team_id
        })
    except Exception as e:
        return errorResponse(500, str(e))

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
