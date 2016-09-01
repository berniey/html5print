# -*- coding: utf-8 -*-
#
# Copyright 2014 Bernard Yue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals, absolute_import

from .cssprint import CSSBeautifier
from .jsprint import JSBeautifier
from .html5print import HTMLBeautifier
from .utils import decodeText, isUnicode

__version__ = '0.1.2'
__author__ = 'Bernard Yue'
__doc__ = """
This tool pretty print your HTML, CSS and JavaScript file.  The package comes
with two parts:

    * a command line tool, ``html5-print``
    * a python module, ``html5print``

.. image:: https://travis-ci.org/berniey/html5print.png?branch=master
   :target: https://travis-ci.org/berniey/html5print

.. image:: https://img.shields.io/badge/version-latest-brightgreen.svg?style=plastic
   :target: https://pypi.python.org/pypi/html5print/
   :alt: Latest Version

.. image:: https://img.shields.io/badge/doc-{0}-brightgreen.svg?style=plastic
   :target: https://pythonhosted.org/html5print/
   :alt: Documentation

.. image:: https://img.shields.io/badge/source-latest-blue.svg?style=plastic
   :target: https://github.com/berniey/html5print
   :alt: Source Code

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=plastic
   :target: https://raw.githubusercontent.com/berniey/html5print/master/LICENSE
   :alt: License


Introduction
------------

This module reformat web page code and make it more readable.  It is targeted
for developers, hence is not optimized for speed.  I start out looking for a
tool, ended up created this module.  Hope it helps you!

Key features:

  * Pretty print HTML as well as embedded CSS and JavaScript within it
  * Pretty print pure CSS and JavaScript
  * Try to fix fragmented HTML5
  * Try to fix HTML with broken unicode encoding
  * Try to guess encoding of the document, and in some cases manage
    to convert 8-bit byte code back into correct UTF-8 format
  * Support both Python 2 and 3


Installation
------------

.. code-block:: sh

    $ [sudo] pip install html5print

Uninstallation
--------------

.. code-block:: sh

    $ [sudo] pip uninstall html5print
    $ [sudo] pip uninstall bs4 html5lib slimit tinycss2 requests chardet


Command Line Tool
-----------------

Synopsis
********

.. code-block:: sh

    $ html5-print --help
    usage: html5-print [-h] [-o OUTFILE] [-s INDENT_WIDTH] [-e ENCODING]
                        [-t {{html,js,css}}] [-v]
                        infile

    Beautify HTML5, CSS, JavaScript - Version {1} (By {2})
    This tool reformat the input and return a beautified version,
    in unicode.

    positional arguments:
      infile                filename | url | -, a dash, which represents stdin

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTFILE, --output OUTFILE
                            filename for formatted HTML, stdout if omitted
      -s INDENT_WIDTH, --indent-width INDENT_WIDTH
                            number of space for indentation, default 2
      -e ENCODING, --encoding ENCODING
                            encoding of input, default UTF-8
      -t {{html,js,css}}, --filetype {{html,js,css}}
                            type of file to parse, default "html"
      -v, --version         show program's version number and exit

Example
*******

Pretty print HTML:

.. code-block:: sh

    $ html5-print -s4 -
    Press Ctrl-D when finished
    <html><head><title>Small HTML page</title>
    <style>p {{ margin: 10px 20px; color: black; }}</style>
    <script>function myFunction() {{
    document.getElementById("demo").innerHTML = "Paragraph changed.";
    }}</script>
    </head><body>
    <p>Some text for testing</body></html>
    ^D
    <html>
        <head>
            <title>
                Small HTML page
            </title>
            <style>
                p {{
                    margin              : 10px 20px;
                    color               : black;
                }}
            </style>
            <script>
                function myFunction() {{
                    document.getElementById("demo").innerHTML = "Paragraph changed.";
                }}
            </script>
        </head>
        <body>
            <p>
                Some text for testing
            </p>
        </body>
    </html>
    $

Create valid HTML5 document from HTML fragment:

.. code-block:: sh

    $ html5-print -s4 -
    Press Ctrl-D when finished
    <title>Hello in different language</title>
    <p>Here is "hello" in different languages</p>
    <ul>
    <li>Hello
    <li>您好
    <li>こんにちは
    <li>Dobrý den,
    <li>สวัสดี
    ^D
    <html>
        <head>
            <title>
                Hello in different language
            </title>
        </head>
        <body>
            <p>
                Here is "hello" in different languages
            </p>
            <ul>
                <li>
                    Hello
                </li>
                <li>
                    您好
                </li>
                <li>
                    こんにちは
                </li>
                <li>
                    Dobrý den,
                </li>
                <li>
                    สวัสดี
                </li>
            </ul>
        </body>
    </html>
    $


Testing
-------
The module uses `pytest <http://pytest.org/latest/>`_.  Use pip to install `pytest`.

.. code-block:: sh

    $ [sudo] pip install pytest

Then run test as normal.

.. code-block:: sh

    $ tar zxf html5print-{0}.tar.gz
    $ cd html5print-{0}
    $ python setup.py test


License
-------
This module is distributed under Apache License Version 2.0.


Python API
----------
""".format(__version__, __version__, __author__)
__all__ = ['CSSBeautifier', 'JSBeautifier', 'HTMLBeautifier', 'decodeText',
           'isUnicode']
