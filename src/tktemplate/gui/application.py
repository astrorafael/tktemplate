# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2020
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#################################
## APPLICATION SPECIFIC WIDGETS #
#################################

#--------------------
# System wide imports
# -------------------

import gettext
import tkinter as tk
from   tkinter import ttk
import tkinter.filedialog

# -------------------
# Third party imports
# -------------------

from pubsub import pub

# ---------------
# Twisted imports
# ---------------

from twisted.logger import Logger
from twisted.internet import reactor
from twisted.application.service import Service
from twisted.internet import defer, threads

#--------------
# local imports
# -------------

from tktemplate import __version__
from tktemplate.utils import Rect
from tktemplate.logger import setLogLevel
from tktemplate.gui.widgets.contrib import ToolTip
from tktemplate.gui.widgets.combos  import ROICombo, CameraCombo, ObserverCombo, LocationCombo
from tktemplate.gui.widgets.about import AboutDialog
from tktemplate.gui.widgets.date import DateFilterDialog
from tktemplate.gui.preferences import Preferences

from tktemplate import __version__, ABOUT_DESC_TXT, ABOUT_ACK_TXT, ABOUT_IMG, ABOUT_ICONS

# ----------------
# Module constants
# ----------------

NAMESPACE = 'GUI  '

# -----------------------
# Module global variables
# -----------------------

# Support for internationalization
_ = gettext.gettext

log  = Logger(namespace=NAMESPACE)

# -----------------
# Application Class
# -----------------

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f'TEMPLATE PROJECT {__version__}')
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.build()
        
    def quit(self):
        pub.sendMessage('file_quit')
        self.destroy()

    def start(self):
        self.menuBar.start()
        self.toolBar.start()
        self.mainArea.start()
        self.statusBar.start()
        
    def build(self):
        self.menuBar  = MenuBar(self)
        self.menuBar.pack(side=tk.TOP, fill=tk.X, expand=True,  padx=10, pady=5)
        self.toolBar = ToolBar(self)
        self.toolBar.pack(side=tk.TOP, fill=tk.X, expand=True,  padx=10, pady=5)
        self.mainArea  = MainFrame(self)
        self.mainArea.pack(side=tk.TOP, fill=tk.X, expand=True,  padx=10, pady=5)
        self.statusBar = StatusBar(self)
        self.statusBar.pack(side=tk.TOP, fill=tk.X, expand=True,  padx=10, pady=5)

    # ----------------
    # Error conditions
    # ----------------

    def messageBoxInfo(self, who, message):
        tk.messagebox.showinfo(message=message, title=who)

    def messageBoxError(self, who, message):
        tk.messagebox.showerror(message=message, title=who)

    def messageBoxWarn(self, who, message):
        tk.messagebox.showwarning(message=message, title=who)

    def messageBoxAcceptCancel(self, who, message):
        return tk.messagebox.askokcancel(message=message, title=who)

    def openDirectoryDialog(self):
        return tk.filedialog.askdirectory()

    def saveFileDialog(self, title, filename, extension):
        return tk.filedialog.asksaveasfilename(
            title            = title,
            defaultextension = extension,
            initialfile      = filename,
            parent           = self,
            )
            


class MenuBar(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build()
        self.preferences = None

    def start(self):
        # Aqui pueden ir varios pub.sendMessage a los controladores
        pass
       

    def build(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # File submenu
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_separator()
        file_menu.add_command(label=_("Quit"), command=self.quit)
        menu_bar.add_cascade(label=_("File"), menu=file_menu)

        # Options submenu
        options_menu = tk.Menu(menu_bar, tearoff=False)
        options_menu.add_separator()
        options_menu.add_command(label=_("Preferences..."), command=self.onMenuPreferences)
        menu_bar.add_cascade(label=_("Edit"), menu=options_menu)
       
        # About submenu
        about_menu = tk.Menu(menu_bar, tearoff=False)
        about_menu.add_command(label=_("Version"), command=self.onMenuAboutVersion)
        menu_bar.add_cascade(label=_("About"), menu=about_menu)
        

    def quit(self):
        '''This halts completely the main Twisted loop'''
        pub.sendMessage('file_quit')

    def doAbout(self, db_version):
        version = _("Version {0}\nDatabase version {1}").format(__version__, db_version)
        about = AboutDialog(
            title      = _("About AZOTEA"),
            version    = version, 
            descr_path = ABOUT_DESC_TXT, 
            ack_path   = ABOUT_ACK_TXT, 
            img_path   = ABOUT_IMG, 
            logos_list = ABOUT_ICONS,
        )
        about.grab_set()

    def onMenuAboutVersion(self):
        pub.sendMessage('database_version_req')

    def onMenuPreferences(self):
        preferences = Preferences(self)
        self.preferences = preferences
        preferences.grab_set()
        preferences.start()



class ToolBar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build()

    def start(self):
        pass

    def build(self):
        pass
    

class MainFrame(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build()

    def start(self):
        pass

    def build(self):
        pass
     


class StatusBar(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build()

    def start(self):
        pass

    def build(self):
        # Process status items
        self.progress = tk.IntVar()
        self.progress_ctrl= ttk.Progressbar(self, 
            variable = self.progress,
            length   = 300, 
            mode     = 'determinate', 
            orient   = 'horizontal', 
            value    = 0,
        )
        self.progress_ctrl.pack(side=tk.RIGHT, fill=tk.X)
        ToolTip(self.progress_ctrl, text=_('Current process progress'))

        self.detail = tk.StringVar()
        self.detail_ctrl = ttk.Label(self, textvariable=self.detail, justify=tk.RIGHT, width=30, borderwidth=1, relief=tk.SUNKEN)
        self.detail_ctrl.pack(side=tk.RIGHT, fill=tk.X, padx=2, pady=2)
        ToolTip(self.detail_ctrl, text=_("process detail"))

        self.process = tk.StringVar()
        self.process_ctrl = ttk.Label(self, textvariable=self.process, width=16, borderwidth=1, relief=tk.SUNKEN)
        self.process_ctrl.pack(side=tk.RIGHT, fill=tk.X, padx=2, pady=2)
        ToolTip(self.process_ctrl, text=_("process under way"))

    def clear(self):
        self.process.set('')
        self.detail.set('')
        self.progress.set(0)
        self.process_ctrl.configure(background='#d9d9d9') # The default color

    def update(self, what, detail, progress, error=False):
        self.process.set(what)
        self.detail.set(detail)
        self.progress.set(progress)
        if error:
            self.process_ctrl.configure(background='#ff0000')
        else:
            self.process_ctrl.configure(background='#00ff00')
