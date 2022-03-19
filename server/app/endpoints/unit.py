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
# @brief	Flask route for the "units" endpoint

#----- Imports
from __future__ import annotations
from typing import List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import Company, Team, Unit

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('unit', __name__, url_prefix="/units")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:unit_id>"
ROUTE_3="/<int:unit_id>/teams"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_unit():
    """Create a new unit

    Returns:
        201 Location
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, ['name', 'company_id'])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the company exists
    company: Optional[Company] = Company.query.filter_by(id=data['company_id']).first()
    if company is None:
        return HTTPResponse.error404(data['company_id'], 'Company')

    # check if the unit exists already or not
    unit: Optional[Unit] = Unit.query.filter_by(name=data['name'], company_id=company.id).first()
    if unit is not None:
        return HTTPResponse.error(400, "Unit already existing for this company.")

    try:
        unit = Unit(name=data['name'], company_id=company.id)

        db.session.add(unit)
        db.session.commit()

        return HTTPResponse.location(unit.id, url_for("unit.get_single_unit", unit_id=unit.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_unit():
    """Get all the units

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
        items: List[Unit] = (db.session
            .query(Unit)
            .order_by(Unit.id)
            .filter(Unit.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        # build the result dictionary
        result = {
            'offset': params['offset'],
            'limit': params['limit'],
            'units': [
                {
                'id': f"{item.id}",
                'name': item.name,
                'company_id': f"{item.company_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_unit():
    """Update all the units - Not Implemented

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_unit():
    """Delete all the units

    Returns:
        204 No content
        500 Internal Server Error
    """
    try:
        # retrieve all the existing companies
        companies: List[Company] = Company.query.order_by(Company.id).all()
        for company in companies:
            Database.Delete.Unit(None, company.id)

        return HTTPResponse.noContent()
    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for a single unit
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_unit(unit_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_unit(unit_id):
    """Retrieve details for a unit

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the unit
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

    try:
        return HTTPResponse.ok({
            'id': f"{unit.id}",
            'name': unit.name,
            'company_id': f"{unit.company_id}"
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_unit(unit_id):
    """Update details for a unit

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    # lookup for the unit
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    try:
        for key in data:
            if key not in [ 'name', 'company_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(unit, key, data[key])

        db.session.add(unit)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_unit(unit_id):
    """Delete a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the unit
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

    try:
        return Database.Delete.Unit(unit.id, None)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for teams
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_unit_teams(unit_id):
    """Create a new team and associate it with the unit

    Returns:
        201 Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, ['name'])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the team already exists for this unit
    team: Optional[Team] = Team.query.filter_by(name=data['name'], unit_id=unit.id).first()
    if team:
        return HTTPResponse.error(400, "Team already exists for this unit.")

    try:
        team = Team(name=data['name'], unit_id=unit.id)

        db.session.add(team)
        db.session.commit()

        return HTTPResponse.location(team.id, url_for('team.get_single_team', team_id=team.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_unit_teams(unit_id):
    """Retrieve all teams for a unit

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

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
        items: List[Team] =(db.session
            .query(Team)
            .order_by(Team.id)
            .filter(Team.unit_id == unit.id)
            .filter(Team.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "teams": [
                {
                    "id": f"{item.id}",
                    "name": item.name
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_unit_teams(unit_id):
    """Update all teams for a unit

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_unit_teams(unit_id):
    """Delete all teams for a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    unit: Optional[Unit] = Unit.query.filter_by(id=unit_id).first()
    if unit is None:
        return HTTPResponse.error404(unit_id, 'Unit')

    try:
        Database.Delete.Team(None, unit.id)
        return HTTPResponse.noContent()

    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    except Exception as e:
        return HTTPResponse.error(500, str(e))
