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
# @brief	Flask routes for the "Right" endpoint

#----- Imports
from __future__ import annotations
from typing import Any, List, Optional

from flask_sqlalchemy import sqlalchemy
from flask import Blueprint, jsonify, request, abort
from app import app, db

from app.models import (
    Unit, Right
)

from app.helpers import authenticate


#----- Globals
blueprint = Blueprint('right', __name__)


#----- Functions
@blueprint.route('/right', methods=['POST'])
@authenticate
def right_create():
    data = request.get_json() or {}

    # try to retrieve the Unit
    if 'unit_id' not in data:
        abort(400)

    unit: Optional[Unit] = Unit.query.filter_by(id=data['unit_id']).first()
    if unit is None:
        abort(404)

    # try to add this right to the database
    try:
        right = Right(name=data['name'], unit_id=unit.id)

        db.session.add(right)
        db.session.commit()

        return (jsonify({
            "id": right.id,
        }), 200)

    except sqlalchemy.exc.IntegrityError:
        abort(409)

