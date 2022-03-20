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
# @brief	Flask route for the "teams/<id>/users" endpoint

#----- Imports
from __future__ import annotations
from typing import List, Optional

from flask import request, url_for

from app import app, db
from app.models import Team, User

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)

from .team import blueprint


#----- Globals
# valid route for this endpoint
ROUTE="/<int:team_id>/users"


#----- Functions

@blueprint.route(ROUTE, methods=["POST"])
@authenticate
def post_single_team_users(team_id):
    """Create a new user and associate it with the team

    Returns:
        201 Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if not team:
        return HTTPResponse.error(0x4041, rid=team_id, table='Team')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'email' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # check if the user already exists for this team
    user: Optional[User] = User.query.filter_by(name=data['name'], email=data['email'], team_id=team.id).first()
    if user:
        return HTTPResponse.error(0x4002, child="User", parent="Team")

    try:
        user = User(name=data['name'], email=data['email'], team_id=team.id)

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.location(user.id, url_for('user.get_single_user', user_id=user.id))

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE, methods=["GET"])
@authenticate
def get_single_team_users(team_id):
    """Retrieve all users for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if not team:
        return HTTPResponse.error(0x4041, rid=team_id, table='Team')

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
        items: List[User] = (db.session
            .query(User)
            .order_by(User.id)
            .filter(User.team_id == team.id)
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
                    "email": item.email
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE, methods=["PUT"])
@authenticate
def put_single_team_users(team_id):
    """Update all users for a team

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("POST, GET, DELETE")

@blueprint.route(ROUTE, methods=["DELETE"])
@authenticate
def delete_single_team_users(team_id):
    """Delete all users for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if not team:
        return HTTPResponse.error(0x4041, rid=team_id, table='Team')

    try:
        Database.Delete.User(None, team.id)
        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))
