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
# @brief	Configuration objecrt

#----- Imports
import os

#----- GLobals
basedir = os.path.abspath(os.path.dirname(__file__))

#----- Class
class Config:
    # the API-KEY used for the administrator section
    DUDE_SECRET_KEY = os.environ.get("DUDE_SECRET_KEY", None)

    # SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "../..", "dude.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # application semantic version
    VERSION = "1.0.0"

    # max value for the Limit parameter in "Get All" query
    MAX_LIMIT_VALUE = 20
    DEFAULT_LIMIT_VALUE = 10

    # token expiry time in minutes
    TOKEN_EXPIRY_MINUTES = 15

    # default locale
    DEFAULT_LOCALE = "en_US"
