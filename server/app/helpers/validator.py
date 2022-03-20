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
# @brief	Class to validate input data and parameters

#----- Imports
from __future__ import annotations
from typing import Any, List, Dict, Tuple

from flask import Request


#----- Class

class Validator:
    """This class regroups all the methods to validate inputs data or parameters"""

    @staticmethod
    def data(input: Dict[str, Any], fields: List[str]) -> None:
        """Validate input JSON data

        Args:
            input: the json input
            fields: the list of fields that should be present in the input

        Raises:
            'KeyError' if a field is missing from the the input
        """
        for field in fields:
            if field not in input:
                raise KeyError(field)

    @staticmethod
    def parameters(request: Request, fields: List[Tuple[str, Any]]):
        """Validate input parameters from query

        Args:
            request: the HTTP request
            fields: a list of Tuple with the name of the parameter and its default value

        Raises:
            'ValueError' if the parameter cannot be cast to a proper value

        Returns:
            a Dict[str, Any] with the parameter values
        """
        results: Dict[str, Any] = {}
        for field, default in fields:
            value = request.args.get(field)

            if value is None:
                results[field] = default
            else:
                if type(default) is int:
                    try:
                        results[field] = int(value)
                        continue
                    except ValueError:
                        raise ValueError((field, 'int'))

                if type(default) is str:
                    try:
                        results[field] = str(value)
                        continue
                    except ValueError:
                        raise ValueError((field, str))

                if type(default) is bool:
                    results[field] = bool(value)
                    continue

        return results
