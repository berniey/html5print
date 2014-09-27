HTML5 Pretty Print
==================
This tool pretty print your HTML, CSS and JavaScript file.  The package comes
with two parts:

    * a command line tool, ``html5-print``
    * a python module, ``html5print``

.. image:: https://travis-ci.org/berniey/html5print.png?branch=master
   :target: https://travis-ci.org/berniey/html5print

.. image:: https://pypip.in/version/html5print/badge.svg?text=version
   :target: https://pypi.python.org/pypi/html5print/
   :alt: Latest Version

.. image:: https://raw.githubusercontent.com/berniey/html5print/master/docs/_static/doc-0.1-brightgreen.png
   :target: https://pythonhosted.org/html5print/
   :alt: Documentation

.. image:: https://raw.githubusercontent.com/berniey/html5print/master/docs/_static/license.png
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
                        [-t {html,js,css}] [-v]
                        infile

    Beautify HTML5, CSS, JavaScript - Version 0.1 (By Bernard Yue)
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
      -t {html,js,css}, --filetype {html,js,css}
                            type of file to parse, default "html"
      -v, --version         show program's version number and exit

Example
*******

Pretty print HTML:

.. code-block:: sh

    $ html5-print -s4 -
    Press Ctrl-D when finished
    <html><head><title>Small HTML page</title>
    <style>p { margin: 10px 20px; color: black; }</style>
    <script>function myFunction() {
    document.getElementById("demo").innerHTML = "Paragraph changed.";
    }</script>
    </head><body>
    <p>Some text for testing</body></html>
    ^D
    <html>
        <head>
            <title>
                Small HTML page
            </title>
            <style>
                p {
                    margin              : 10px 20px;
                    color               : black;
                }
            </style>
            <script>
                function myFunction() {
                    document.getElementById("demo").innerHTML = "Paragraph changed.";
                }
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

Python API
----------

This module requires Python 2.6+ (should work for Python
3.1 and 3.2 but was not tested).

Pretty Print HTML
*****************

.. code-block:: pycon

    >>> from html5print import HTMLBeautifier
    >>> html = '<title>Page Title</title><p>Some text here</p>'
    >>> print(HTMLBeautifier.beautify(html, 4))
    <html>
        <head>
            <title>
                Testing
            </title>
        </head>
        <body>
            <p>
                Some Text
            </p>
        </body>
    </html>
    <BLANKLINE>
    >>>

Pretty Print CSS
****************

Format common CSS

.. code-block:: pycon

    >>> from html5print import CSSBeautifier
    >>> css = """
    ... .para { margin: 10px 20px;
    ... /* Cette règle contrôle l'espacement de tous les côtés \*/"""
    >>> print(CSSBeautifier.beautify(css, 4))
    .para {
        margin              : 10px 20px; /* Cette règle contrôle l'espacement de tous les côtés \*/
    }

Format media query

.. code-block:: pycon

    >>> from html5print import CSSBeautifier
    >>> css = '''@media (-webkit-min-device-pixel-ratio:0) {
    ... h2.collapse { margin: -22px 0 22px 18px;
    ... }
    ... ::i-block-chrome, h2.collapse { margin: 0 0 22px 0; } }
    ... '''
    >>> print(CSSBeautifier.beautify(css, 4))
    @media (-webkit-min-device-pixel-ratio:0) {
        h2.collapse {
            margin              : -22px 0 22px 18px;
        }
        ::i-block-chrome, h2.collapse {
            margin              : 0 0 22px 0;
        }
    }

Pretty Print JavaScript
***********************

.. code-block:: pycon

    >>> from html5print import JSBeautifier
    >>> js = '''
    ... "use strict"; /* Des bribes de commentaires ici et là \*/
    ... function MSIsPlayback() { try { return parent && parent.WebPlayer }
    ... catch (e) { return !1 } }
    ... '''
    >>> print(JSBeautifier.beautify(js, 4))
    "use strict"; /* Des bribes de commentaires ici et là \*/

    function MSIsPlayback() {
        try {
            return parent && parent.WebPlayer
        } catch (e) {
            return !1
        }
    }


Testing
-------
The module uses `pytest <http://pytest.org/latest/>`_.  Use pip to install `pytest`.

.. code-block:: sh

    $ [sudo] pip install pytest

Then run test as normal.

.. code-block:: sh

    $ tar zxf html5print-0.1.tar.gz
    $ cd html5print-0.1
    $ python setup.py test


License
-------
This module is distributed under Apache License Version 2.0.


