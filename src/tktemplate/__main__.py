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


# ---------------
# Twisted imports
# ---------------

from twisted.internet import reactor
from twisted.application import service

#--------------
# local imports
# -------------

from tktemplate.controller.service import GraphicalService
from tktemplate.dbase.service      import DatabaseService


# ----------------
# Module constants
# ----------------

# -----------------------
# Module global variables
# -----------------------

# -------------------
# Applcation assembly
# -------------------

application = service.Application("tktemplate")

dbaseService = DatabaseService()
dbaseService.setName(DatabaseService.NAME)
dbaseService.setServiceParent(application)

guiService = GraphicalService()
guiService.setName(GraphicalService.NAME)
guiService.setServiceParent(application)


# Start the ball rolling
service.IService(application).startService()
reactor.run()