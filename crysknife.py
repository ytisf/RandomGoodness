#!/usr/bin/env python

import sys
import base64
import datetime

from twisted.internet import protocol, reactor

# Proxy - Server running this script.
# Server - Server which the requests go to.
# Client - Machine connecting to the server through the proxy.

LISTEN_PORT = 8000
SERVER_PORT = 80
SERVER_ADDR = "morirt.com"
SEP = ";"


def _time():
    return str(datetime.datetime.now())

def _assemble_line(code_source, code_dest, src_ip, src_port, dest_host, dest_port, data=""):
    this = _time() + SEP
    this += code_source + SEP
    this += code_dest + SEP
    this += "%s:%s%s" % (src_ip, src_port, SEP)
    this += "%s:%s%s" % (dest_host, dest_port, SEP)
    if "GET /" in data[:20]:
        this += "http_request_get" + SEP
    elif "POST /" in data[:20]:
        this += "http_request_post" + SEP
    else:
        this += "unknown" + SEP
    if data != "":
        this += base64.b64encode(data)
    this += SEP + "\n"
    return this

LOGFILE_NAME = "recent.log"
LOGFILE = open(LOGFILE_NAME, 'wb')



# Stolen from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    # Client => Proxy
    def dataReceived(self, data):
        if self.client:
            # data is the request (from client to proxy)
            self.client.write(data)
        else:
            # data is the HTTP respose
            host_ip = self.transport.getHost().host
            host_port = self.transport.getHost().port
            peer_ip = self.transport.getPeer().host
            peer_port = self.transport.getPeer().port
            w = _assemble_line(code_source="Client", code_dest="Proxy", src_ip=peer_ip, src_port=peer_port, dest_host=host_ip, dest_port=host_port, data=data)
            LOGFILE.write(w)

            print "[.]\t1.) [%s] Client (%s:%s) --> Proxy (%s:%s) with length %s." % (
                _time(), peer_ip, peer_port, host_ip, host_port, len(data)
            )
            self.buffer = data

    # Proxy => Client
    def write(self, data):
        host_ip = self.transport.getHost().host
        host_port = self.transport.getHost().port
        peer_ip = self.transport.getPeer().host
        peer_port = self.transport.getPeer().port
        w = _assemble_line(code_source="Proxy", code_dest="Client", src_ip=host_ip, src_port=host_port, dest_host=peer_ip, dest_port=peer_port, data=data)
        LOGFILE.write(w)

        print "[.]\t4.) [%s] Proxy (%s:%s) --> Client (%s:%s) with length %s." % (
            _time(), host_ip, host_port, peer_ip, peer_port, len(data)
        )
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    # Server => Proxy
    def dataReceived(self, data):
        host_ip = self.transport.getHost().host
        host_port = self.transport.getHost().port

        w = _assemble_line(code_source="Server", code_dest="Proxy", src_ip=SERVER_ADDR, src_port=SERVER_PORT, dest_host=host_ip, dest_port=host_port, data=data)
        LOGFILE.write(w)

        print "[.]\t3.) [%s] Server (%s:%s) --> Proxy (%s:%s) with length %s." % (
            _time(), SERVER_ADDR, SERVER_PORT, host_ip, host_port, len(data)
        )
        self.factory.server.write(data)

    # Proxy => Server
    def write(self, data):
        if data:
            host_ip = self.transport.getHost().host
            host_port = self.transport.getHost().port
            peer_ip = self.transport.getPeer().host
            peer_port = self.transport.getPeer().port

            w = _assemble_line(code_source="Proxy", code_dest="Server", src_ip=host_ip, src_port=host_port, dest_host=peer_ip, dest_port=peer_port, data=data)
            LOGFILE.write(w)

            print "[.]\t2.) [%s] Proxy (%s:%s) --> Server (%s:%s) with length %s." % (
                _time(), host_ip, host_port, peer_ip, peer_port, len(data)
            )
            self.transport.write(data)


def main():
    sys.stdout.write("\n\t--- crysknife desert ---\n\n")
    sys.stdout.write("\tSettings: %s:%s-->%s:%s.\n" % ("0.0.0.0", LISTEN_PORT, SERVER_ADDR, SERVER_PORT))
    sys.stdout.write("\tStarting at: %s.\n" % _time())
    sys.stdout.write("\tLogfile: %s.\n\n" % LOGFILE_NAME)
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        LOGFILE.close()
        exit()
