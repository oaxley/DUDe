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
from app import app, db


#----- Begin

# create the SQLAlchemy tables
db.create_all()

# run the application
if __name__ == "__main__":
    app.run()
