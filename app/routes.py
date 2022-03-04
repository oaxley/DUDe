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
from app import app


#----- Globals


#----- Functions

# main route
@app.route('/')
def index():
    return "Hello, World!"
