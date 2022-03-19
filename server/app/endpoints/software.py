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
# @brief	Flask route for the "software" endpoint

#----- Imports
from __future__ import annotations
from typing import List, Optional

from uuid import uuid4
from flask import Blueprint, request, url_for

from app import app, db
from app.models import Team, Software

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('software', __name__, url_prefix="/software")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:software_id>"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_software():
    """Create a new software

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

    # check if the software exists already or not
    software: Optional[Software] = Software.query.filter_by(name=data['name'], team_id=team.id).first()
    if software is not None:
        return HTTPResponse.error(400, "Software already exists for this team.")

    try:
        software = Software(name=data['name'], apikey=str(uuid4()), team_id=team.id)

        db.session.add(software)
        db.session.commit()

        return HTTPResponse.location(software.id, url_for("software.get_single_software", software_id=software.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_software():
    """Get all the software

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
        items: List[Software] =(db.session
            .query(Software)
            .order_by(Software.id)
            .filter(Software.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "software": [
                {
                    "id": f"{item.id}",
                    "name": item.name,
                    "apikey": item.apikey,
                    "team_id": f"{item.team_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_software():
    """Update all the software - Not Implemented

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_software():
    """Delete all the software

    Returns:
        204 No content
        500 Internal Server Error
    """
    try:
        # retrieve all the existing teams
        teams: List[Team] = Team.query.order_by(Team.id).all()
        for team in teams:
            Database.Delete.Software(None, team.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))


#
# routes for a single software
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_software(software_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()


@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_software(software_id):
    """Retrieve details for a software

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the software
    software: Optional[Software] = Software.query.filter_by(id=software_id).first()
    if software is None:
        return HTTPResponse.error404(software_id, 'Software')

    try:
        return HTTPResponse.ok({
            'id': f"{software.id}",
            'name': software.name,
            'apikey': software.apikey,
            'team_id': f"{software.team_id}"
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_software(software_id):
    """Update details for a software

    Returns:
        204 No Content
        400 Bad Request
        404 Not Found
        500 Internal Server Error
    """
    data = request.get_json() or {}

    # lookup for the software
    software: Optional[Software] = Software.query.filter_by(id=software_id).first()
    if software is None:
        return HTTPResponse.error404(software_id, 'Software')

    # update fields of interests
    try:
        for key in data:
            if key not in [ 'name', 'team_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(software, key, data[key])

        db.session.add(software)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_software(software_id):
    """Delete a software

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the software
    software: Optional[Software] = Software.query.filter_by(id=software_id).first()
    if software is None:
        return HTTPResponse.error404(software_id, 'Software')

    try:
        return Database.Delete.Software(software.id, None)

    except Exception as e:
        return HTTPResponse.error(500, str(e))
