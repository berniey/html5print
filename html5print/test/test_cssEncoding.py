# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import pytest
import os


@pytest.fixture
def decodeText_func():
    import os
    import sys
    abspath = os.path.abspath('.')
    sys.path.insert(0, abspath)
    from html5print.utils import decodeText
    return decodeText


@pytest.fixture
def cssBeautifer_func():
    import os
    import sys
    abspath = os.path.abspath('.')
    sys.path.insert(0, abspath)
    from html5print.cssprint import CSSBeautifier
    return CSSBeautifier.beautify


def test_decode_unicode(decodeText_func, cssBeautifer_func):
    data = """.para { margin: 10px 20px; /* Cette règle contrôle l'espacement
    de tous les côtés */ }"""
    expected = """
    .para {
       margin              : 10px 20px; /* Cette règle contrôle l'espacement
         de tous les côtés */
    }
    """
    assert cssBeautifer_func(decodeText_func(data)[0]), expected


