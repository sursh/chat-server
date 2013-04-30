#!/usr/bin/env python

import socket, sys

# create a new, blank socket object. Nothing is assigned about it right now except that it's TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the hostname if passed in as an argumet, otherwise use localhost
HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
# Use the polestar port, because it's unlikely that you're using it for real
PORT = 1060

def recv_all(sock, length):
    ''' Passes messages length bytes at a time into sock. '''
    data = ''
    while len(data) < length:
        # grab the next 'length' of incoming data
        more = sock.recv(length - len(data))

        # if we're out of incoming data, close the socket:
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))

        # add 'more' to the list of data already sent
        data += more
    return data

if sys.argv[1:] == ['server']:

    # at the SOL_SOCKET level, set the SO_REUSEADDR flag to a value of 1.
    # this is the maximum number of connections that our server will accept.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to the host and port. At this point, OS still doesn't know
    # if this is an active or passive port
    s.bind((HOST, PORT))

    # now we've committed - it's a passive port! With a max number of connections of 1
    s.listen(1)

    while True:
        print 'Listening at', s.getsockname()

        # sc is a connection object used for send/receive data
        # sockname is the socket address on the other end of the connection (so, the client)
        sc, sockname = s.accept()
        print 'We have accepted a connection from', sockname

        # sc.getpeername() == s.getsockname(). This is the active port that's created
        #  for this particular client
        print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()

        # this is a homebrewed method, defined above
        #
        message = recv_all(sc, 16)
        print 'The incoming sixteen-octet message says', repr(message)

        # Send all the data until it's done sending, then close the socket
        sc.sendall('Farewell, client')
        sc.close()
        print 'Reply sent, socket closed'

else:
    print >>sys.stderr, 'Usage: $ %s server [host]' % sys.argv[0]
