from __future__ import unicode_literals

import pytest


@pytest.fixture
def script_object():
    import sys
    import os
    abspath = os.path.abspath('.')
    sys.path.insert(0, abspath)
    import script
    return script.Main()


@pytest.fixture
def urls():
    return [('http://house.focus.cn/msglist/7073/', 'html'),
            ('http://src.focus.cn/common/modules/standard_head/css/'
                'standard_head_foot.css', 'css'),
            ('http://src.focus.cn/common/group/v2012/js/'
                'sohu.focus.login.bk_1.0.0.s.js', 'js'),
            ]


@pytest.fixture
def data_files():
    import sys
    import os
    abspath = os.path.abspath('.')
    abspath = os.path.join(abspath, 'test', 'fixture')
    extensions = ('.html', '.css', '.js')
    files = ['unicode_sample' + ext for ext in extensions]
    files = [os.path.join(abspath, f) for f in files]
    return zip(files, [s[1:] for s in extensions])


@pytest.mark.remote
def test_read_from_urls(script_object, urls):
    for url, ftype in urls:
        data = script_object.read(url)
        assert type(data) == type(bytes())


def test_read_from_files(script_object, data_files):
    import sys
    import os
    files = [i[0] for i in data_files]
    for f in files:
        data = script_object.read(f)
        assert type(data) == type(bytes())


@pytest.mark.remote
def test_beautify_from_urls(tmpdir, script_object, urls):
    """This test is assume to be passed if no exception raised"""
    indent = 2
    encoding = None
    for url, ftype in urls:
        outfile = str(tmpdir.join('null'))
        script_object.process(ftype, url, outfile, indent, encoding)


@pytest.mark.remote
def test_beautify_from_url_with_encoding(tmpdir, script_object, urls):
    """This test is assume to be passed if no exception raised"""
    indent = 2
    encoding = 'gbk'
    for url, ftype in urls:
        outfile = str(tmpdir.join('null'))
        script_object.process(ftype, url, outfile, indent, encoding)


def test_beautify_from_files(tmpdir, script_object, data_files):
    """This test is assume to be passed if no exception raised"""
    indent = 2
    encoding = None
    for file, ftype in data_files:
        outfile = str(tmpdir.join('null'))
        script_object.process(ftype, file, outfile, indent, encoding)


def test_beautify_from_files_with_encoding(tmpdir, script_object, data_files):
    """This test is assume to be passed if no exception raised"""
    indent = 2
    encoding = 'gbk'
    for file, ftype in data_files:
        outfile = str(tmpdir.join('null'))
        script_object.process(ftype, file, outfile, indent, encoding)



