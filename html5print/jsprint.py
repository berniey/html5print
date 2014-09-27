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
import sys
import re
import slimit

from .utils import BeautifierBase, decodeText


class JSBeautifier(BeautifierBase):
    """A Javascript Beautifier that pretty print Javascript"""

    @classmethod
    def _reindenting(cls, js, indent=2, srcIndent=2):
        """indenting `js` using `indent` as width of indent per level.  This
        function if for internal use only.

        :param js:        pre-indent js
        :param indent:    indent width per level of resulting js
        :param srcIndent: current indent width per level of `js`
        :returns:         indented javascript with indent width of `indent` per
                          level
        """
        firstLine = js.split('\n', 1)[0]
        offset = len(firstLine) - len(firstLine.lstrip())
        result = []
        lastLevel = 0
        for line in js.splitlines():
            extraIndent = 0
            text = line.lstrip()
            currIndent = len(line) - len(text)
            if currIndent < lastLevel * srcIndent + offset:
                # level down
                lastLevel = (currIndent - offset) // srcIndent
            elif currIndent == (lastLevel + 1) * srcIndent + offset:
                # one level up
                lastLevel += 1
            elif currIndent > (lastLevel + 1) * srcIndent + offset:
                # not indenet to next level but continuation from previous line
                # XXX: not handling param alignment with bracket on last line
                extraIndent = currIndent - offset - lastLevel * srcIndent
            finalIndent = offset + lastLevel * indent + extraIndent
            result.append(' ' * finalIndent + text)
        return '\n'.join(result)

    @classmethod
    def beautify(cls, js, indent=2, encoding=None):
        """Prettifing `js` by reindending to width of indent per level. `js`
        is expected to be a valid Javascipt

        :param js:       a valid javascript as multiline string
        :param indent:   width od indentation per level
        :param encoding: expected encoding of `js`.  If None, it will be
                         guesssed
        :returns:        reindented javascript

        >>> from html5print import JSBeautifier
        >>> js = '''function myFunction() {
        ... document.getElementById("demo").innerHTML = "Paragraph changed.";
        ... }'''

        >>> # test default indent of 2 spaces
        >>> print(JSBeautifier.beautify(js))
        function myFunction() {
          document.getElementById("demo").innerHTML = "Paragraph changed.";
        }

        >>> # test indent of 4 spaces
        >>> print(JSBeautifier.beautify(js, 4))
        function myFunction() {
            document.getElementById("demo").innerHTML = "Paragraph changed.";
        }

        """
        parser = slimit.parser.Parser()
        tree = parser.parse(decodeText(js))
        text = tree.to_ecma()
        return cls._reindenting(text, indent)

    @classmethod
    def beautifyTextInHTML(cls, html, indent=2, encoding=None):
        """Beautifying Javascript within the ``<script></script> tag``. HTML
        comments(s) (i.e. ``<!-- ...  -->``) within the script tag, if any,
        will be moved to the end of the tag block

        :param html:      html as string
        :param indent:    width of indentation for embedded javascript in HTML
        :returns:         html with javascript beautified (i.e. text
                          within ``<script>...</script>``)

        >>> from html5print import JSBeautifier
        >>> js = '''<html><body>
        ...   <script>function myFunction() {
        ... document.getElementById("demo").innerHTML = "Paragraph changed.";
        ... }
        ...   </script>
        ... </body></html>
        ... '''
        >>> print(JSBeautifier.beautifyTextInHTML(js))
        <html><body>
          <script>
            function myFunction() {
              document.getElementById("demo").innerHTML = "Paragraph changed.";
            }
          </script>
        </body></html>
        <BLANKLINE>
        """
        return cls._findAndReplace(html, cls.reIndentAndScript,
                                   cls.beautify, (indent,), indent)
