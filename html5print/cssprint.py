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

from .utils import BeautifierBase, decodeText, isUnicode


class CSSBeautifier(BeautifierBase):
    """A CSS Beautifier that pretty print CSS.  It loosely supports CSS3.
    """

    @staticmethod
    def _foundSelector(node):
        """Determine if `node` represents beginning of a CSS Selector

        :param node: an AST node
        :returns:    | **True** if node represents beginning of a CSS Selector,
                     | **False** otherwise
        """
        ns = tinycss2.ast
        found = False
        stypes = [ns.HashToken, ns.IdentToken, ns.AtKeywordToken]
        if sum(map(isinstance, [node] * len(stypes), stypes)):
            found = True
        elif isinstance(node, ns.LiteralToken) and node.serialize() in '.*:':
            found = True
        return found

    @staticmethod
    def _serializeSelector(ast):
        """Return the serialized Selector portion of a CSS Rule from ast.  For
        example, "p " of "p { margin: 0; }"

        :param ast: a list of nodes that represents a CSS selector
        :returns:   serialized css selector

        >>> import tinycss2
        >>> from html5print import CSSBeautifier
        >>> data = '.abc /* comment */ { margin:10px,20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print('"{0}"'.format(CSSBeautifier._serializeSelector(ast)))
        ".abc /* comment */ "

        >>> # multiple selectors
        >>> data = 'p, h1, h2 /* comment */ { margin:10px,20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print('"{0}"'.format(CSSBeautifier._serializeSelector(ast)))
        "p, h1, h2 /* comment */ "
        """
        contents = []
        for index in range(len(ast)):
            node = ast[index]
            if isinstance(node, tinycss2.ast.CurlyBracketsBlock):
                break
        contents = ast[:index]
        return ''.join((n.serialize() for n in contents)).rstrip() + ' '

    @staticmethod
    def _stripAST(ast):
        """Remove whitespace from the beginning and the end of `ast`

        :param ast: a list of nodes that represents a CSS selector
        :returns:   a new `ast` with whitespace node removed
        """
        try:
            indexes = (0, -1)
            for i in indexes:
                if isinstance(ast[i], tinycss2.ast.WhitespaceToken):
                    ast.pop(i)
        except IndexError:
            pass        # ast was just whitespaces, so just return empty list
        finally:
            return ast

    @classmethod
    def _serializeComments(cls, ast):
        """Return serialized comments `/* ... */` with `indent` spaceis on the
        left

        :param ast: an AST that represents comments
        :returns:   a comment string
        """
        result = ''
        for node in cls._stripAST(ast):
            result += node.serialize() + os.linesep
        return result[:-1]

    @classmethod
    def _getCSSObjects(cls, ast):
        """Return CSS Objects (comment or CSS rule)
        Note: This function define CSS object as the followings:
        - a css rule i.e. selector { declaration(s) }
        - comment outside of CSS rule.  i.e. in betwen '}' and '{',
          at the beginning of css (before first CSS rule), or at the
          end (after the last CSS rule)

        :param ast:   Abstract Syntax Tree of CSS
        :returns:     a generator with element (cssObject, isCSSRule):
                      `cssObject` - a list of ast nodes
                      `isCssRule` - *True* if `cssObject` represents CSSRule,
                                    *False* otherwise
        """
        cssObj = []
        insideCSSRule = False
        for node in ast:
            if insideCSSRule:
                if isinstance(node, tinycss2.ast.CurlyBracketsBlock):
                    # hit end of CSS Rule
                    cssObj.append(node)
                    yield cssObj, True
                    cssObj = []
                    insideCSSRule = False
                    continue
            else:
                if cls._foundSelector(node):
                    # hit start of CSS Rule
                    if cssObj:
                        yield cssObj, False
                        cssObj = []
                    insideCSSRule = True
            cssObj.append(node)
        if cssObj:
            yield cssObj, False

    @classmethod
    def _serializeDeclarations(cls, cbb, indent=2):
        """Return serialized declaration(s) defined in `cbb`
        Note: cbb can contain another cbb, i.e. nested structure is possible

        :param cbb:     a curly blacket block node
        :param indent:  width of indent per level
        :returns:       seialized declaration

        >>> import tinycss2
        >>> from html5print import CSSBeautifier

        >>> # css with comments and random space between elements
        >>> data = '.abc /* comment */ { margin:10px 20px; /* hello */ }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px; /* hello */'

        >>> # with indent of 4
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1],
        ... 4)))
        '    margin              : 10px 20px; /* hello */'

        >>> # css with no spaces between elements
        >>> data = '.abc/*comment*/{margin:10px 20px;}'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;'

        >>> # css with random spaces between elements
        >>> data = '.abc /* comment */ { margin:10px 20px; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;'

        >>> # css with two declarations
        >>> data = '.abc /* comment */ { margin:10px 20px; '
        >>> data += os.linesep + ' color: red; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1])))
        '  margin              : 10px 20px;
          color               : red;'

        >>> data = 'a.red:visited { color: #FF0000; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print("'{0}'".format(CSSBeautifier._serializeDeclarations(ast[-1])))
        '  color               : #FF0000;'

        """
        contents = []
        content = ''
        entityEnded = False
        ns = tinycss2.ast
        cbb.content = cls._stripAST(cbb.content)

        for node in cbb.content:
            if node.serialize() == ';':
                entityEnded = True
            if entityEnded and isinstance(node, ns.IdentToken):
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
                contents[i] = '{0:<20}: {1}'.format(p, v.lstrip())
            else:
                contents[i] = contents[i]
        return os.linesep.join(' ' * indent + c for c in contents)

    @classmethod
    def _serializeCSSRule(cls, ast, indent=2):
        """Return a serialized CSS Rule

        :param ast:     Abstract Syntax Tree of a CSS rule
        :param indent:  width of indent per level
        :returns:       seialized CSS rule

        >>> import tinycss2
        >>> from html5print import CSSBeautifier

        >>> data = '.abc /* comment */ { margin:10px 20px; /* hello */ }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print(CSSBeautifier._serializeCSSRule(ast))
        .abc /* comment */ {
          margin              : 10px 20px; /* hello */
        }

        >>> # CSS rule with ':'
        >>> data = 'a.red:visited { color: #FF0000; }'
        >>> ast = tinycss2.parse_component_value_list(data, True)
        >>> print(CSSBeautifier._serializeCSSRule(ast))
        a.red:visited {
          color               : #FF0000;
        }
        """
        selector = cls._serializeSelector(ast)
        if selector[0] == '@':
            # media query has nested css rule, need special handling
            thisAst = ast[-1].content
            parsed = []
            for a, isCSSRule in cls._getCSSObjects(thisAst):
                if isCSSRule:
                    text = cls._serializeCSSRule(a, indent)
                else:
                    text = cls._serializeComments(a)
                if text:
                    parsed.extend(text.split(os.linesep))
            parsed = (' ' * indent + p for p in parsed)
            declarations = os.linesep.join(parsed)
        else:
            declarations = cls._serializeDeclarations(ast[-1], indent)
        return os.linesep.join((selector + '{', declarations, '}'))

    @classmethod
    def beautify(cls, css, indent=2, encoding=None):
        """Prettifing `css` by reindending to width of `indent` per
        level.  `css` is expected to be a valid Cascading Style Sheet

        :param css:      a valid css as multiline string
        :param indent:   width od indentation per level
        :param encoding: expected encoding of `css`.  If None, it will be
                         guesssed
        :returns:        reindented css

        >>> # a single css rule
        >>> from html5print import CSSBeautifier
        >>> css = ".para { margin: 10px 20px; }"
        >>> print(CSSBeautifier.beautify(css))
        .para {
          margin              : 10px 20px;
        }

        >>> # multiple css rules
        >>> from html5print import CSSBeautifier
        >>> css = ".para { margin: 10px 20px; }"
        >>> css += os.linesep + "p { border: 5px solid red; }"
        >>> print(CSSBeautifier.beautify(css))
        .para {
          margin              : 10px 20px;
        }
        p {
          border              : 5px solid red;
        }

        >>> # pseudo-class css rule
        >>> from html5print import CSSBeautifier
        >>> css = ' /* beginning of css*/\\n ::after { margin: 10px 20px; }'
        >>> print(CSSBeautifier.beautify(css))
        /* beginning of css*/
        ::after {
          margin              : 10px 20px;
        }

        >>> # pseudo-class css rule with different indent
        >>> from html5print import CSSBeautifier
        >>> css = ' /* beginning of css*/\\n ::after { margin: 10px 20px; }'
        >>> print(CSSBeautifier.beautify(css, 4))
        /* beginning of css*/
        ::after {
            margin              : 10px 20px;
        }

        >>> # pseudo-class css rules with comments in between
        >>> from html5print import CSSBeautifier
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

        >>> # media query
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
        """
        text = decodeText(css)
        ast = tinycss2.parse_component_value_list(text, True)
        parsed = []
        for ast, isCSSRule in cls._getCSSObjects(ast):
            if isCSSRule:
                text = cls._serializeCSSRule(ast, indent)
            else:
                text = cls._serializeComments(ast)
            if text:
                parsed.append(text)
        return os.linesep.join(parsed)

    @classmethod
    def beautifyTextInHTML(cls, html, indent=2, encoding=None):
        """Beautifying CSS within the ``<style></style>`` tag.  HTML
        comments(s) (i.e. ``<!-- ... -->``) within the `style tag`, if any,
        will be moved to the end of the tag block.

        **Note**: The function assumes tag ``<style>`` the first
        element in a new line containing the tag (except for whitespace).
        Indention of the `style` block will be the indent of ``<style>`` tag
        plus one ``indent`` of current indentation

        :param html:      html as string
        :param indent:    width of indentation for embedded CSS in HTML
        :returns:         html with CSS beautified (i.e. text
                          within ``<style>...</style>``)

        >>> # pretty print css
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

        >>> # <style> not the first element, no pretty print
        >>> from html5print import CSSBeautifier
        >>> html = '''<html><body><style>
        ...     .para { margin: 10px 20px; }
        ... <!-- This is what the function is dealing with-->
        ... p { color: red; font-style: normal; }
        ...   </style>
        ... </body></html>'''
        >>> print(CSSBeautifier.beautifyTextInHTML(html))
        <html><body><style>
            .para { margin: 10px 20px; }
        <!-- This is what the function is dealing with-->
        p { color: red; font-style: normal; }
          </style>
        </body></html>
        """
        return cls._findAndReplace(html, cls.reIndentAndStyle,
                                  CSSBeautifier.beautify, (indent,), indent)
