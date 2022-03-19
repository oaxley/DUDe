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
from app.models import (
    Team, User, Right, UserRight
)

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('right', __name__, url_prefix="/rights")

# valid routes for this blueprint
ROUTE_1=""
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
        Validator.data(data, [ 'name', 'team_id' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if team is None:
        return HTTPResponse.error404(data['team_id'], 'Team')

    # check if the right exists already or not
    right: Optional[Right] = Right.query.filter_by(name=data['name'], team_id=team.id).first()
    if right is not None:
        return HTTPResponse.error(400, "Right already exists for this Team.")

    try:
        right = Right(name=data['name'], team_id=team.id)

        db.session.add(right)
        db.session.commit()

        return HTTPResponse.location(right.id, url_for("right.get_single_right", right_id=right.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_right():
    """Get all the rights

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """
    # retrieve the parameters from the request (or set the default value)
    try:
        params = Validator.parameters(request, [('offset', 0), ('limit', app.config['DEFAULT_LIMIT_VALUE'])])
    except ValueError as e:
        return HTTPResponse.error(400, str(e))

    # ensure parameters remains positive
    params['offset'] = abs(params['offset'])
    params['limit'] = abs(params['limit'])

    if params['limit'] > app.config['MAX_LIMIT_VALUE']:
        params['limit'] = app.config['MAX_LIMIT_VALUE']

    try:
        # retrieve all the items between the limits
        items: List[Right] =(db.session
            .query(Right)
            .order_by(Right.id)
            .filter(Right.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "users": [{
                "id": f"{item.id}",
                "name": item.name,
                "team_id": item.team_id
            } for item in items]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_right():
    """Update all the rights - Not Implemented

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_right():
    """Delete all the rights

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    try:
        # retrieve all the existing teams
        teams: List[Team] = Team.query.order_by(Team.id).all()
        for team in teams:
            Database.Delete.Right(None, team.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
    return HTTPResponse.notAllowed()

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
        return HTTPResponse.error404(right_id, 'Right')

    try:
        return HTTPResponse.ok({
            'id': right.id,
            'name': right.name,
            'team_id': right.team_id
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_right(right_id):
    """Update details for a right

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return HTTPResponse.error404(right_id, 'Right')

    data = request.get_json() or {}
    try:
        for key in data:
            if key not in [ 'name', 'team_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(right, key, data[key])

        db.session.add(right)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_right(right_id):
    """Delete a right

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return HTTPResponse.error404(right_id, 'Right')

    try:
        return Database.Delete.Right(right.id, None)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


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
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return HTTPResponse.error404(right_id, 'Right')


@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_right_users(right_id):
    """Retrieve all users for a right

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return HTTPResponse.error404(right_id, 'Right')

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
    # lookup for the right
    right: Optional[Right] = Right.query.filter_by(id=right_id).first()
    if right is None:
        return HTTPResponse.error404(right_id, 'Right')
