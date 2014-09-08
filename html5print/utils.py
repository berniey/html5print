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
import warnings


try:
    import chardet as cdetector
except ImportError:
    try:
        import cchardet as cdetector
    except ImportError:
        print('Requires either chardet or cchardet module')
        raise


def decodeText(bstr, encoding=None):
    """Decoding `bstr` to `encoding`.  If `encoding` is None.  Encoding
    will be guessed
    """
    guess = False
    if encoding:
        try:
            encodingToUse = encoding
            text = bstr.decode(encoding, 'strict')
        except UnicodeEncodeError as e:
            # incorrect `encoding` set by caller, so let's guess first
            t = "Error in decoding as '{}' at pos ({}, {}), will try to guess."
            warnings.warn(t.format(e.encoding, e.start, e.end))
            guess = True
    if guess or not encoding:
        detected = cdetector.detect(bstr)
        detectedEncoding = detected['encoding']
        encodingToUse = detectedEncoding
        if not detectedEncoding:
            # when all things failed, go 'utf-8' for now
            # TODO: find another way
            encodingToUse = 'utf-8'
        text = bstr
        if type(bstr) == type(bytes()):
            text = bstr.decode(encodingToUse, 'replace')
    return text, encodingToUse


class BeautifierBase(object):
    """Base Class for Beautifiers"""

    reIndentAndScript = re.compile(r'^(\s*)<script.*?>(.*?)\s*</script',
                                   re.MULTILINE | re.DOTALL | re.IGNORECASE)
    reIndentAndStyle = re.compile(r'^(\s*)<style.*?>(.*?)\s*</style',
                                  re.MULTILINE | re.DOTALL | re.IGNORECASE)

    @staticmethod
    def stripHTMLComments(text):
        """Removing HTML Comments '<!-- ... -->' out of `text`
        :return : a tuple with the following fields
                    - text with comment(s) removed
                    - removed comment(s)
        """
        textWithoutComments = ''
        comments = []
        sep = ('<!--', '-->')
        fragments = text.split(sep[0])
        if len(fragments) == 1:
            textWithoutComments = fragments[0]
        else:
            textWithoutComments += fragments[0]
            for f in fragments[1:]:
                tmp = f.split(sep[-1])
                if len(tmp) == 1:
                    # found comment with no endtag ...
                    # ignore for now
                    textWithoutComments += tmp[0]
                elif len(tmp) == 2:
                    # this is the correct case
                    textWithoutComments += tmp[-1]
                    comments.append(sep[0] + tmp[0].rstrip() + sep[-1])
                else:
                    # this should never happen (maybe invalid
                    # nested comment)
                    # for this we take maximum chunk as comment
                    textWithoutComments += tmp[-1]
                    comments.append(sep[0] + u''.join(tmp[:-1]) + sep[-1])
        return (textWithoutComments, os.linesep.join(comments))

    @classmethod
    def findAndReplace(cls, text, regExp, bfunc, bfuncArgs, indent=2):
        """Find and replace `text` with what returned by `regExp` by
        beautifing function `bfunc` and params `bfuncArgs`.

        :param text:      text to be find and replace
        :param regExp:    regular expression that returns a list of pairs of
                          (indent, textRequiresFormatting).  E.g.
                          ('    ', '* { margin : 0; }')
        :param bfunc:     beautifying function that take the following
                          parameters (ordered):
                          - textRequiresFormatting
                          - other optional arguments
        :param bfuncArgs: list of arguments for `bfunc`
        :param indent:    width of indentation for section of text requires
                          beautifing
        :return :         beautified text
        """
        final = text
        sections = []
        marker = '%%__mark__%%'
        matches = regExp.finditer(text)
        if matches:
            adjustment = 0
            for mo in matches:
                spaces, script = mo.groups()
                if not script.strip():
                    continue
                start, end = mo.span()
                start += adjustment
                thisIndent = ' ' * (len(spaces) + indent)
                newScript, comments = cls.stripHTMLComments(script)
                params = (newScript,) + bfuncArgs
                lines = [thisIndent + l for l in bfunc(*params).splitlines()]
                lines.extend([thisIndent + l for l in comments.splitlines()])
                sections.append(os.linesep.join(lines))
                final = final[:start] + final[start:].replace(
                    script, marker, 1)
                adjustment += len(marker) - len(script)
        for s in sections:
            final = final.replace(marker, os.linesep + s, 1)
        return final
