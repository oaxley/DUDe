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
class Organization(db.Model):
    """An organization is the main entity where a person belongs to"""
    # __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)

    departments = db.relationship('Department', backref='organization', lazy='dynamic')

class Department(db.Model):
    """A department is an entity within an organization"""
    # __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

    units = db.relationship('Unit', backref='department', lazy='dynamic')

class Unit(db.Model):
    """Departments are subdivised in unit"""
    # __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    applications = db.relationship('Application', backref='unit', lazy='dynamic')
    users = db.relationship('User', backref='unit', lazy='dynamic')

class Application(db.Model):
    """An application belongs to a department unit"""
    # __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    apikey = db.Column(db.String(128), nullable=False, unique=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

    rights = db.relationship('Right', backref='application', lazy='dynamic')

class User(db.Model):
    """A user belongs to a unit"""
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

class Right(db.Model):
    """A right is an abstract object attached to an application"""
    # __tablename__ = "right"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))

class UserRight(db.Model):
    """Associate a user with a specific right"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'))
