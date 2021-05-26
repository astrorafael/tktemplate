import os
import os.path

from setuptools import setup, find_packages, Extension
import versioneer

# Default description in markdown
LONG_DESCRIPTION = open('README.md').read()

PKG_NAME     = 'tktemplate'
AUTHOR       = 'Rafael Gonzalez'
AUTHOR_EMAIL = 'rafael08@ucm.es'
DESCRIPTION  = 'Graphical Front-End',
LICENSE      = 'MIT'
KEYWORDS     = 'Astronomy'
URL          = 'https://github.com/astrorafael/tktemplate/'
DEPENDENCIES = [
    'numpy',      # Basic dependency
    'twisted',    # Basic dependency
    'pypubsub',   # Publish/Subscribe support Model/View/Controller
    'rawpy',      # Reads RAW faile formats (from libRaw)
    'exifread',   # Reads EXIF headers only
    'tkcalendar', # calendar data entry widget
    'matplotlib', # Fancy plots for the GUI
    'astropy',    # FITS support (for the time being)
]

CLASSIFIERS  = [
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Astronomy',
    'Topic :: Scientific/Engineering :: Image Processing',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'Framework :: Twisted',
    'Framework :: Matplotlib',
    'Natural Language :: English',
    'Natural Language :: Spanish',
    'Development Status :: 4 - Beta',
]


PACKAGE_DATA = {
    'tktemplate.dbase': [
        'sql/*.sql',
        'sql/data/initial/*.sql',
    ],
    'tktemplate.gui': [
        'data/img/*.gif',
    ],
}

SCRIPTS = ["scripts/tktemplate"]

DATA_FILES  = []

setup(
    name             = PKG_NAME,
    version          = versioneer.get_version(),
    cmdclass         = versioneer.get_cmdclass(),
    author           = AUTHOR,
    author_email     = AUTHOR_EMAIL,
    description      = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    license          = LICENSE,
    keywords         = KEYWORDS,
    url              = URL,
    classifiers      = CLASSIFIERS,
    packages         = find_packages("src"),
    package_dir      = {"": "src"},
    install_requires = DEPENDENCIES,
    scripts          = SCRIPTS,
    package_data     = PACKAGE_DATA,
    data_files       = DATA_FILES,
)
