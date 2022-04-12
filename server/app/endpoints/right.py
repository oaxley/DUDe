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
from typing import List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import Team, Right

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
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'team_id' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # check if the team exists
    team: Optional[Team] = Team.query.filter_by(id=data['team_id']).first()
    if not team:
        return HTTPResponse.error(0x4041, rid=data['team_id'], table='Team')

    # check if the right exists already or not
    right: Optional[Right] = Right.query.filter_by(name=data['name'], team_id=team.id).first()
    if right:
        return HTTPResponse.error(0x4002, child='Right', parent='Team')

    try:
        right = Right(name=data['name'], team_id=team.id)

        db.session.add(right)
        db.session.commit()

        return HTTPResponse.location(right.id, url_for("right.get_single_right", right_id=right.id))

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
        return HTTPResponse.error(0x4004, name=e.args[0][0], type=e.args[0][1])

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
            "count": f"{len(items)}",
            "rights": [
                {
                    "id": f"{item.id}",
                    "name": item.name,
                    "team_id": f"{item.team_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_right():
    """Update all the rights - Not Implemented

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("POST, GET, DELETE")

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
        return HTTPResponse.internalError(str(e))


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
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("GET, PUT, DELETE")

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
    if not right:
        return HTTPResponse.error(0x4041, rid=right_id, table='Right')

    try:
        return HTTPResponse.ok({
            'id': f"{right.id}",
            'name': right.name,
            'team_id': f"{right.team_id}"
        })

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
    if not right:
        return HTTPResponse.error(0x4041, rid=right_id, table='Right')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    try:
        for key in data:
            if key not in [ 'name', 'team_id' ]:
                return HTTPResponse.error(0x4005, name=key)

            # ensure team_id exists
            if key == 'team_id':
                team: Optional[Team] = Team.query.filter_by(id=data[key]).first()
                if not team:
                    return HTTPResponse.error(0x4041, rid=data[key], table='Team')

            setattr(right, key, data[key])

        db.session.add(right)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))

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
    if not right:
        return HTTPResponse.error(0x4041, rid=right_id, table='Right')

    try:
        return Database.Delete.Right(right.id, None)

    except Exception as e:
        return HTTPResponse.internalError(str(e))
