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
from curses.ascii import HT
from typing import Any, List, Optional

from uuid import uuid4
from flask import Blueprint, jsonify, request, url_for

from app import app, db
from app.models import Team, Software

from app.helpers import (
    authenticate, Validator, HTTPResponse
)


#----- Globals
blueprint = Blueprint('software', __name__, url_prefix="/software")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:software_id>"

# max value for the Limit in query
MAX_LIMIT_VALUE = 20


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
        return HTTPResponse.error(404, f"Could not find team with ID #{data['team_id']}.")

    # check if the software exists already or not
    software: Optional[Software] = Software.query.filter_by(name=data['name'], team_id=team.id).first()
    if software is not None:
        return HTTPResponse.error(400, "Software already existing for this team.")

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
        params = Validator.parameters(request, [('offset', 0), ('limit', 10)])
    except ValueError as e:
        return HTTPResponse.error(400, str(e))

    # ensure parameters remains positive
    params['offset'] = abs(params['offset'])
    params['limit'] = abs(params['limit'])

    if params['limit'] > MAX_LIMIT_VALUE:
        params['limit'] = MAX_LIMIT_VALUE

    try:
        # retrieve all the items between the limits
        items: List[Software] = db.session.query(Software) \
                                .order_by(Software.id) \
                                .filter(Software.id >= params['offset']) \
                                .limit(params['limit']) \
                                .all()

        # build the result dictionary
        result = {
            "offset": f"{params['offset']}",
            "limit": f"{params['limit']}",
            "software": []
        }
        for item in items:
            result['software'].append({
                "id": f"{item.id}",
                "name": item.name,
                "apikey": item.apikey,
                "team_id": f"{item.team_id}"
            })

        # return the response
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
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_software():
    """Delete all the software

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


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
        return HTTPResponse.error(404, f"Could not find software with ID #{software_id}.")

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
        return HTTPResponse.error(404, f"Could not find software with ID #{software_id}.")

    # update fields of interests
    try:
        for key in data:
            if key == 'token':
                continue

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
        return HTTPResponse.error(404, f"Could not find software with ID #{software_id}.")

    try:
        db.session.delete(software)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))
