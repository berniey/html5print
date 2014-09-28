# -*- coding: utf-8 -*-

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
def unicode_func():
    import sys
    if sys.version_info[0] >= 3:
        return str
    else:
        return unicode


def test_the_failed_doctest_case(decodeText_func, unicode_func):
    """Test a potential bug in doctest in using string with mix 7-bit and 8-bit
    chr.
    """
    data = b'Hello! \xe6\x82\xa8\xe5\xa5\xbd!'
    data += b' \xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf!'
    data += b' Hall\xc3\xb3!'
    got = decodeText_func(data)
    assert got == data.decode('utf-8')
