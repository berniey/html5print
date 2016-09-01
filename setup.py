#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals
import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

__version__ = '0.1.2'
__author__ = 'Bernard Yue'

_classifiers = '''
        Development Status :: 4 - Beta
        Environment :: Console
        Environment :: Web Environment
        Intended Audience :: End Users/Desktop
        Intended Audience :: Developers
        Intended Audience :: System Administrators
        License :: OSI Approved :: Apache Software License
        Operating System :: OS Independent
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: POSIX
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries
        Topic :: System
        Topic :: Text Processing
        Topic :: Text Processing :: Markup
        Topic :: Text Processing :: Markup :: HTML
        Topic :: Utilities
        '''
_classifiers = [s.strip() for s in _classifiers.splitlines() if s.strip()]


filename = 'README.rst'
encoding = 'utf-8'
if sys.version_info[0] >= 3:
    with open(filename, 'r', encoding=encoding) as fh:
        docstring = fh.read()
    packages = ['html5print']
else:
    with open(filename, 'rU') as fh:
        fh = codecs.getreader(encoding)(fh)
        docstring = fh.read()
    packages = [b'html5print']           # without this setup will crash

with open('requirements.txt') as fh:
    requires = fh.read().splitlines()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a',
                     '--doctest-module --ignore=setup.py -m "not remote"')]
    if sys.version_info[0] < 3:
        temp = []
        for t in user_options:
            temp.append(tuple([bytes(i) for i in t]))
        user_options = temp
        del temp

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run unit tests"""
        """import here, cause outside the eggs aren't loaded"""
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='html5print',
      version=__version__,
      description='HTML5, CSS, Javascript Pretty Print',
      long_description=docstring,
      author=__author__,
      author_email='html5print@gmail.com',
      url='https://github.com/berniey/html5print',
      keywords='HTML HTML5 CSS CSS3 Beautify Pretty Print',
      install_requires=requires,
      packages=packages,
      scripts=['html5-print'],
      tests_require=['pytest'],
      cmdclass=dict(test=PyTest),
      classifiers=_classifiers,
      license='Apache 2.0',)
