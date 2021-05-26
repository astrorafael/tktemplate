# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------


# ---------------
# Twisted imports
# ---------------

from twisted.logger import Logger
from twisted.enterprise import adbapi


from twisted.internet import reactor, task, defer
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.threads import deferToThread

#--------------
# local imports
# -------------

from tktemplate import SQL_SCHEMA, SQL_INITIAL_DATA_DIR
from tktemplate.logger import setLogLevel
from tktemplate.dbase import tables

# ----------------
# Module constants
# ----------------

NAMESPACE = 'DBASE'

# -----------------------
# Module global variables
# -----------------------

log = Logger(NAMESPACE)

# ------------------------
# Module Utility Functions
# ------------------------


# --------------
# Module Classes
# --------------

class DataAccesObject():

    def __init__(self, pool, *args, **kargs):
        setLogLevel(namespace=NAMESPACE, levelStr='info')
        self.pool = pool
        self.start(*args)
        
       
    #------------
    # Service API
    # ------------

    def start(self, cfg_dbg):
        log.info('starting DAO')

        self.config = tables.ConfigTable(
            pool      = self.pool,
            log_level = cfg_dbg,
        )
        
        