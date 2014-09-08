HTML5 Pretty Print
==================
This tool pretty print your HTML, CSS and Javascript file.  The package comes
with two parts:

    * a command line tool, ``html5-print``
    * a python module, ``html5-print``

.. image:: https://travis-ci.org/berniey/html5print.png?branch=master
   :target: https://travis-ci.org/berniey/html5print

Detail Description
------------------

This module is intended to help developer to reformat web page code and
make it more readable.  It is not optimized for speed.
I start out looking for a tool, ending up created this module.  Hope it help
you!

Key features:

  * Pretty print not only HTML but also embedded CSS and Javascript within HTML
  * Also pretty print pure CSS and Javascript
  * Try to fix broken HTML5
  * Try to fix HTML with broken unicode encoding
  * Will try to guess the encoding of the document, and in some cases manage
    to convert 8-bit byte code back into correct UTF-8 format
  * Support both Python 2 and 3


Installation
------------

.. code-block:: sh

    $ pip install html5print

Uninstallation
--------------

.. code-block:: sh

    $ pip uninstall html5print
    $ pip uninstall html5print
    $ pip uninstall bs4 html5lib jsbeautifier tinycss2 requests chardet


Command Line Tool
-----------------

Synopsis
********

.. code-block:: sh

    $ ./html5-print --help
    usage: html5-print [-h] [-o OUTFILE] [-s INDENT_WIDTH] [-e ENCODING]
                        [-t {html,js,css}] [-v]
                        infile

    Beautify HTML5, CSS, Javascript - Version 0.1 (By Bernard Yue)
    This tool reformat the input and return a beautified version,
    in unicode.

    positional arguments:
      infile                filename | url | -, a dash, which represents stdin

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTFILE, --output OUTFILE
                            filename for formatted html, stdout if omitted
      -s INDENT_WIDTH, --indent-width INDENT_WIDTH
                            number of space for indentation, default 2
      -e ENCODING, --encoding ENCODING
                            encoding of input, default UTF-8
      -t {html,js,css}, --filetype {html,js,css}
                            type of file to parse, default html
      -v, --version         show program's version number and exit

Example
*******

Pretty print html

.. code-block:: sh

    $ python ./html5-print -s4 -
    Press Ctrl-D when finished


Create valid html5 document from html fragment

.. code-block:: sh

    $ python ./html5-print -s4 -
    Press Ctrl-D when finished
    <p>Hello in different language</p>
    <ul>
    <li>您好
    <li>こんにちは
    <li>Dobrý den,
    <li>สวัสดี
    ^D
    <html>
        <head>
        </head>
        <body>
            <p>
                Hello in different language
            </p>
            <ul>
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

This module requires Python 2.7+ (should work for Python 2.6 but was not tested)

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

    >>>

Pretty Print CSS
****************

Format common CSS

.. code-block:: pycon

    >>> from html5print import CSSBeautifier
    >>> css = ".para { margin: 10px 20px; /* langue étrangère \*/}"
    >>> print(CSSBeautifier.beautify(css, 4))
    .para {
        margin              : 10px 20px;    /* langue étrangère \*/
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

Pretty Print Javascript
***********************

.. code-block:: pycon


Testing
-------
You can either run the standalone ``runtests.py`` or standard
``python setup.py test``

.. code-block:: sh

    $ tar zxf html5print-0.1.tar.gz
    $ cd html5print-0.1
    $ python setup.py test


License
-------
This module is distributed under Apache License Version 2.0.



