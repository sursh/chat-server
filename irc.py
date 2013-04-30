#!/usr/bin/env python
# working on a simple chat client

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060

# this is a stupid name for this method
def recv_all(sock, length):
    ''' Receives the first 'length' chars of a message from 'sock'. '''
    data = ''

    # stop when we've collected 'length' chars of message
    while len(data) < length:

        more = sock.recv(length - len(data))

        # if we're out of incoming data, we're done, close the socket!
        if not more:
            raise EOFError('socket closed %d chars into a %d-char message' % (len(data), length))

        # and append this most recent bit to the whole message we've received so far
        data += more

        # and here's your final message!
    return data

if sys.argv[1:] == ['server']:

    # TODO: allow more than 1 client to connect at a time
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1) # TODO: here too

    print 'Listening at', s.getsockname()

    while True:

        sc, sockname = s.accept()
        print 'We have accepted a connection from', sockname
        print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()

        # TODO accept more than 16 chars
        message = recv_all(sc, 16)
        print 'The incoming message says', repr(message)

        # TODO broadcast new message to all clients

        print 'Still listening at', s.getsockname()

else:
    print >>sys.stderr, 'Usage: $ %s server [host]' % sys.argv[0]
