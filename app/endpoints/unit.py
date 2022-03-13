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
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, url_for

from app import app, db
from app.models import Company, Unit

from app.helpers import (
    authenticate, Validator, HTTPResponse
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
    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, ['name', 'company_id'])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the company exists
    company: Optional[Company] = Company.query.filter_by(id=data['company_id']).first()
    if company is None:
        return HTTPResponse.error(404, f"Could not find company with ID #{data['company_id']}")

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

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_unit():
    """Update all the units - Not Implemented

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_unit():
    """Delete all the units

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


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
        return HTTPResponse.error(404, f"Could not find unit with ID #{unit_id}")

    try:
        return HTTPResponse.ok({
            'id': unit.id,
            'name': unit.name,
            'company_id': unit.company_id
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

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_unit(unit_id):
    """Delete a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """


#
# routes for teams
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_unit_teams(unit_id):
    """Create a new team and associate it with the unit

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_unit_teams(unit_id):
    """Retrieve all teams for a unit

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_unit_teams(unit_id):
    """Update all teams for a unit

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_unit_teams(unit_id):
    """Delete all teams for a unit

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
