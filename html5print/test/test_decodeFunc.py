from __future__ import unicode_literals
from __future__ import absolute_import

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


def test_decodeText(decodeText_func, script_object, fixture_dir):
    abspath = fixture_dir
    files = ['unicode_sample' + ext for ext in ('.html', '.css')]
    files = [os.path.join(abspath, f) for f in files]
    expectedEncoding = ['GB2312'] * 2
    for f, ex in zip(files, expectedEncoding):
        data = script_object.read(f)
        data, encoding = decodeText_func(data)
        assert encoding == ex, f


@pytest.mark.xfail
def test_decodeText_failed(decodeText_func, fixture_dir):
    # autodedect within test_decodeText faild.  Should
    # have detected 'GB2312', but detected 'ISO-8859-2'
    abspath = fixture_dir
    file = os.path.join(abspath, 'failed_detection.js')
    expected = 'GB2312'
    with open(file) as fh:
        data, encoding = decodeText_func(fh.read())
        emsg = 'Expected {}, Got {} - {}'.format(expected, encoding, file)
        assert encoding == expected, emsg
