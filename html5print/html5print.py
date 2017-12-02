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

import os
import re

import bs4

from .utils import BeautifierBase
from .cssprint import CSSBeautifier
from .jsprint import JSBeautifier


class HTMLBeautifier(BeautifierBase):
    """HTML Beautifier.  Powered by BeautifulSoup 4"""

    reSpace = re.compile(r'^(\s*)')
    reBeginTag = re.compile('\s*(<[a-zA-Z].*?>)')       # match begin tag
    reEndTag = re.compile('\s*(</[a-zA-Z].*?>|<.*/>)')  # match end tag
    ignoreTags = ['style', 'script']

    @classmethod
    def beautify(cls, html, indent=2, encoding=None, formatter="html5"):
        """Pretty print html with indentation of `indent` per level

        :param html:      html as string
        :param indent:    width of indentation
        :param encoding:  encoding of html
        :param formatter: formatter to use by bs4.  use `lxml` if you want
                          HTML4 output
        :returns:         beautified html

        >>> # pretty print HTML
        >>> from html5print import HTMLBeautifier
        >>> html = '<title>Testing</title><body><p>Some Text</p>'
        >>> print(HTMLBeautifier.beautify(html))
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

        >>> # pretty print HTML
        >>> from html5print import HTMLBeautifier
        >>> html = '<script type="text/javascript">switch (1 = 2) {case 1:return 1;}</script>'
        >>> print(HTMLBeautifier.beautify(html))
        <html>
          <head>
            <script type="text/javascript">
           switch (1 = 2) {case 1:return 1;}
            </script>
          </head>
          <body>
          </body>
        </html>
        <BLANKLINE>

        >>> # pretty print HTML with embedded CSS and Javascript
        >>> from html5print import HTMLBeautifier
        >>> html = '''<html><head><title>Testing</title>
        ... <style>p { color:red; font-weight:nornal}
        ... h1{color:green;}
        ... </style>
        ... </head>
        ... <body><p>Some Text</p>
        ... <script>function myFunction()
        ... {document.getElementById("demo").innerHTML="changed.";
        ... }</script>
        ... </body></html>
        ... '''
        >>> print(HTMLBeautifier.beautify(html))
        <html>
          <head>
            <title>
              Testing
            </title>
            <style>
              p {
                color               : red;
                font-weight         : nornal
              }
              h1 {
                color               : green;
              }
            </style>
          </head>
          <body>
            <p>
              Some Text
            </p>
            <script>
              function myFunction() {
                document.getElementById("demo").innerHTML = "changed.";
              }
            </script>
          </body>
        </html>
        <BLANKLINE>
        """
        soup = bs4.BeautifulSoup(html, 'html5lib')
        html = soup.prettify(formatter=formatter)
        html = cls._prettifyWithIndent(html, indent)
        html = JSBeautifier.beautifyTextInHTML(html, indent, encoding)
        html = CSSBeautifier.beautifyTextInHTML(html, indent, encoding)
        return html

    @classmethod
    def _prettifyWithIndent(cls, html, indent=2):
        """Prettify bs4.prettify output with `indent`
        Note: Assumed `html` is input from bs4.prettify, which has indent
              width of 1.

        :param html:    html as string
        :param indent:  width of indentation
        :returns:       beautified html with bs4.prettify() error fixed
        """
        final = []
        lastNonBlankLine = ''
        canChange = True
        multiLineTag2ndLine = False
        for line in html.splitlines():
            if not line or not line.strip():
                final.append(line)
                continue
            spaces = cls.reSpace.match(line).group()
            if line[len(spaces)] == '<':
                stMatch = cls.reBeginTag.match(line)
                etMatch = cls.reEndTag.match(line)
                if stMatch and etMatch:
                    pass
                elif not stMatch and not etMatch:
                    # multiline tag
                    canChange = False
                    multiLineTag2ndLine = True
                elif etMatch:
                    for tag in cls.ignoreTags:
                        if '</' + tag in line.lower():
                            canChange = True
                            break
                elif stMatch:
                    for tag in cls.ignoreTags:
                        if '<' + tag in line.lower():
                            canChange = False
                            break
                line = ' ' * len(spaces) * indent + line.lstrip()
            else:
                if canChange:
                    thisLevel = len(spaces) * indent
                    if lastNonBlankLine.lstrip()[0] != '<':
                        lastLevel = len(cls.reSpace.match(
                                        lastNonBlankLine).group())
                        if thisLevel > lastLevel + 4:
                            line = ' ' * lastLevel + line.lstrip()
                    else:
                        line = ' ' * thisLevel + line.lstrip()
                elif multiLineTag2ndLine:
                    # now you are free
                    canChange = True
                    multiLineTag2ndLine = False
            final.append(line)
            lastNonBlankLine = line
        return os.linesep.join(final) + os.linesep
