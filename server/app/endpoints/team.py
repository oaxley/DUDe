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
from typing import List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import Team, Unit, Company

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('team', __name__, url_prefix="/teams")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:team_id>"


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
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'unit_id' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # check if the unit exists
    unit: Optional[Unit] = Unit.query.filter_by(id=data['unit_id']).first()
    if not unit:
        return HTTPResponse.error(0x4041, rid=data['unit_id'], table='Unit')

    # check if the team exists already or not
    team: Optional[Team] = Team.query.filter_by(name=data['name'], unit_id=unit.id).first()
    if team:
        return HTTPResponse.error(0x4002, child="Team", parent="Unit")

    try:
        team = Team(name=data['name'], unit_id=unit.id)

        db.session.add(team)
        db.session.commit()

        return HTTPResponse.location(team.id, url_for("team.get_single_team", team_id=team.id))

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_team():
    """Get all the teams

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
        items: List[Team] =(db.session
            .query(Team)
            .order_by(Team.id)
            .filter(Team.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "count": f"{len(items)}",
            "teams": [
                {
                    "id": f"{item.id}",
                    "name": item.name,
                    "unit_id": f"{item.unit_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_team():
    """Update all the teams

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("POST, GET, DELETE")

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_team():
    """Delete all the teams

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    try:
        # retrieve all the existing units
        units: List[Unit] = Unit.query.order_by(Unit.id).all()
        for unit in units:
            Database.Delete.Team(None, unit.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))


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
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("GET, PUT, DELETE")

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
    if not team:
        return HTTPResponse.error(0x4041, rid=team_id, table='Team')

    try:
        return HTTPResponse.ok({
            'id': f"{team.id}",
            'name': team.name,
            'unit_id': f"{team.unit_id}"
        })

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_team(team_id):
    """Update details for a team

    Returns:
        204 No Content
        404 Not Found
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

    try:
        for key in data:
            if key not in [ 'name', 'unit_id' ]:
                return HTTPResponse.error(0x4005, name=key)

            if key == 'name':
                item: Optional[Team] = Team.query.filter_by(name=data['name'], unit_id=team.unit_id).first()
                if item:
                    return HTTPResponse.error(0x4002, child=data['name'], parent='Unit')

            if key == 'unit_id':
                # retrieve the company we are currently in
                unit: Optional[Unit] = Unit.query.filter_by(id=team.unit_id).first()
                company: Optional[Company] = Company.query.filter_by(id=unit.company_id).first()

                # lookup for this new unit within the same company
                unit = Unit.query.filter_by(id=data['unit_id'], company_id=company.id).first()
                if not unit:
                    return HTTPResponse.error(0x4042, parent='Company', child='Unit', rid=data['unit_id'])

                # ensure item does not exist with this unit
                item: Optional[Team] = Team.query.filter_by(name=team.name, unit_id=data['unit_id']).first()
                if item:
                    return HTTPResponse.error(0x4002, child=team.name, parent='Unit')

            setattr(team, key, data[key])

        db.session.add(team)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_team(team_id):
    """Delete a team

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
        return Database.Delete.Team(team.id, None)

    except Exception as e:
        return HTTPResponse.internalError(str(e))


#
# routes for users
#
from . import team_user

#
# routes for rights
#
from . import team_right

#
# routes for software
#
from . import team_software
