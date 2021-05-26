# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

import os
import sys
import argparse

# ---------------
# Twisted imports
# ---------------

from twisted.logger   import Logger
from twisted.internet import  tksupport, reactor, defer, task
from twisted.application.service import Service
from twisted.internet.defer import inlineCallbacks

# -------------------
# Third party imports
# -------------------


#--------------
# local imports
# -------------

from tktemplate import __version__
from tktemplate.logger  import startLogging, setLogLevel
from tktemplate.dbase.service   import DatabaseService
from tktemplate.gui.application import Application
from tktemplate.controller.application import ApplicationController

# ----------------
# Module constants
# ----------------

NAMESPACE = 'CTRL '

# -----------------------
# Module global variables
# -----------------------

log = Logger(namespace=NAMESPACE)

# ------------------------
# Module Utility Functions
# ------------------------

def createParser():
    # create the top-level parser
    name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
    parser    = argparse.ArgumentParser(prog=name, description='AZOTEA GUI')

    # Global options
    parser.add_argument('--version', action='version', version='{0} {1}'.format(name, __version__))
    parser.add_argument('--console', action='store_true',  help='log to console.')
    return parser


# --------------
# Module Classes
# --------------

class GraphicalService(Service):

    NAME = NAMESPACE

    # Default subscription QoS
    

    def __init__(self, **kargs):
        super().__init__()
        self.options = createParser().parse_args(sys.argv[1:])
        startLogging(console=self.options.console)
        setLogLevel(namespace=NAMESPACE, levelStr='info')
        self.task    = task.LoopingCall(self.heartBeat)
    
    @inlineCallbacks
    def quit(self):
         yield self.parent.stopService()
         reactor.stop()


    # -----------
    # Service API
    # -----------
    
    def startService(self):
        log.info('starting Graphical User Interface')
        super().startService()
        self.application = Application()
        self.dbaseService = self.parent.getServiceNamed(DatabaseService.NAME)
        self.controllers = (
            ApplicationController(
                parent  = self, 
                view    = self.application, 
                model   = self.dbaseService.dao,
            ),
        )

        # synchronous start
        for controller in self.controllers[1:]:
            controller.start()        

        tksupport.install(self.application)
        self.task.start(3, now=False)           # call every T seconds
        # application start is deferred untill all controllers have started
        reactor.callLater(0, self.controllers[0].start)
        

    def stopService(self):
        log.info('stopping Graphical User Interface Service')
        self.task.stop()
        return super().stopService()


    # -----------------
    # Configuration API
    # -----------------

    def configure(self, **kwargs):
        '''Configuration from command line arguments'''
        pass

    # ---------
    # Heartbeat
    # ---------

    def heartBeat(self):
        '''Oly for dubugging purposes'''
        log.info('Tick')