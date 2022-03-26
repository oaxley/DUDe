# -*- coding: utf-8 -*-
# vim: set ft=Makefile
#
# This source file is subject to the Apache License 2.0
# that is bundled with this package in the file LICENSE.txt.
# It is also available through the Internet at this address:
# https://opensource.org/licenses/Apache-2.0
#
# @author	Sebastien LEGRAND
# @license	Apache License 2.0
#
# @brief	Makefile to create SSL certificates

#
# globals
#
ifndef SERVER_NAME
SERVER_NAME = my_dev_site
endif

#
# Root Certificate Authority
#

# create the root private key (this key has no password!)
root_key:
	@echo "Creating the private root key (root_ca.key.pem)"
	@mkdir -p root
	@openssl genrsa -out root/root_ca.key.pem 4096 >/dev/null 2>&1

# create the root certificate
root_ca: root_key
	@echo "Creating the root certitficate (root_ca.cert.pem)"
	@openssl req -x509 -new -nodes -sha256 -days 365 \
		-key root/root_ca.key.pem \
		-subj /CN=Root_CA/ \
		-out root/root_ca.cert.pem

#
# Server certificate
#

# create the private key for the server
server_key:
	@echo "Creating server private key ($(SERVER_NAME).key.pem)"
	@openssl genrsa -out $(SERVER_NAME).key.pem 2048 >/dev/null 2>&1

# create the signing request
server_csr:
	@echo "Creating server signing request ($(SERVER_NAME).csr)"
	@openssl req -new -key $(SERVER_NAME).key.pem -out $(SERVER_NAME).csr -subj '/CN=ACME Development Server/'

# sign the request with the root certificate
server_cert: server_key server_csr
	@echo "Creating server certificate $(SERVER_NAME).cert.pem"

	@echo "\
authorityKeyIdentifier=keyid,issuer\n\
basicConstraints=CA:FALSE\n\
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment\n\
subjectAltName = @alt_names\n\
[alt_names]\n\
DNS.1 = localhost\n" > $(SERVER_NAME).ext

	@openssl x509 -req -days 365 -sha256 \
	-extfile $(SERVER_NAME).ext \
	-CA root/root_ca.cert.pem -CAkey root/root_ca.key.pem -CAcreateserial \
	-in $(SERVER_NAME).csr \
	-out $(SERVER_NAME).cert.pem >/dev/null 2>&1

	@rm -f $(SERVER_NAME).ext $(SERVER_NAME).csr
