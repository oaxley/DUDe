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
# @brief	Flask route for the "teams/<id>/software" endpoint

#----- Imports
from __future__ import annotations
from typing import List, Optional

from flask import request, url_for
from uuid import uuid4

from app import app, db
from app.models import Team, Software

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)

from .team import blueprint


#----- Globals
# valid route for this endpoint
ROUTE="/<int:team_id>/software"


#----- Functions

@blueprint.route(ROUTE, methods=["POST"])
@authenticate
def post_single_team_software(team_id):
    """Create a new software and associate it with the team

    Returns:
        201 + Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the software already exists for this team
    software: Optional[Software] = Software.query.filter_by(name=data['name'], team_id=team.id).first()
    if software:
        return HTTPResponse.error(400, "Software already exists for this Team.")

    try:
        software = Software(name=data['name'], apikey=str(uuid4()), team_id=team.id)

        db.session.add(software)
        db.session.commit()

        return HTTPResponse.location(software.id, url_for('software.get_single_software', software_id=software.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE, methods=["GET"])
@authenticate
def get_single_team_software(team_id):
    """Retrieve all software for a team

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

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
        items: List[Software] = (db.session
            .query(Software)
            .order_by(Software.id)
            .filter(Software.team_id == team.id)
            .filter(Software.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "count": f"{len(items)}",
            "software": [
                {
                    "id": f"{item.id}",
                    "name": item.name
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE, methods=["PUT"])
@authenticate
def put_single_team_software(team_id):
    """Update all software for a team

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE, methods=["DELETE"])
@authenticate
def delete_single_team_software(team_id):
    """Delete all software for a team

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    try:
        Database.Delete.Software(None, team.id)
        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))