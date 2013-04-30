#!/usr/bin/env python

import socket, sys

# create a new, blank socket object. Nothing is assigned about it right now except that it's TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the hostname if passed in as an argumet, otherwise use localhost
HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
# Use the polestar port, because it's unlikely that you're using it for real
PORT = 1060

def recv_all(sock, length):
    pass






if sys.argv[1:] == ['server']:
    # at the SOL_SOCKET level, set the SO_REUSEADDR flag to a value of 1.
    # this is the maximum number of connections that our server will accept.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)