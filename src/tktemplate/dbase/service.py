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
import sqlite3
import glob


# ---------------
# Twisted imports
# ---------------

from twisted.application.service import Service
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
from tktemplate.dbase.dao import DataAccesObject

# ----------------
# Module constants
# ----------------

NAMESPACE = 'DBASE'

DATABASE_FILE = 'template.db'

SQL_TEST_STRING = "SELECT COUNT(*) FROM config_t"

# -----------------------
# Module global variables
# -----------------------

log = Logger(NAMESPACE)

# ------------------------
# Module Utility Functions
# ------------------------

def getPool(*args, **kargs):
    '''Get connetion pool for sqlite3 driver'''
    kargs['check_same_thread'] = False
    return adbapi.ConnectionPool("sqlite3", *args, **kargs)


def open_database(dbase_path):
    '''Creates a Database file if not exists and returns a connection'''
    output_dir = os.path.dirname(dbase_path)
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(dbase_path):
        with open(dbase_path, 'w') as f:
            pass
        log.info("Created database file {0}".format(dbase_path))
    return sqlite3.connect(dbase_path)


def create_database(connection, schema_path, initial_data_dir_path, query, updates_data_dir=None,):
    created = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception:
        created = False
    if not created:
        with open(schema_path) as f: 
            lines = f.readlines() 
        script = ''.join(lines)
        connection.executescript(script)
        log.info("Created data model from {0}".format(os.path.basename(schema_path)))
        file_list = glob.glob(os.path.join(initial_data_dir_path, '*.sql'))
        for sql_file in file_list:
            log.info("Populating data model from {0}".format(os.path.basename(sql_file)))
            with open(sql_file) as f: 
                lines = f.readlines() 
            script = ''.join(lines)
            connection.executescript(script)
    elif updates_data_dir:
        file_list = glob.glob(os.path.join(updates_data_dir, '*.sql'))
        for sql_file in file_list:
            log.info("Applying updates to data model from {0}".format(os.path.basename(sql_file)))
            with open(sql_file) as f: 
                lines = f.readlines() 
            script = ''.join(lines)
            connection.executescript(script)
    connection.commit()

def read_database_version(connection):
    cursor = connection.cursor()
    query = 'SELECT value FROM config_t WHERE section = "database" AND property = "version";'
    cursor.execute(query)
    version = cursor.fetchone()[0]
    return version


# --------------
# Module Classes
# --------------

class DatabaseService(Service):

    # Service name
    NAME = NAMESPACE

    def __init__(self, **kargs):
        super().__init__()   
        setLogLevel(namespace=NAMESPACE, levelStr='info')
        self.path = None
        self.pool = None
        self.preferences = None
        self.getPoolFunc = getPool
    
    def foreign_keys(self, flag):
        def _foreign_keys(txn, flag):
            value = "ON" if flag else "OFF"
            sql = f"PRAGMA foreign_keys={value};"
            txn.execute(sql)
        return self.pool.runInteraction(_foreign_keys, flag)

    #------------
    # Service API
    # ------------

    def startService(self):
        self.path = os.path.join(os.getcwd(), DATABASE_FILE)
        log.info("starting Database Service on {database}", database=self.path)
        connection = open_database(self.path)
        create_database(connection, SQL_SCHEMA, SQL_INITIAL_DATA_DIR, SQL_TEST_STRING)
        version = read_database_version(connection)
        # Remainder Service initialization
        super().startService()
        connection.commit()
        connection.close()
        self.openPool()
        cfg_dbg="info"
        self.dao = DataAccesObject(self.pool, cfg_dbg)
        self.dao.version = version
        return self.foreign_keys(True)


    def stopService(self):
        #self.closePool()
        log.info("Stopping Database Service")
        return super().stopService()


    # -----------------
    # Configuration API
    # -----------------

    def configure(self, **kwargs):
        '''Configuration from command line arguments'''
        pass

    # ---------------
    # OPERATIONAL API
    # ---------------

    

    # =============
    # Twisted Tasks
    # =============
   
        

      
    # ==============
    # Helper methods
    # ==============

    def openPool(self):
        # setup the connection pool for asynchronouws adbapi
        log.info("Opening a DB Connection to {conn!s}", conn=self.path)
        self.pool  = self.getPoolFunc(self.path)
        log.info("Opened a DB Connection to {conn!s}", conn=self.path)


    def closePool(self):
        '''setup the connection pool for asynchronouws adbapi'''
        log.info("Closing a DB Connection to {conn!s}", conn=self.path)
        self.pool.close()
        log.info("Closed a DB Connection to {conn!s}", conn=self.path)
