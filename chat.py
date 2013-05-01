#!/usr/bin/env python
# working on a simple chat client

# TODO
# dejank the readin function
# add data structure to keep track of users

import socket, sys

HOST = '127.0.0.1'
PORT = 1060

def recv_all(sock, length):
    ''' Receives the first 'length' chars of a message from 'sock'. '''

    data = ''
    more = sock.recv(length)
    # if we're out of incoming data, we're done, close the socket!
    if not more:
        raise EOFError('socket closed %d chars into a %d-char message' % (len(data), length))
    data += more
    return data

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: allow more than 1 client to connect at a time
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
        s.bind((HOST, PORT))
        s.listen(2) # TODO: here too

        print 'Listening for connections at', s.getsockname()
        sc, sockname = s.accept()

        while True:
            sc.send('> ') # client's chat prompt
            message = recv_all(sc, 1000)
            print '%s says: %s' % (sc.getpeername(), str(message))

            # TODO broadcast new message to all clients
    except KeyboardInterrupt:
        sc.send('!!! Server shutting down.\n')
        print "\nKthxbai, shutting down servers."
        sc.close()

if __name__ == '__main__':
  main()

