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
# @brief	DUDE database model

#----- Imports
from app import db

#----- Classes
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    units = db.relationship('Unit', cascade="all,delete", backref='company', lazy='dynamic')

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    teams = db.relationship('Team', cascade="all,delete", backref='unit', lazy='dynamic')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

    users = db.relationship('User', cascade="all,delete", backref='team', lazy='dynamic')
    rights = db.relationship('Right', cascade="all,delete", backref='team', lazy='dynamic')
    software = db.relationship('Software', cascade="all,delete", backref='team', lazy='dynamic')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Right(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    apikey = db.Column(db.String(128), nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))


class UserRight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'))
