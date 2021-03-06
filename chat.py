#!/usr/bin/env python
# Sasha Laundy, 2013

'''

Simple Python chat server with threads and queues.
See README for lots more info.

'''

import sys
import socket
import Queue
import threading
import datetime

HOST = '127.0.0.1'
PORT = 1060
MSG_SIZE = 4096

masterQueue = Queue.Queue()

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


class Putter(threading.Thread):
    ''' Get messages from user and put on masterQueue. '''

    def __init__(self, queue, sock, usercount):
        threading.Thread.__init__(self)
        self.queue = queue # master queue
        self.sock = sock
        self.nickname = ''
        self.usercount = usercount

    def run(self):
        self.sock.send('There are %d users already chatting. \nYour handle: ' % self.usercount)
        self.nickname = recv_all(self.sock).strip()
        print "%s has just signed in on port %s." % (self.nickname, self.sock.getpeername())

        while True:
            self.sock.send('> ') # client's chat prompt
            body = recv_all(self.sock)
            masterQueue.put(Message(self.nickname, body, self.sock))


class Message():
    ''' Individual chat messages from users. '''

    def __init__(self, nickname, body, sock):
        ''' Sending the nickname with the message, instead of a server-side lookup,
            in case a client leaves before their message is served to the other clients. '''
        self.nickname    = nickname
        self.body        = body
        self.address     = sock.getpeername()


def recv_all(sock):
    ''' Receives the first 'length' chars of a message from 'sock'. '''

    message = sock.recv(MSG_SIZE)
    return message


def main():

    activeClients = {}

    try:
        # initialize passive/listening socket at PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))

        ms = MasterSender(masterQueue, activeClients)
        ms.setDaemon(True)
        ms.start()

        while True:
            s.listen(100)
            print 'Listening for connections at', s.getsockname()

            sock, sockname = s.accept()
            c = Putter(masterQueue, sock, len(activeClients))
            c.setDaemon(True)
            c.start()
            activeClients[sock.fileno()] = sock

    except KeyboardInterrupt:
        print "\nKthxbai, closing sockets."
        for sock in activeClients.values():
            sock.send('\nSorry, server shutting down now.\n')
            sock.close()

if __name__ == '__main__':
    main()

