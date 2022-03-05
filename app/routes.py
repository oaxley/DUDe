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
# @brief	Routes definition for Dude project

#----- Imports
from __future__ import annotations
from typing import Any, List

from flask import jsonify, request, abort
from app import app, db

from .models import Organization


#
#----- Generic routes
#

# main route
@app.route('/')
def index():
    return f"Dummy User Directory (DUDe) - {app.config['VERSION']}"

# return the version information
@app.route('/version')
def version():
    return jsonify({'version': app.config['VERSION']})


#
#----- Organization routes
#

# add a new organization
@app.route('/orga', methods=['POST'])
def orga_create():
    data = request.get_json()

    # check the admin user key
    if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
        abort(403)

    # try to add this organization to the DB
    try:
        u = Organization(name = data['name'])
        db.session.add(u)
        db.session.commit()
        return (jsonify({"id": u.id}), 201)
    except:
        abort(409, "Resource already present")

