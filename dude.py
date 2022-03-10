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
# @brief	Dude main application file

#----- Imports


#----- Logging
import logging

# setup the logging facility
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


#----- Begin
# import the application & database
from app import app, db

# create the database if it does not exist
db.create_all()
