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
# @brief	Strings for the en_US locale

#----- Imports
from __future__ import annotations
from typing import Dict


#----- Globals

messages: Dict[int, str] = {
    # 0xxxh: Admin messages
    0x0001: "X-API-TOKEN for administrative endpoints is [{apikey}].",
    0x0002: "DUDE_SECRET_KEY is not defined. Please fix this and restart.",

    # 1xxxh: HTTP 1xx messages

    # 2xxxh: HTTP 2xx messages
    0x2000: "User is authorized.",

    # 3xxxh: HTTP 3xx messges

    # 4xxxh: HTTP 4xx messges

    ## 400x: Bad Request
    0x4000: "Could not update the field '{key}'.",
    0x4001: "Field '{name}' is missing from the input data.",
    0x4002: "{child} is already existing for this {parent}.",
    0x4003: "{name} already exists.",
    0x4004: "Field '{name}' cannot be converted to a '{type}'.",
    0x4005: "Not able to update field '{name}'.",
    0x4006: "Association not authorized between two different teams.",

    ## 401x: Unauthorized (ie unauthenticated)
    0x4010: "Token has expired.",
    0x4011: "Token contains invalid data.",
    0x4012: "Token is missing.",

    ## 403x: Forbidden
    0x4030: "User is not authorized to perform the operation.",

    ## 404x: Not Found
    0x4040: "Could not find {name} with the parameters provided.",
    0x4041: "Could not find {table} with ID #{rid}.",
    0x4042: "{parent} has no {child} with ID #{rid}",

    ## 405x: Method not allowed
    0x4050: "Method not allowed.",

    # 25xxh: HTTP 5xx messges

    ## 500x: Internal Server Error
    0x5000: "Internal Server Error.",
    0x5001: "{trace}"
}
