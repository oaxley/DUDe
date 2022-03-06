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
# @brief	Flask routes for the "Unit" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask_sqlalchemy import sqlalchemy
from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import (
    Department, Unit
)

from app.helpers import authenticate

#----- Globals
blueprint = Blueprint('unit', __name__)


#----- Functions
@blueprint.route('/unit', methods=['POST'])
@authenticate
def unit_create():
    data = request.get_json() or {}

    # check the admin user key
    # if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
    #     abort(403)

    # try to retrieve the department
    if 'dept_id' not in data:
        abort(400)

    dept: Optional[Department] = Department.query.filter_by(id=data['dept_id']).first()
    if dept is None:
        abort(404)

    # try to add this unit to the DB
    try:
        unit = Unit(name=data['name'], dept_id=dept.id)
        db.session.add(unit)
        db.session.commit()
        return (jsonify({
            "id": unit.id
        }), 201)

    except sqlalchemy.exc.IntegrityError:
        abort(409, "Integrity Error")
