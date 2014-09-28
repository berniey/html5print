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
import types
import warnings


try:
    import chardet as cdetector
except ImportError:
    try:
        import cchardet as cdetector
    except ImportError:
        print('Requires either chardet or cchardet module')
        raise


def decodeText(text, encoding=None):
    """Decoding `text` to `encoding`.  If `encoding` is None, encoding
    will be guessed.

    **Note**: `encoding` provided will be disregarded if it causes decoding
    error

    :param text:     string to be decoded
    :param encoding: encoding scheme of `text`.  guess by system if None
    :returns:        new decoded text as unicode

    >>> import sys
    >>> from html5print import decodeText
    >>> s = 'Hello! 您好! こんにちは! halló!'
    >>> output = decodeText(s)
    >>> print(output)
    Hello! 您好! こんにちは! halló!
    >>> if sys.version_info.major >= 3:
    ...    unicode = str
    >>> isinstance(output, unicode)
    True
    """
    # if `text` is unicode, not much to convert
    if isUnicode(text):
        return text

    # Now for non unicode text, try decode with provided encoding
    if encoding:
        try:
            text = text.decode(encoding, 'strict')
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            # incorrect `encoding` set by caller, so let's guess first
            warnings.warn(str(e))
        else:
            return text

    # no encoding or decoding with provided `encoding` failed
    detected = cdetector.detect(text)
    detectedEncoding = detected['encoding']
    encodingToUse = detectedEncoding
    if not detectedEncoding:
        # when all things failed, go 'utf-8' for now
        # TODO: find another way
        encodingToUse = 'utf-8'
    try:
        text = text.decode(encodingToUse, 'ignore')
    except UnicodeEncodeError as e:
        msg = str(e) + ' Encodeing used: {}'.format(encodingToUse)
        warnings.warn(msg)

    return text


def isUnicode(text):
    """Return True if `text` is unicode. False otherwise.  Note that because
    the function has to work on both Python 2 and Python 3, u'' cannot be used
    in doctest.

    :param text:  string to check if it is unicode
    :returns:     | **True** if `text` is unicode,
                  | **False** otherwise

    >>> import sys
    >>> if sys.version_info.major >= 3:
    ...     isUnicode(bytes('hello', 'ascii'))
    ... else:
    ...     isUnicode(bytes('hello'))
    False

    >>> import sys
    >>> if sys.version_info.major >= 3:
    ...     unicode = str
    >>> isUnicode(unicode('hello'))
    True
    """
    if sys.version_info.major >= 3:
        if isinstance(text, str):
            return True
        else:
            return False
    else:
        if isinstance(text, str):
            return False
        else:
            return True


class BeautifierBase(object):
    """Base Class for Beautifiers"""

    reIndentAndScript = re.compile(r'^(\s*)<script.*?>(.*?)\s*</script',
                                   re.MULTILINE | re.DOTALL | re.IGNORECASE)
    reIndentAndStyle = re.compile(r'^(\s*)<style.*?>(.*?)\s*</style',
                                  re.MULTILINE | re.DOTALL | re.IGNORECASE)

    @staticmethod
    def _stripHTMLComments(text):
        """Removing HTML Comments '<!-- ... -->' out of `text`
        :returns: a tuple with the following fields
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
                    comments.append(sep[0] + ''.join(tmp[:-1]) + sep[-1])
        return (textWithoutComments, os.linesep.join(comments))

    @classmethod
    def _findAndReplace(cls, text, regExp, bfunc, bfuncArgs, indent=2):
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
        :returns:         beautified text
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
                newScript, comments = cls._stripHTMLComments(script)
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
