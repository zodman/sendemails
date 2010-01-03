#!/usr/bin/env python
# -*- mode:Python; tab-width: 4 -*-
from __future__ import generators
"""Simulate an SMTP server for debugging purposes.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

__author__ = "Grzegorz Adam Hankiewicz <gradha@efaber.net>"
__date__ = "June 2003"
__version__ = "$Revision: 1.1 $"
__credits__ = ""

SUCCESSFUL_EXIT = 0
DEFAULT_PORT_NUMBER = 8007

import os
import sys
try:
    from twisted.protocols.smtp import SMTP, SMTPFactory
    from twisted.internet import reactor
except ImportError, msg:
    print msg
    print "Sorry, you need Twisted from http://www.twistedmatrix.com/products/twisted"
    sys.exit(1)

class Server(SMTP):
    def connectionMade(self):
        SMTP.connectionMade(self)
        self.data_mode = 0
       
        
    def lineReceived(self, line):
        if self.data_mode:
            if line == ".":
                self.sendCode(250, "Ok")
                self.data_mode = 0
            else:
                print line
             
        else:
            if line[:4].lower() == "quit":
                self.sendCode(221, "Bye bye")
                self.transport.loseConnection()
                
            if line[:4].lower() == "data":
                self.data_mode = 1
                self.sendCode(354, "Go ahead")
            else:
                self.sendCode(250, "Ok")


def usage_information(binary_name = "fake_SMTP_server.py", exit_code = SUCCESSFUL_EXIT):
    """Prints usage information and terminates execution."""
    print """Usage: %s [-hv -p port_number]

-h, --help
    Print this help screen.
-v, --version
    Print version number and exit.
-p xxx, --port-number xxx
    Use xxx as port number to listen incoming SMTP connections.
    
Usage example:
 %s -p 12345
""" % (binary_name, binary_name)
    sys.exit(exit_code)


def process_command_line(argv = None):
    """Extracts from argv the options and returns them in a tuple.

    This function is a command line wrapper against main_process,
    it returns a tuple which you can `apply' calling main_process. If
    something in the command line is missing, the program will exit
    with a hopefully helpfull message.

    args should be a list with the full command line. If it is None
    or empty, the arguments will be extracted from sys.argv. The
    correct format of the accepted command line is documented by
    usage_information.
    """
    import getopt
    if not argv:
        argv = sys.argv

    short = "hvp:"
    long = ["help", "version", "port-number="]

    try:
        opts, args = getopt.getopt(argv[1:], short, long)
    except getopt.GetoptError, msg:
        print "Error processing command line: %s\n" % msg
        usage_information(2)

    port_number = DEFAULT_PORT_NUMBER

    for option, value in opts:
        if option in ("-h", "--help"):
            usage_information()
        elif option in ("-v", "--version"):
            print __version__[11:-1]
            sys.exit(SUCCESSFUL_EXIT)
        elif option in ("-p", "--port-number"):
            port_number = int(value)

    # tell the user what options did (s)he choose
    print "I'll be listening port number %d" % port_number
    return (port_number,)


def main_process(port_number):
    # Next lines are magic:
    factory = SMTPFactory()
    #factory = Factory()
    factory.protocol = Server
    factory.timeout = 200
    # listen incoming emails
    reactor.listenTCP(port_number, factory)
    reactor.run()


if __name__ == "__main__":
    args = process_command_line()
    main_process(*args)
    print "Done"

