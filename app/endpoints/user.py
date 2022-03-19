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

from flask import Blueprint, request, url_for

from app import app, db
from app.models import (
    Team, User, Right, UserRight
)

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
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
        Validator.data(data, [ 'name', 'email', 'team_id' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if team is None:
        return HTTPResponse.error404(data['team_id'], 'Team')

    # check if the user exists already or not
    user: Optional[User] = User.query.filter_by(name=data['name'], email=data['email'], team_id=team.id).first()
    if user is not None:
        return HTTPResponse.error(400, f"User already exists for this Team.")

    try:
        user = User(name=data['name'], email=data['email'], team_id=team.id)

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.location(user.id, url_for("user.get_single_user", user_id=user.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_user():
    """Get all the users

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
        items: List[User] =(db.session
            .query(User)
            .order_by(User.id)
            .filter(User.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "users": [{
                "id": f"{item.id}",
                "name": item.name,
                "email": item.email,
                "team_id": item.team_id
            } for item in items]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_user():
    """Update all the users - Not Implemented

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_user():
    """Delete all the users

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    try:
        # retrieve all the existing teams
        teams: List[Team] = Team.query.order_by(Team.id).all()
        for team in teams:
            Database.Delete.User(None, team.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
    return HTTPResponse.notAllowed()

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
        return HTTPResponse.error404(user_id, 'User')

    try:
        return HTTPResponse.ok({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'team_id': user.team_id
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_user(user_id):
    """Update details for a user

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return HTTPResponse.error404(user_id, 'User')

    data = request.get_json() or {}
    try:
        for key in data:
            if key not in [ 'name', 'email', 'team_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(user, key, data[key])

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_user(user_id):
    """Delete a user

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return HTTPResponse.error404(user_id, 'User')

    try:
        return Database.Delete.User(user.id, None)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


#
# routes for rights
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_user_rights(user_id):
    """Create a new right and associate it with the user

    Returns:
        201 Location of the new right
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return HTTPResponse.error404(user_id, 'User')

    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'team_id' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the right already exists for this team
    right: Optional[Right] = Right.query.filter_by(name=data['name'], team_id=data['team_id']).first()
    if right:
        return HTTPResponse.error(400, "Right already exists for this Team.")

    try:
        # create the new right
        right = Right(name=data['name'], team_id=data['team_id'])

        db.session.add(right)
        db.session.commit()

        # create the association user/right
        rel = UserRight(user_id=user.id, right_id=right.id)
        db.session.add(rel)
        db.session.commit()

        return HTTPResponse.location(user.id, url_for('user.get_single_user', user_id=user.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_user_rights(user_id):
    """Retrieve all rights for a user

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return HTTPResponse.error404(user_id, 'User')

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_user_rights(user_id):
    """Update all rights for a user

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    return

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_user_rights(user_id):
    """Delete all rights for a user

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the user
    user: Optional[User] = User.query.filter_by(id=user_id).first()
    if user is None:
        return HTTPResponse.error404(user_id, 'User')
