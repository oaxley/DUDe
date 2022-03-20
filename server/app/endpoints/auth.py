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
# @brief	Flask route for the "auth" endpoint

#----- Imports
from __future__ import annotations
from typing import Optional

import jwt
import datetime

from flask import Blueprint, request

from app import app
from app.models import Software

from app.helpers import (
    Validator, HTTPResponse
)


#----- Globals
blueprint = Blueprint("authentication", __name__, url_prefix="/auth")


#----- Functions

#
# generic routes
#

@blueprint.route("", methods=["POST"])
def post_auth():
    """Authenticate a software against the list of know software/apikey

    Returns:
        200 OK
        400 Bad Request
        404 Not Found
        500 Internal Server Error
    """
    # retrieve the data if any
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'name', 'apikey' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # lookup for the software in the database
    software: Optional[Software] = Software.query.filter_by(name=data['name'], apikey=data['apikey']).first()
    if not software:
        return HTTPResponse.error(0x4040, name='Software')

    try:
        # issue at and expiry time
        iat = datetime.datetime.utcnow()
        exp = iat + datetime.timedelta(minutes=app.config['TOKEN_EXPIRY_MINUTES'])

        # generate a new JSON Web Token
        payload = {
            'apikey': software.apikey,
            'name': software.name,
            'team_id': f"{software.team_id}",
            'iat': iat.timestamp(),
            'exp': exp.timestamp()
        }

        token = jwt.encode(payload, app.config['DUDE_SECRET_KEY'], "HS256")
        return HTTPResponse.ok({ 'token': token })

    except Exception as e:
        return HTTPResponse.internalError(str(e))


@blueprint.route("", methods=["GET", "PUT", "DELETE"])
def default_auth():
    """Default route for other methods than POST

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed(allowed="POST")

