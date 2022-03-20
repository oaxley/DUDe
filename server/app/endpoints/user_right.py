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
# @brief	Flask route fo the "user-rights" endpoint

#----- Imports
from __future__ import annotations
from typing import List, Optional

from flask import Blueprint, request, url_for

from app import app, db
from app.models import (
    User, Right, UserRight
)

from app.helpers import (
    authenticate, Validator, HTTPResponse, Database
)


#----- Globals
blueprint = Blueprint('user_right', __name__, url_prefix='/user-rights')

# valid routes for this blueprint
ROUTE_1=""
ROUTE_2="/<int:user_right_id>"


#----- Functions
#
# generic routes
#
@blueprint.route(ROUTE_1, methods=["POST"])
@authenticate
def post_userright():
    """Create a new user-right association

    Returns:
        201 Location
        400 Bad Request
        404 Not Found
        500 Internal Server Error
    """
    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    # check parameters
    try:
        Validator.data(data, [ 'user_id', 'right_id' ])
    except KeyError as e:
        return HTTPResponse.error(0x4001, name=str(e))

    # check if the user exists
    user: Optional[User] = User.query.filter_by(id=data['user_id']).first()
    if not user:
        return HTTPResponse.error(0x4041, rid=data['user_id'], table='User')

    # check if the right exists
    right: Optional[Right] = Right.query.filter_by(id=data['right_id']).first()
    if not right:
        return HTTPResponse.error(0x4041, rid=data['right_id'], table='Right')

    # check if the association already exists
    usrg: Optional[UserRight] = UserRight.query.filter_by(user_id=user.id, right_id=right.id).first()
    if usrg:
        return HTTPResponse.error(0x4002, child="UserRight", parent="User/Right")

    try:

        user_right = UserRight(user_id=user.id, right_id=right.id)

        db.session.add(user_right)
        db.session.commit()

        return HTTPResponse.location(user_right.id, url_for('user_right.get_single_userright', user_right_id=user_right.id))

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["GET"])
@authenticate
def get_userright():
    """Get all the user-right associations

    Returns:
        200 OK
        400 Bad Request
        500 Internal Server Error
    """
    # retrieve the parameters from the request (or set the default value)
    try:
        params = Validator.parameters(request, [('offset', 0), ('limit', app.config['DEFAULT_LIMIT_VALUE'])])
    except ValueError as e:
        return HTTPResponse.error(0x4004, name=e.args[0][0], type=e.args[0][1])

    # ensure parameters remains positive
    params['offset'] = abs(params['offset'])
    params['limit'] = abs(params['limit'])

    if params['limit'] > app.config['MAX_LIMIT_VALUE']:
        params['limit'] = app.config['MAX_LIMIT_VALUE']

    try:
        # retrieve all the items between the limits
        items: List[UserRight] =(db.session
            .query(UserRight)
            .order_by(UserRight.id)
            .filter(UserRight.id >= params['offset'])
            .limit(params['limit'])
            .all()
        )

        result = {
            "offset": params['offset'],
            "limit": params['limit'],
            "count": f"{len(items)}",
            "users": [
                {
                    "id": f"{item.id}",
                    "user_id": f"{item.user_id}",
                    "right_id": f"{item.right_id}"
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_userright():
    """Update all the user-right associations

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("POST, GET, DELETE")

@blueprint.route(ROUTE_1, methods=["DELETE"])
@authenticate
def delete_userright():
    """Delete all the user-right associations

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    try:
        # retrieve all the items
        items: List[UserRight] = UserRight.query.order_by(UserRight.id).all()
        for item in items:
            Database.Delete.UserRight(usrg_id=item.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))


#
# routes for a single user-right association
#
@blueprint.route(ROUTE_2, methods=["POST"])
@authenticate
def post_single_userright(user_right_id):
    """This endpoint has no meaning

    Returns:
        405 Method not allowed
    """
    # this line ensures flask does not return errors if data is not purged
    if int(request.headers.get('Content-Length', 0)) > 0:
        request.get_json()
    return HTTPResponse.notAllowed("PUT, GET, DELETE")

@blueprint.route(ROUTE_2, methods=["GET"])
@authenticate
def get_single_userright(user_right_id):
    """Get details for a user-right association

    Returns:
        200 OK
        404 Not found
        500 Internal Server Error
    """
    # lookup the association
    usrg: Optional[UserRight] = UserRight.query.filter_by(id=user_right_id).first()
    if not usrg:
        return HTTPResponse.error(0x4041, rid=user_right_id, table='UserRight')

    try:
        return HTTPResponse.ok({
            'id': f"{usrg.id}",
            'user_id': f"{usrg.user_id}",
            'right_id': f"{usrg.right_id}"
        })

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_2, methods=["PUT"])
@authenticate
def put_single_userright(user_right_id):
    """Update a user-right association

    Returns:
        204 No Content
        404 Not Found
        500 Internal Server Error
    """
    # lookup the association
    usrg: Optional[UserRight] = UserRight.query.filter_by(id=user_right_id).first()
    if not usrg:
        return HTTPResponse.error(0x4041, rid=user_right_id, table='UserRight')

    if int(request.headers.get('Content-Length', 0)) > 0:
        data = request.get_json()
    else:
        data = {}

    try:
        for key in data:
            if key not in [ 'user_id', 'right_id' ]:
                return HTTPResponse.error(0x4005, name=key)

            # ensure right_id exists
            if key == 'right_id':
                right: Optional[Right] = Right.query.filter_by(id=data[key]).first()
                if not right:
                    return HTTPResponse.error(0x4041, rid=data[key], table='Right')

            # ensure user_id exists
            if key == 'user_id':
                user: Optional[User] = User.query.filter_by(id=data[key]).first()
                if not user:
                    return HTTPResponse.error(0x4041, rid=data[key], table='User')

            setattr(usrg, key, data[key])

        db.session.add(usrg)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.internalError(str(e))

@blueprint.route(ROUTE_2, methods=["DELETE"])
@authenticate
def delete_single_userright(user_right_id):
    """Delete a user-right association

    Returns:
        204 No content
        404 Not found
        500 Internal Server Error
    """
    # lookup the association
    usrg: Optional[UserRight] = UserRight.query.filter_by(id=user_right_id).first()
    if not usrg:
        return HTTPResponse.error(0x4041, rid=user_right_id, table='UserRight')

    try:
        return Database.Delete.UserRight(usrg_id=usrg.id)

    except Exception as e:
        return HTTPResponse.internalError(str(e))
