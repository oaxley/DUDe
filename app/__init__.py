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
# @brief	Application package init file

#----- Imports
import logging

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


#----- Begin
# define the flask application and load the configuration
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)



# print the api-key for administrative tasks
logging.info(f"API-KEY for admin is [{app.config['DUDE_SECRET_KEY']}]")

# import routes at the last moment to avoid cyclic imports
from app import routes
