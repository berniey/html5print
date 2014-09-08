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
import tinycss2

from .utils import BeautifierBase


class CSSBeautifier(BeautifierBase):
    """CSS Beautifier"""

    @staticmethod
    def foundSelector(node):
        """Return True if node represents beginning of a CSS Selector, False
        otherwise"""
        ns = tinycss2.ast
        found = False
        if type(node) in [ns.HashToken, ns.IdentToken, ns.AtKeywordToken]:
            found = True
        elif type(node) == ns.LiteralToken and node.serialize() in '.*:':
            found = True
        return found

    @staticmethod
    def serializeSelector(ast):
        """Return the serialized Selector portion of a CSS Rule from ast.  For
        example, "p " of "p { margin: 0; }"
        :param ast: a list of nodes that represents a CSS selector
        :return :   serialized css selector

        >>> import tinycss2
        >>> from html5print import CSSBeautifier
        >>> data = '.abc /* comment */ { margin:10px,20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print('"{}"'.format(CSSBeautifier.serializeSelector(ast)))
        ".abc /* comment */ "

        # multiple selector
        >>> data = 'p, h1, h2 /* comment */ { margin:10px,20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print('"{}"'.format(CSSBeautifier.serializeSelector(ast)))
        "p, h1, h2 /* comment */ "

        """
        # this is the one
        contents = []
        for index in range(len(ast)):
            node = ast[index]
            if type(node) == tinycss2.ast.CurlyBracketsBlock:
                break
        contents = ast[:index]
        return ''.join((n.serialize() for n in contents)).rstrip() + ' '

    @staticmethod
    def stripAST(ast):
        """Remove whitespace from the beginning and the end of `ast`"""
        try:
            indexes = (0, -1)
            for i in indexes:
                if type(ast[i]) == tinycss2.ast.WhitespaceToken:
                    ast.pop(i)
        except IndexError:
            pass        # ast was just whitespaces, so just return empty list
        finally:
            return ast

    @classmethod
    def beautify(cls, css, indent=2, encoding=None):
        """beautifying `css` by reindending to width of `indent` per
        level.  `css` is expected to be a valid javascript (i.e. no html
        comment(s) tag <!-- ... -->).

        :param css:      a valid css as multiline string
        :param indent:   width od indentation per level
        :param encoding: expected encoding of `css`.  If None, it will be
                         guesssed
        :return :        reindented css

        >>> from html5print import CSSBeautifier

        >>> css = ".para { margin: 10px 20px; }"
        >>> print(CSSBeautifier.beautify(css))
        .para {
          margin              : 10px 20px;
        }

        >>> css = ".para { margin: 10px 20px; }"
        >>> css += os.linesep + "p { border: 5px solid red; }"
        >>> print(CSSBeautifier.beautify(css))
        .para {
          margin              : 10px 20px;
        }
        p {
          border              : 5px solid red;
        }

        >>> css = ' /* beginning of css*/\\n ::after { margin: 10px 20px; }'
        >>> print(CSSBeautifier.beautify(css))
        /* beginning of css*/
        ::after {
          margin              : 10px 20px;
        }

        >>> css = ' /* beginning of css*/\\n ::after { margin: 10px 20px; }'
        >>> print(CSSBeautifier.beautify(css, 4))
        /* beginning of css*/
        ::after {
            margin              : 10px 20px;
        }

        >>> css = ' /* beginning of css*/\\n ::after { margin: 10px 20px; }'
        >>> css += os.linesep + ' /* another comment */p {'
        >>> css += 'h1 : color: #36CFFF; font-weight: normal;}'
        >>> print(CSSBeautifier.beautify(css, 4))
        /* beginning of css*/
        ::after {
            margin              : 10px 20px;
        }
        /* another comment */
        p {
            h1                  : color: #36CFFF;
            font-weight         : normal;
        }

        # test media query
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

        """
        text = css
        ast = tinycss2.parse_component_value_list(text, True)
        parsed = []
        for ast, isCSSRule in cls.getCSSObjects(ast):
            if isCSSRule:
                text = cls.serializeCSSRule(ast, indent)
            else:
                text = cls.serializeComments(ast)
            if text:
                parsed.append(text)
        return os.linesep.join(parsed)

    @classmethod
    def beautifyTextInHTML(cls, html, indent=2, encoding=None):
        """Beautifying CSS within the <style></style> tag.  Note that
        html comment(s), i.e. <!-- ... --> will be moved to the end of the
        block.
        :param html:      html as string
        :param indent:    width of indentation for embedded CSS in HTML
        :return :         html with CSS beautified (i.e. text
                          within <style>...</style>
        Note: This function will only work if the begin tag `<style>` field is
              the first element in a new line (except for whitespace).
              Indention of the `style` block will be the indent of `<style>`
              tag plus one level of indentation
        >>> from html5print import CSSBeautifier

        >>> html = '''<html><body>
        ...   <style>
        ...     .para { margin: 10px 20px; }
        ... <!-- This is what the function is dealing with-->
        ... p { color: red; font-style: normal; }
        ...   </style>
        ... </body></html>'''
        >>> print(CSSBeautifier.beautifyTextInHTML(html))
        <html><body>
          <style>
            .para {
              margin              : 10px 20px;
            }
            p {
              color               : red;
              font-style          : normal;
            }
            <!-- This is what the function is dealing with-->
          </style>
        </body></html>

        """
        return cls.findAndReplace(html, cls.reIndentAndStyle,
                                  CSSBeautifier.beautify, (indent,), indent)

    @classmethod
    def serializeComments(cls, ast):
        """Return serialized comments `/* ... */` with `indent` spaceis on the
        left"""
        result = ''
        for node in cls.stripAST(ast):
            result += node.serialize() + os.linesep
        return result[:-1]

    @classmethod
    def getCSSObjects(cls, ast):
        """Return CSS Objects (comment or CSS rule)
        :param ast:   Abstract Syntax Tree of CSS
        :return :     a generator with element (cssObject, isCSSRule):
                        cssObject - : a list of ast nodes
                        isCssRule - True if `cssObject` represents CSSRule,
                                    False otherwise
        Note: This function define CSS object as the followings:
                - a css rule i.e. selector { declaration(s) }
                - comment outside of CSS rule.  i.e. in betwen '}' and '{',
                  at the beginning of css (before first CSS rule), or at the
                  end (after the last CSS rule)
        """
        cssObj = []
        insideCSSRule = False
        for node in ast:
            if insideCSSRule:
                if type(node) == tinycss2.ast.CurlyBracketsBlock:
                    # hit end of CSS Rule
                    cssObj.append(node)
                    yield cssObj, True
                    cssObj = []
                    insideCSSRule = False
                    continue
            else:
                if cls.foundSelector(node):
                    # hit start of CSS Rule
                    if cssObj:
                        yield cssObj, False
                        cssObj = []
                    insideCSSRule = True
            cssObj.append(node)
        if cssObj:
            yield cssObj, False

    @classmethod
    def serializeDeclarations(cls, cbb, indent=2):
        """Return serialized declaration(s) defined in `cbb`
        Note: cbb can contain another cbb, i.e. nested structure is possible
        :param cbb:     a curly blacket block node
        :param indent:  width of indent per level
        :return :       seialized declaration

        >>> import tinycss2
        >>> from html5print import CSSBeautifier

        # css with comments and random space between elements
        >>> data = '.abc /* comment */ { margin:10px 20px; /* hello */ }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px; /* hello */'

        # with indent of 4
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1],
        ... 4)))
        '    margin              : 10px 20px; /* hello */'

        # css with no spaces between elements
        >>> data = '.abc/*comment*/{margin:10px 20px;}'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;'

        # css with random spaces between elements
        >>> data = '.abc /* comment */ { margin:10px 20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;'

        # css with two declarations
        >>> data = '.abc /* comment */ { margin:10px 20px; '
        >>> data += os.linesep + ' color: red; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;
          color               : red;'

        >>> data = 'a.red:visited { color: #FF0000; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{}'".format(CSSBeautifier.serializeDeclarations(ast[-1])))
        '  color               : #FF0000;'

        """
        contents = []
        content = ''
        entityEnded = False
        ns = tinycss2.ast
        cbb.content = cls.stripAST(cbb.content)

        for node in cbb.content:
            if node.serialize() == ';':
                entityEnded = True
            if entityEnded and type(node) == ns.IdentToken:
                # new declaration encountered
                # write last entity and then reset
                contents.append(content.rstrip())
                entityEnded = False
                content = node.serialize()
            else:
                content += node.serialize()
        contents.append(content)

        for c, i in zip(contents, range(len(contents))):
            if ':' in c and '::' not in c:
                p, v = c.split(':', 1)
                contents[i] = '{:<20}: {}'.format(p, v.lstrip())
            else:
                contents[i] = contents[i]
        return os.linesep.join(' ' * indent + c for c in contents)

    @classmethod
    def serializeCSSRule(cls, ast, indent=2):
        """Return a serialized CSS Rule
        :param ast:     Abstract Syntax Tree of a CSS rule
        :param indent:  width of indent per level
        :return :       a seialized CSS rule

        >>> import tinycss2
        >>> from html5print import CSSBeautifier

        >>> data = '.abc /* comment */ { margin:10px 20px; /* hello */ }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print(CSSBeautifier.serializeCSSRule(ast))
        .abc /* comment */ {
          margin              : 10px 20px; /* hello */
        }

        # CSS rule with ':'
        >>> data = 'a.red:visited { color: #FF0000; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print(CSSBeautifier.serializeCSSRule(ast))
        a.red:visited {
          color               : #FF0000;
        }
        """
        selector = cls.serializeSelector(ast)
        if selector[0] == '@':
            # media query has nested css rule, need special handling
            thisAst = ast[-1].content
            parsed = []
            for a, isCSSRule in cls.getCSSObjects(thisAst):
                if isCSSRule:
                    text = cls.serializeCSSRule(a, indent)
                else:
                    text = cls.serializeComments(a)
                if text:
                    parsed.extend(text.split(os.linesep))
            parsed = (' ' * indent + p for p in parsed)
            declarations = os.linesep.join(parsed)
        else:
            declarations = cls.serializeDeclarations(ast[-1], indent)
        return os.linesep.join((selector + '{', declarations, '}'))
