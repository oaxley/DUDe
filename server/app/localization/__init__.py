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
# @brief	Main file to provide internalization messages

#----- Imports
from __future__ import annotations

import locale
import importlib

from app import app


#----- Globals

# try to load the file corresponding to the current locale
try:
    locale_name, _ = locale.getlocale()
    module = importlib.import_module(f"app.localization.{locale_name}")

# by default we load the en_US locale
except ModuleNotFoundError:
    module = importlib.import_module(f"app.localization.{app.config['DEFAULT_LOCALE']}")

# export all the messages
messages = module.messages


#----- Functions

# function to return a localized string
def getMessage(msg_id: int, **kwargs) -> str:
    """Return the localized version of a string

    Args:
        msg_id: the ID of the message to retrieve
        kwargs: list of keyword arguments for the message if any

    Raises:
        KeyError if the msg ID is not present in the localized messages dictionary

    Returns:
        The localised string
    """
    if msg_id not in messages:
        raise Exception(f"Could not find message #{msg_id} in the list of messages.")

    return messages[msg_id].format(**kwargs)
