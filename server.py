#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor SIP en UDP simple
"""

import SocketServer
import sys
import os


class SipHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class(INVITE,ACK y BYE)
    """
    def handle(self):

        while 1:
            line = self.rfile.read()
            if not line:
                break
            print line
            line = line.split(" ")
            method = line[0]
            ip_clt = str(self.client_address[0])
            if "SIP/2.0\r\n\r\n" not in line:
                self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n")
            elif method == "INVITE":
                self.wfile.write("SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write("SIP/2.0 180 Ringing-\r\n\r\n")
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            elif method == "ACK":
                run = ('./mp32rtp -i ' + ip_clt + ' -p 23032 < ' + fich_audio)
                os.system(run)
                print run
            elif method == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            else:
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[2])
    fich_audio = sys.argv[3]
    try:
        serv = SocketServer.UDPServer(("", PORT), SipHandler)
    except (IndexError, ValueError):
        sys.exit("Usage: python servidor.py IP port audio_file")
    print "Listening...."
    serv.serve_forever()
