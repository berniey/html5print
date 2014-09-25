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
def unicode_func():
    import sys
    if sys.version > '3':
        return str
    else:
        return unicode


@pytest.fixture
def script_object():
    import os
    import sys
    abspath = os.path.abspath('.')
    spath = os.path.join(abspath, 'test')
    sys.path.insert(0, abspath)
    from script import Main
    return Main()


@pytest.fixture
def fixture_dir():
    import os
    import sys
    abspath = os.path.abspath('.')
    return os.path.join(abspath, 'html5print', 'test', 'fixture')


def test_decodeText(decodeText_func, script_object, fixture_dir, unicode_func):
    """test decodeText() with sample text file"""
    abspath = fixture_dir
    files = ['unicode_sample' + ext for ext in ('.html', '.css')]
    files = [os.path.join(abspath, f) for f in files]
    for f in files:
        data = script_object.read(f)
        data = decodeText_func(data)
        assert isinstance(data, unicode_func), f


@pytest.mark.xfail
def test_decodeText_failed(decodeText_func, fixture_dir):
    """autodedect within test_decodeText faild.  Should have detected
    'GB2312', but detected 'ISO-8859-2'"""
    abspath = fixture_dir
    file = os.path.join(abspath, 'failed_detection.js')
    expected = 'GB2312'
    with open(file) as fh:
        data, encoding = decodeText_func(fh.read())
        emsg = 'Expected {}, Got {} - {}'.format(expected, encoding, file)
        assert encoding == expected, emsg


def test_decodeText_utf8(decodeText_func, unicode_func):
    """test decodeText() with utf-8 input"""
    data = b'\xe4\xba\xba\xe7\x94\x9f'
    data = data.decode('utf-8')

    # no encodeing given
    got = decodeText_func(data)
    assert got == unicode_func('\u4eba\u751f')

    # correct encodeing given
    got = decodeText_func(data, 'utf-8')
    assert got == unicode_func('\u4eba\u751f')

    # incorrect encodeing given
    got = decodeText_func(data, 'utf-32')
    assert got == unicode_func('\u4eba\u751f')


def test_decodeText_utf16(decodeText_func, unicode_func):
    """test decodeText() with utf-16 input"""
    data = b'\xff\xfe\xbaN\x1fu'
    data = data.decode('utf-16')

    # no encodeing given
    got = decodeText_func(data)
    assert got == unicode_func('\u4eba\u751f')

    # correct encodeing given
    got = decodeText_func(data, 'utf-16')
    assert got == unicode_func('\u4eba\u751f')

    # incorrect encodeing given
    got = decodeText_func(data, 'utf-8')
    assert got == unicode_func('\u4eba\u751f')


def test_decodeText_utf32(decodeText_func, unicode_func):
    """test decodeText() with utf-32 input"""
    data = b'\xff\xfe\x00\x00\xbaN\x00\x00\x1fu\x00\x00'
    data = data.decode('utf-32')

    # no encodeing given
    got = decodeText_func(data)
    assert got == unicode_func('\u4eba\u751f')

    # correct encodeing given
    got = decodeText_func(data, 'utf-32')
    assert got == unicode_func('\u4eba\u751f')

    # incorrect encodeing given
    got = decodeText_func(data, 'utf-16')
    assert got == unicode_func('\u4eba\u751f')
