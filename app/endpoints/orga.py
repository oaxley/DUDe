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
# @brief	Flask routes for the "Organization" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import Organization


#----- Globals
blueprint = Blueprint('organization', __name__)


#----- Functions
# add a new organization
@blueprint.route('/orga', methods=['POST'])
def orga_create():
    data = request.get_json() or {}

    # check the admin user key
    if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
        abort(403)

    # try to add this organization to the DB
    try:
        orga = Organization(name = data['name'])
        db.session.add(orga)
        db.session.commit()
        return (jsonify({"id": orga.id}), 201)
    except:
        abort(409, "Resource already present")

# modify an organization
@blueprint.route('/orga/<int:orga_id>', methods=['PUT'])
def orga_update(orga_id):
    data = request.get_json() or {}

    # check the admin user key
    if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
        abort(403)

    # try to get the record
    orga: Optional[Organization] = Organization.query.filter_by(id=orga_id).first()
    if orga is None:
        abort(404)

    # retrieve previous organization parameters
    old_name = orga.name

    if ('name' not in data) or (data['name'] == old_name):
        abort(400)

    # change the name with the new data
    try:
        orga.name = data['name']
        db.session.add(orga)
        db.session.commit()

        return (jsonify({
            'name': old_name
        }), 200)

    except:
        abort(404)
