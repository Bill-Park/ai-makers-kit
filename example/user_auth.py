#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc
import os
import datetime
import hmac
import hashlib


# Config for GiGA Genie gRPC
CLIENT_ID = 'Y2xpZW50X2lkMTU1NDY5MDI4ODEzOQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTQ2OTAyODgxMzk='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTQ2OTAyODgxMzk='

### COMMON : Client Credentials ###
def getMetadata():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + timestamp

    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

    metadata = [('x-auth-clientkey', CLIENT_KEY),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]

    return metadata

def credentials(context, callback):
    callback(getMetadata(), None)

def getCredentials():
    with open('../data/ca-bundle.pem', 'rb') as f:
        trusted_certs = f.read()

    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    authCred = grpc.metadata_call_credentials(credentials)

    return grpc.composite_channel_credentials(sslCred, authCred)

### END OF COMMON ###
