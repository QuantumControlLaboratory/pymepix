#!/usr/bin/env python


import os
import imp
from setuptools import Distribution
from setuptools import setup, find_packages
from setuptools.command.install import install

from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils import log




package_dir = {"": "lib"}

packages = find_packages(where="lib")

provides = [
    'pymepix',
]




requires = [
    

]

install_requires = [
    

    
]



console_scripts = [
]


entry_points = {'console_scripts': console_scripts,
                }


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: No Input/Output (Daemon)',
    'Environment :: Win32 (MS Windows)',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
]

setup(name='pymepix',
      author='CFEL-CMI group, et al (see AUTHORS)',
      author_email='cmidaq@cfel.de',
      maintainer='CFEL-CMI group',
      version='0.5',
      description='Timepix python library',
      classifiers=classifiers,
      packages=packages,
      package_dir=package_dir,
 #     scripts=scripts,
      include_package_data=True,
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      install_requires=install_requires,
)