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
# @brief	Flask route for the "companies" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import Company, Unit

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('company', __name__, url_prefix="/companies")

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:company_id>"
ROUTE_3="/<int:company_id>/units"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_company():
    """Create a new company

    Returns:
        201 + Location upon successful creation
        500 Internal Server Error
        400 Bad Request
    """
    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, ['name'])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    company: Optional[Company] = Company.query.filter_by(name=data['name']).first()
    if company is not None:
        return HTTPResponse.error(400, "Company already exist.")

    try:
        company = Company(name=data['name'])

        db.session.add(company)
        db.session.commit()

        resp = HTTPResponse.location(company.id, url_for("company.get_single_company", company_id=company.id))
        return resp

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_company():
    """Retrieve all the companies"""
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
        items: List[Company] = (db.session
            .query(Company)
            .order_by(Company.id)
            .filter(Company.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        # build the result dictionary
        result = {
            "offset": f"{params['offset']}",
            "limit": f"{params['limit']}",
            "companies": [
                {
                    "id": f"{item.id}",
                    "name": item.name
                } for item in items
            ]
        }

        # return the response
        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_company():
    """Update all the companies

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_company():
    """Delete all the companies

    Returns:
        204 No Content
        500 Internal Server Error
    """
    try:
        Database.deleteAll()
        db.session.commit()
        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for a single company
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_company(company_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_company(company_id):
    """Retrieve details for company_id

    Returns:
        200 + details as json
        404 Not found
        500 Internal Server Error
    """
    # lookup for the company
    company: Optional[Company] = Company.query.filter_by(id=company_id).first()
    if company is None:
        return HTTPResponse.error404(company_id, 'Company')

    try:
        return  HTTPResponse.ok({
            'id': f"{company.id}",
            'name': company.name
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_company(company_id):
    """Update details for company_id

    Returns:
        204 No Content
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    data = request.get_json() or {}

    # lookup for the company
    company: Optional[Company] = Company.query.filter_by(id=company_id).first()
    if company is None:
        return HTTPResponse.error404(company_id, 'Company')

    # update fields of interests
    try:
        for key in data:
            if key not in [ 'name' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(company, key, data[key])

        db.session.add(company)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_company(company_id):
    """Delete Company with company_id

    Returns:
        204 No Content
        404 Not found
        500 Internal Server Error
    """
    try:
        # remove the company and all the associated elements
        return Database.Delete.Company(company_id)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

#
# routes for units
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_company_units(company_id):
    """Create a new unit and associate it with the company

    Returns:
        201 Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the company
    company: Optional[Company] = Company.query.filter_by(id=company_id).first()
    if company is None:
        return HTTPResponse.error404(company_id, 'Company')

    # prepare the new unit
    data = request.get_json() or {}
    if 'name' not in data:
        return HTTPResponse.error(400, "Field 'name' is missing from input data.")

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

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_company_units(company_id):
    """Retrieve all units for company_id

    Returns:
        200 OK
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the company
    company: Optional[Company] = Company.query.filter_by(id=company_id).first()
    if company is None:
        return HTTPResponse.error404(company_id, 'Company')

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
        items: List[Unit] = (db.session
            .query(Unit)
            .order_by(Unit.id)
            .filter(Unit.company_id == company.id)
            .filter(Unit.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        # build the result dictionary
        result = {
            "offset": f"{params['offset']}",
            "limit": f"{params['limit']}",
            "units": [
                {
                    "id": f"{item.id}",
                    "name": item.name
                } for item in items
            ]
        }

        # return the response
        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_company_units(company_id):
    """Update all units for company_id

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_company_units(company_id):
    """Delete all units for company_id

    Returns:
        204 No Content
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """
    # lookup for the company
    company: Optional[Company] = Company.query.filter_by(id=company_id).first()
    if company is None:
        return HTTPResponse.error404(company_id, 'Company')

    try:
        Database.Delete.Unit(None, company_id)
        return HTTPResponse.noContent()

    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    except Exception as e:
        return HTTPResponse.error(500, str(e))
