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
from typing import Any, List, Optional

from flask import jsonify, request, abort
from app import app

from . import endpoints


#----- Globals
# register all the endpoint
app.register_blueprint(endpoints.BPCompany)
app.register_blueprint(endpoints.BPUnit)
app.register_blueprint(endpoints.BPTeam)
app.register_blueprint(endpoints.BPUser)
app.register_blueprint(endpoints.BPRight)
app.register_blueprint(endpoints.BPSoftware)
app.register_blueprint(endpoints.BPUserRight)

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

