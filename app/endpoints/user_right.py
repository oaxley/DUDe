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
    data = request.get_json() or {}

    # check parameters
    try:
        Validator.data(data, [ 'user_id', 'right_id' ])
    except KeyError as e:
        return HTTPResponse.error(400, str(e))

    # check if the user exists
    user: Optional[User] = User.query.filter_by(id=data['user_id']).first()
    if not user:
        return HTTPResponse.error404(data['user_id'], 'User')

    # check if the right exists
    right: Optional[Right] = Right.query.filter_by(id=data['right_id']).first()
    if not right:
        return HTTPResponse.error404(data['right_id'], 'Right')

    try:

        user_right = UserRight(user_id=user.id, right_id=right.id)

        db.session.add(user_right)
        db.session.commit()

        return HTTPResponse.location(user_right.id, url_for('user_right.get_single_userright', user_right_id=user_right.id))

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
        return HTTPResponse.error(400, str(e))

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
            "users": [
                {
                    "id": f"{item.id}",
                    "user_id": item.user_id,
                    "right_id": item.right_id
                } for item in items
            ]
        }

        return HTTPResponse.ok(result)

    except Exception as e:
        return HTTPResponse.error(500, str(e))


@blueprint.route(ROUTE_1, methods=["PUT"])
@authenticate
def put_userright():
    """Update all the user-right associations

    Returns:
        405 Method not allowed
    """
    return HTTPResponse.notAllowed()

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
        # retrieve all the users
        users: List[User] = User.query.order_by(User.id).all()
        for user in users:
            Database.Delete.UserRight(user.id, None)

        # retrieve all the rights
        rights: List[Right] = Right.query.order_by(Right.id).all()
        for right in rights:
            Database.Delete.UserRight(None, right.id)

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
    return HTTPResponse.notAllowed()

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
        return HTTPResponse.error404(user_right_id, 'UserRight')

    try:
        return HTTPResponse.ok({
            'id': usrg.id,
            'user_id': usrg.user_id,
            'right_id': usrg.right_id
        })

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
        return HTTPResponse.error404(user_right_id, 'UserRight')

    data = request.get_json() or {}
    try:
        for key in data:
            if key not in [ 'user_id', 'right_id' ]:
                return HTTPResponse.error(400, f"Could not update field '{key}'.")

            setattr(usrg, key, data[key])

        db.session.add(usrg)
        db.session.commit()

        return HTTPResponse.noContent()

    except Exception as e:
        return HTTPResponse.error(500, str(e))

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
        return HTTPResponse.error404(user_right_id, 'UserRight')

    try:
        return Database.Delete.UserRight(usrg_id=usrg.id)

    except Exception as e:
        return HTTPResponse.error(500, str(e))
