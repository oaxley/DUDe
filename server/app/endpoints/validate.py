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
# @brief	Flask route for the "validate" endpoint

#----- Imports
from __future__ import annotations
from typing import Optional

import jwt
import datetime

from flask import Blueprint, request

from app import app
from app.models import (
    User, Right, UserRight
)

from app.helpers import (
    Validator, HTTPResponse
)


#----- Globals
blueprint = Blueprint("validation", __name__, url_prefix="/validate")


#----- Functions

#
# generic routes
#

@blueprint.route("", methods=["POST"])
def post_validate():
    """Validate a user/right request for a particular application

    Returns:
        200 OK
        400 Bad Request
        401 Unauthorized
        500 Internal Server Error
    """
    # retrieve the data if any
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'token', 'email', 'right' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    try:
        # retrieve the data contained in the token
        token = jwt.decode(data['token'], app.config['DUDE_SECRET_KEY'], "HS256")

        # validate expiry date
        now = datetime.datetime.utcnow().timestamp()
        if token['exp'] < now:
            return HTTPResponse.error(401, "Token has expired.")

        # retrieve the user
        user: Optional[User] = User.query.filter_by(email=data['email'], team_id=token['team_id']).first()
        if not user:
            return HTTPResponse.error(400, f"Invalid user email in the request.")

        # retrieve the right
        right: Optional[Right] = Right.query.filter_by(name=data['right'], team_id=token['team_id']).first()
        if not right:
            return HTTPResponse.error(400, f"Invalid right name in the request.")

        # lookup for the association
        user_right: Optional[UserRight] = UserRight.query.filter_by(user_id=user.id, right_id=right.id).first()
        if not user_right:
            return HTTPResponse.error(403, "User is not authorized")
        else:
            return HTTPResponse.ok({ "message": "User is authorized" })

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route("", methods=["GET", "PUT", "DELETE"])
def default_validate():
    """Default route for other methods than POST

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed()
