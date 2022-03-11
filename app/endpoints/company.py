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

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Company
from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('company', __name__, url_prefix="/companies")

# valid routes for this blueprint
ROUTE_1="/"
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

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_company():
    """Retrieve all the companies"""

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_company():
    """Update all the companies - Not implemented

    Returns:
        405 Method not allowed
    """
    return (jsonify({}), 405)

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_company():
    """Delete all the companies

    Returns:
        204 No Content
        404 Not found
    """


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
    return (jsonify({}), 405)

@blueprint.route(ROUTE_2, methods=["GET"])
def get_single_company(company_id):
    """Retrieve details for company_id

    Returns:
        200 + details as json
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_company(company_id):
    """Update details for company_id

    Returns:
        204 No Content
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_company(company_id):
    """Delete details for company_id

    Returns:
        204 No Content
        404 Not found
        500 Internal Server Error
    """


#
# routes for units
#
@blueprint.route(ROUTE_3, methods=["POST"])
@authenticate
def post_single_company_units(company_id):
    """Create a new unit and associate it with the company

    Returns:
        201 + Location of the new unit
        400 Bad Request
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["GET"])
@authenticate
def get_single_company_units(company_id):
    """Retrieve all units for company_id

    Returns:
        200 + details as json
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["PUT"])
@authenticate
def put_single_company_units(company_id):
    """Update all units for company_id

    Returns:
        204 No Content
        404 Not found
        500 Internal Server Error
    """

@blueprint.route(ROUTE_3, methods=["DELETE"])
@authenticate
def delete_single_company_units(company_id):
    """Delete all units for company_id

    Returns:
        204 No Content
        404 Not found
        500 Internal Server Error
    """
