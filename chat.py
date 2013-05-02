#!/usr/bin/env python
# working on a simple chat client

'''
TODO
[x] implement master queue and boilerplate for sender method
[ ] use child threads instead of objects
[ ] get client messages onto the queue and just print out incoming messages
[ ] implement message sending to all clients except sender
[ ] pass along sender info as well as the message
[ ] add data structure to keep track of users
'''

import sys
import socket
import Queue
import threading

HOST = '127.0.0.1'
PORT = 1060
NUM_CLIENTS = 10

DEBUG = True

# Message queue from all clients
masterQueue = Queue.Queue()


# DEFINE MASTER SENDER
class MasterSender(threading.Thread):
    ''' Pull messages off the masterQueue and send to all clients. '''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        if DEBUG: print "You just initialized a master sender."


# DEFINE MESSAGE PUTTER (from user -> masterQueue)
class Putter(threading.Thread):
    ''' Get messages from user and put on masterQueue. '''
    def __init__(self, queue, sock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.sock = sock

    def run(self):
        print "You just initialized a client object", self.sock.getpeername()


# DEFINE MESSAGE GETTER
class Getter(threading.Thread):
    ''' Pulls messages from this client's queue and sends to user. '''
    pass

def recv_all(sock, length):
    ''' Receives the first 'length' chars of a message from 'sock'. '''

    data = ''
    more = sock.recv(length)
    if not more:
        raise EOFError('socket closed %d chars into a %d-char message' % (len(data), length))
    data += more
    return data


def main():
    try:
        # initialize passive socket at PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, NUM_CLIENTS)
        s.bind((HOST, PORT))

        # TODO create master sender
        ms = MasterSender(masterQueue)
        ms.setDaemon(True) # ?
        ms.start()

        while True:
            s.listen(NUM_CLIENTS)
            print 'Listening for connections at', s.getsockname()

            sock, sockname = s.accept()
            c = Putter(masterQueue, sock)
            c.setDaemon(True)
            c.start()


        # TODO MOVE THIS INTO CHILD THREAD
        while True:
            sc.send('> ') # client's chat prompt
            message = recv_all(sc, 1000)
            print '%s says: %s' % (sc.getpeername(), str(message))

    except KeyboardInterrupt:
        sc.send('!!! Server shutting down.\n')
        print "\nKthxbai, shutting down servers."
        sc.close()

if __name__ == '__main__':
    main()

