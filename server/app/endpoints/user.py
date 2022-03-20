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
from typing import List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import Team, User

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
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'email', 'team_id' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if not team:
        return HTTPResponse.error(0x4041, rid=data['team_id'], table='Team')

    # check if the user exists already or not
    user: Optional[User] = User.query.filter_by(name=data['name'], email=data['email'], team_id=team.id).first()
    if user:
        return HTTPResponse.error(0x4002, child="User", parent="Team")

    try:
        user = User(name=data['name'], email=data['email'], team_id=team.id)

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.location(user.id, url_for("user.get_single_user", user_id=user.id))

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
        return HTTPResponse.error(0x4004, name=e.args[0][0], type=e.args[0][1])

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
            "count": f"{len(items)}",
            "users": [
                {
                    "id": f"{item.id}",
                    "name": item.name,
                    "email": item.email,
                    "team_id": f"{item.team_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_user():
    """Update all the users - Not Implemented

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("POST, GET, DELETE")

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
        return HTTPResponse.internalError(str(e))


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
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("GET, PUT, DELETE")

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
    if not user:
        return HTTPResponse.error(0x4041, rid=user_id, table='User')

    try:
        return HTTPResponse.ok({
            'id': f"{user.id}",
            'name': user.name,
            'email': user.email,
            'team_id': f"{user.team_id}"
        })

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
    if not user:
        return HTTPResponse.error(0x4041, rid=user_id, table='User')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    try:
        for key in data:
            if key not in [ 'name', 'email', 'team_id' ]:
                return HTTPResponse.error(0x4005, name=key)

            # ensure team_id exists
            if key == 'team_id':
                team: Optional[Team] = Team.query.filter_by(id=data[key]).first()
                if not team:
                    return HTTPResponse.error(0x4041, rid=data[key], table='Team')

            setattr(user, key, data[key])

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
    if not user:
        return HTTPResponse.error(0x4041, rid=user_id, table='User')

    try:
        return Database.Delete.User(user.id, None)

    except Exception as e:
        return HTTPResponse.internalError(str(e))
