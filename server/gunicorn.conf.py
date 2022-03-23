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
# @brief	Gunicorn configuration file

## Debugging
reload = False
reload_engine = 'auto'
spew = False
print_config = False

## Logging
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# loglevel = 'info'

## SSL
# keyfile = None
# certfile = None
# ssl_version = ssl.PROTOCOL_TLS
# cert_reqs = None
# ca_certs = None
# suppress_ragged_eofs = True
# do_handshake_on_connect = False
# ciphers = None

## Server Mechanics
reuse_port = True
daemon = False

## Server Socket
bind = ['0.0.0.0:5000']
