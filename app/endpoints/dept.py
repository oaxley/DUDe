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
# @brief	Flask routes for the "Department" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import (
    Organization, Department
)


#----- Globals
blueprint = Blueprint('department', __name__)


#----- Functions
# add a new department
@blueprint.route('/dept', methods=['POST'])
def dept_create():
    data = request.get_json() or {}

    # check the admin user key
    if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
        abort(403)

    # try to retrieve the organization
    if 'orga_id' not in data:
        abort(400)

    orga: Optional[Organization] = Organization.query.filter_by(id=data['orga_id']).first()
    if orga is None:
        abort(404)

    # try to add this department to the DB
    try:
        dept = Department(name = data['name'], org_id=orga.id)
        db.session.add(dept)
        db.session.commit()
        return (jsonify({"id": dept.id}), 201)
    except:
        abort(409, "Resource already present")

# update a department
@blueprint.route('/dept/<int:dept_id>', methods=['PUT'])
def dept_update(dept_id):
    data = request.get_json() or {}

    # check the admin user key
    if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
        abort(403)

    # retrieve the deparment
    dept: Optional[Department] = Department.query.filter_by(id=dept_id).first()
    if dept is None:
        abort(404)

    # change the name of the department
    if 'name' in data:
        try:
            old_name = dept.name
            dept.name = data['name']

            db.session.add(dept)
            db.session.commit()
            return (jsonify(
                {
                    'old_name': old_name,
                    'new_name': dept.name
                }
            ), 200)
        except:
            abort(400)

    # change the department organization
    if 'orga_id' in data:
        try:
            orga: Optional[Organization] = Organization.query.filter_by(id=data['orga_id']).first()
            if orga is None:
                abort(404)

            old_orga = dept.org_id
            dept.org_id = orga.id

            db.session.add(dept)
            db.session.commit()
            return (jsonify(
                {
                    'old_orga_id': old_orga,
                    'new_orga_id': dept.org_id
                }
            ), 200)
        except:
            abort(400)

    abort(400)
