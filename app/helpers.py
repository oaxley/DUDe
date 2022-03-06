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
# @brief	Helper functions

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from functools import wraps
from flask import request, jsonify, abort
from app import app



#----- Functions

# decorator function to authenticate an endpoint with a token
def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # retrieve the data from the request
        data = request.get_json() or {}

        # check the validity of the token
        if ('token' not in data) or (data['token'] != app.config['DUDE_SECRET_KEY']):
            abort(403)

        # call the fuinction
        return fn(*args, **kwargs)

    return wrapper
