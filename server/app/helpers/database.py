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
# @brief	Class to facilitate database management

#----- Imports
from __future__ import annotations
from typing import Any, List, Dict, Optional

from app import db
from app.models import (
    Company, Right, Unit, Team, Software,
    User, Right, UserRight
)

from .http_response import HTTPResponse


#----- Globals


#----- Functions


#----- Classes
class Database:
    """Helper class to facilitate database management"""

    @staticmethod
    def deleteAll() -> None:
        """Delete all the tables from the database"""
        Company.query.delete()
        Unit.query.delete()
        Team.query.delete()
        User.query.delete()
        Right.query.delete()
        UserRight.query.delete()

    class Delete:
        """Specific helper class for deletion management"""

        @staticmethod
        def Company(company_id: Optional[int]) -> HTTPResponse:
            """Delete Company record

            Args:
                company_id: ID of the Company to delete

            Raises:
                Exception is company_id is None

            Returns:
                HTTPResponse value 204 on success, 404 if the Company cannot be found
            """
            if company_id is None:
                raise Exception("company_id is None in Delete::Company")

            company: Company = Company.query.filter(Company.id == company_id).first()
            if company:
                # cascade the deletion to all Units
                Database.Delete.Unit(None, company.id)

                # delete this company
                db.session.delete(company)
                db.session.commit()

                return HTTPResponse.noContent()
            else:
                return HTTPResponse.error404(company_id, 'company')

        @staticmethod
        def Unit(unit_id: Optional[int], company_id: Optional[int]) -> HTTPResponse|None:
            """Delete Unit record

            Args:
                unit_id: ID of the Unit to delete
                company_id: ID of the Company for massive selection

            Raises:
                Exception is unit_id/company_id are None

            Returns:
                HTTPResponse value 204 on success, 404 if the Unit cannot be found
            """
            if (unit_id is None) and (company_id is None):
                raise Exception("Both unit_id and company_id are None in Delete::Unit.")

            # delete a single unit
            if unit_id:
                unit: Unit = Unit.query.filter(Unit.id == unit_id).first()
                if unit:
                    # cascade the deletion to teams
                    Database.Delete.Team(None, unit.id)

                    db.session.delete(unit)
                    db.session.commit()

                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(unit_id, 'Unit')

            # massive deletion
            if company_id:
                units: List[Unit] = Unit.query.filter(Unit.company_id == company_id).all()
                for unit in units:
                    Database.Delete.Team(None, unit.id)
                    db.session.delete(unit)
                db.session.commit()

        @staticmethod
        def Team(team_id: Optional[int], unit_id: Optional[int]) -> HTTPResponse|None:
            """Delete Team record

            Args:
                team_id: ID of the Team to delete
                unit_id: ID of the Unit for massive selection

            Raises:
                Exception is unit_id/company_id are None

            Returns:
                HTTPResponse value 204 on success, 404 if the Team cannot be found
            """
            def removeTeam(team: Team) -> None:
                """Remove all the dependencies from a Team"""
                # delete all the associated Software
                Database.Delete.Software(None, team.id)

                # delete all the associated Users
                Database.Delete.User(None, team.id)

                # delete all the associated Rights
                Database.Delete.Right(None, team.id)

                # remove the team
                db.session.delete(team)
                db.session.commit()


            if (team_id is None) and (unit_id is None):
                raise Exception("Both team_id and unit_id are None in Delete::Team.")

            if team_id:
                team: Team = Team.query.filter(Team.id == team_id).first()
                if team:
                    removeTeam(team)
                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(team_id, 'Team')

            # massive deletion
            if unit_id:
                teams: List[Team] = Team.query.filter(Team.unit_id == unit_id).all()
                for team in teams:
                    removeTeam(team)

        @staticmethod
        def Software(soft_id: Optional[int], team_id: Optional[int]) -> HTTPResponse|None:
            """Delete Software record

            Args:
                soft_id : ID of the Software to delete
                team_id : ID of the Team for massive selection

            Raises:
                Exception is unit_id/company_id are None

            Returns:
                HTTPResponse value 204 on success, 404 if the Software cannot be found
            """
            if (soft_id is None) and (team_id is None):
                raise Exception("Both soft_id and team_id are None in Delete::Software.")

            if soft_id:
                software: Software = Software.query.filter(Software.id == soft_id).first()
                if software:
                    db.session.delete(software)
                    db.session.commit()
                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(soft_id, 'Software')

            # massive deletion
            if team_id:
                softs: Software = Software.query.filter(Software.team_id == team_id).all()
                for soft in softs:
                    db.session.delete(soft)
                db.session.commit()

        @staticmethod
        def User(user_id: Optional[int], team_id: Optional[int]) -> HTTPResponse|None:
            """Delete User record

            Args:
                user_id : ID of the User to delete
                team_id : ID of the Team for massive selection

            Raises:
                Exception is unit_id/company_id are None

            Returns:
                HTTPResponse value 204 on success, 404 if the User cannot be found
            """

            if (user_id is None) and (team_id is None):
                raise Exception("Both user_id and team_id are None in Delete::User.")

            if user_id:
                user: User = User.query.filter(User.id == user_id).first()
                if user:
                    Database.Delete.UserRight(user_id=user.id)
                    db.session.delete(user)
                    db.session.commit()

                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(user_id, 'User')

            # massive deletion
            if team_id:
                users: List[User] = User.query.filter(User.team_id == team_id).all()
                for user in users:
                    Database.Delete.UserRight(user_id=user.id)
                    db.session.delete(user)
                db.session.commit()

        @staticmethod
        def Right(right_id: Optional[int], team_id: Optional[int]) -> HTTPResponse|None:
            """Delete Right record

            Args:
                right_id : ID of the Right to delete
                team_id : ID of the Team for massive selection

            Raises:
                Exception is unit_id/company_id are None

            Returns:
                HTTPResponse value 204 on success, 404 if the Right cannot be found
            """
            if (right_id is None) and (team_id is None):
                raise Exception("Both right_id and team_id are None in Delete::Right.")

            if right_id:
                right: Right = Right.query.filter(Right.id == right_id).first()
                if right:
                    Database.Delete.UserRight(right_id=right_id)
                    db.session.delete(right)
                    db.session.commit()

                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(right_id, 'Right')

            # massive deletion
            if team_id:
                rights: List[Right] = Right.query.filter(Right.team_id == team_id).all()
                for right in rights:
                    Database.Delete.UserRight(right_id=right.id)
                    db.session.delete(right)
                db.session.commit()

        @staticmethod
        def UserRight(usrg_id: Optional[int] = None, user_id: Optional[int] = None, right_id: Optional[int] = None) -> None:
            """Delete UserRight record either from a user_id or right_id

            Args:
                usrg_id : ID of the UserRight to delete
                user_id : ID of the user for which the relation should be removed
                right_id: ID of the right for which the relation should be removed

            Raises:
                Exception is unit_id/company_id are None
            """

            # nothing to do
            if (usrg_id is None) and (user_id is None) and (right_id is None):
                raise Exception("All usrg_id, user_id and right_id are None in Delete::UserRight.")

            if usrg_id:
                usrg: UserRight = UserRight.query.filter(UserRight.id == usrg_id).first()
                if usrg:
                    db.session.delete(usrg)
                    db.session.commit()

                    return HTTPResponse.noContent()
                else:
                    return HTTPResponse.error404(usrg_id, 'UserRight')

            if user_id:
                users: List[UserRight] = UserRight.query.filter(UserRight.user_id == user_id).all()
                for user in users:
                    db.session.delete(user)
                db.session.commit()

            if right_id:
                rights: List[UserRight] = UserRight.query.filter(UserRight.right_id == right_id).all()
                for right in rights:
                    db.session.delete(right)
                db.session.commit()
