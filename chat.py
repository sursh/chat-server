#!/usr/bin/env python
# working on a simple chat client

'''
TODO
[x] implement master queue and boilerplate for sender method
[x] use child threads instead of objects
[x] get client messages onto the queue and just print out incoming messages
[x] implement message sending to all clients
[-] add data structure to keep track of users
[x]     add Message class: contains port, text, nickname, date.
[x]     Add nickname to Putter init function
[x]     don't send me my own message
[x]     pass along sender info as well as the message
[ ]     display sender name to other clients
[ ] display "there are X other users" when you log in
[ ] refactor: move masterQueue to attribute on MasterSender
[ ] handle clients quitting more gracefully - broken pipe on line 56
'''

import sys
import socket
import Queue
import threading
import datetime

HOST = '127.0.0.1'
PORT = 1060
NUM_CLIENTS = 10

DEBUG = True

# Message queue from all clients
masterQueue = Queue.Queue()


# DEFINE MASTER SENDER
class MasterSender(threading.Thread):
    ''' Pull messages off the masterQueue and send to all clients. '''
    def __init__(self, queue, activeClients):
        threading.Thread.__init__(self)
        self.queue = queue
        self.activeClients = activeClients

    def run(self):
        broadcast = ''
        while True:
            message = self.queue.get()
            for (_id, clientsock) in self.activeClients.iteritems():
                # don't send me back my own message
                if message.address != clientsock.getpeername():
                    broadcast = "%s: %s" % (message.nickname, message.body)
                    clientsock.send(broadcast)


# DEFINE MESSAGE PUTTER (from user -> masterQueue)
class Putter(threading.Thread):
    ''' Get messages from user and put on masterQueue. '''

    def __init__(self, queue, sock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.sock = sock
        self.nickname = ''

    def run(self):
        self.sock.send('What\'s your handle? ')
        self.nickname = recv_all(self.sock, 50).strip()

        print "%s has just signed in on port %s." % (self.nickname, self.sock.getpeername())
        while True:
            self.sock.send('> ') # client's chat prompt
            body = recv_all(self.sock, 1000)
            masterQueue.put(Message(self.nickname, body, self.sock))


class Message():
    ''' Individual chat messages from users. '''

    def __init__(self, nickname, body, sock):
        ''' Sending the nickname with the message, instead of a server-side lookup,
            in case a client leaves before their message is served to the other clients. '''
        self.nickname    = nickname
        self.body        = body
        self.address     = sock.getpeername()


# DEFINE MESSAGE GETTER
class Getter(threading.Thread):
    ''' Pulls messages from this client's queue and sends to user. '''
    pass


def recv_all(sock, length):
    ''' Receives the first 'length' chars of a message from 'sock'. '''

    data = ''
    more = sock.recv(length)
    data += more

    return data


def main():

    activeClients = {}

    try:
        # initialize passive socket at PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, NUM_CLIENTS)
        s.bind((HOST, PORT))

        # TODO create master sender
        ms = MasterSender(masterQueue, activeClients)
        ms.setDaemon(True) # ?
        ms.start()

        while True:
            s.listen(NUM_CLIENTS)
            print 'Listening for connections at', s.getsockname()

            sock, sockname = s.accept()
            c = Putter(masterQueue, sock)
            c.setDaemon(True)
            c.start()
            activeClients[sock.fileno()] = sock

    except KeyboardInterrupt:
        # this is broken, will fix later
        # sc.send('!!! Server shutting down.\n')
        print "\nKthxbai, shutting down servers."
        # sc.close()

if __name__ == '__main__':
    main()

