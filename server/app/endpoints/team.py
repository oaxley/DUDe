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
from uuid import uuid4

from app import app, db
from app.models import (
    Team, Unit,
    User, Right, Software
)

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('team', __name__, url_prefix="/teams")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:team_id>"
ROUTE_3="/<int:team_id>/users"
ROUTE_4="/<int:team_id>/rights"
ROUTE_5="/<int:team_id>/software"


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
    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'unit_id' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the unit exists
    unit: Optional[Unit] = Unit.query.filter_by(id=data['unit_id']).first()
    if unit is None:
        return HTTPResponse.error404(data['unit_id'], 'Unit')

    # check if the team exists already or not
    team: Optional[Team] = Team.query.filter_by(name=data['name'], unit_id=unit.id).first()
    if team is not None:
        return HTTPResponse.error(400, "Team already existing for this unit.")

    try:
        team = Team(name=data['name'], unit_id=unit.id)

        db.session.add(team)
        db.session.commit()

        return HTTPResponse.location(team.id, url_for("team.get_single_team", team_id=team.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
                    "name": item.name,
                    "unit_id": f"{item.unit_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_team():
    """Update all the teams

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

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
        return HTTPResponse.error(500, str(e))

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
    return HTTPResponse.notAllowed()

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
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    try:
        return HTTPResponse.ok({
            'id': f"{team.id}",
            'name': team.name,
            'unit_id': f"{team.unit_id}"
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    data = request.get_json() or {}
    try:
        for key in data:
            if key not in [ 'name', 'unit_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(team, key, data[key])

        db.session.add(team)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    try:
        return Database.Delete.Team(team.id, None)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


#
# routes for users
#
@blueprint.route(ROUTE_3, methods=["POST"])
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
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'email' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the user already exists for this team
    user: Optional[User] = User.query.filter_by(name=data['name'], email=data['email'], team_id=team.id).first()
    if user:
        return HTTPResponse.error(400, "User already exists for this Team.")

    try:
        user = User(name=data['name'], email=data['email'], team_id=team.id)

        db.session.add(user)
        db.session.commit()

        return HTTPResponse.location(user.id, url_for('user.get_single_user', user_id=user.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_3, methods=["GET"])
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
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_team_users(team_id):
    """Update all users for a team

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_3, methods=["DELETE"])
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
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    try:
        Database.Delete.User(None, team.id)
        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for rights
#
@blueprint.route(ROUTE_4, methods=["POST"])
@authenticate
def post_single_team_rights(team_id):
    """Create a new right and associate it with the team

    Returns:
        201 Location of the new user
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the team
    team: Optional[Team] = Team.query.filter_by(id=team_id).first()
    if team is None:
        return HTTPResponse.error404(team_id, 'Team')

    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, [ 'name' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the right already exists for this team
    right: Optional[Right] = Right.query.filter_by(name=data['name'], team_id=team.id).first()
    if right:
        return HTTPResponse.error(400, "Right already exists for this Team.")

    try:
        right = Right(name=data['name'], team_id=team.id)

        db.session.add(right)
        db.session.commit()

        return HTTPResponse.location(right.id, url_for('right.get_single_right', right_id=right.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_4, methods=["GET"])
@authenticate
def get_single_team_rights(team_id):
    """Retrieve all rights for a team

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
        items: List[Right] = (db.session
            .query(Right)
            .order_by(Right.id)
            .filter(Right.team_id == team.id)
            .filter(Right.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "rights": [
                {
                    "id": f"{item.id}",
                    "name": item.name
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_4, methods=["PUT"])
@authenticate
def put_single_team_rights(team_id):
    """Update all rights for a team

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_4, methods=["DELETE"])
@authenticate
def delete_single_team_rights(team_id):
    """Delete all rights for a team

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
        Database.Delete.Right(None, team.id)
        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for software
#
@blueprint.route(ROUTE_5, methods=["POST"])
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

    data = request.get_json() or {}

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

@blueprint.route(ROUTE_5, methods=["GET"])
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

@blueprint.route(ROUTE_5, methods=["PUT"])
@authenticate
def put_single_team_software(team_id):
    """Update all software for a team

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_5, methods=["DELETE"])
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

