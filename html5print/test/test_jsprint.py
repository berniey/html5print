from __future__ import unicode_literals, absolute_import

import pytest
import os
import sys
import textwrap


@pytest.fixture
def js_beautify():
    import sys
    abspath = os.path.abspath('.')
    sys.path.insert(0, abspath)
    from html5print import JSBeautifier
    return JSBeautifier.beautify


@pytest.fixture
def html_fragment():
    html = '''
    <script>var x = function(
      y, // notice one tab over
      z,
      w) {
      t;
      }
    </script>
    '''
    return html


@pytest.fixture
def js_fragment():
    js = '''
var Event = require('./event');

var EventTarget = {
    onopen:     null,
    onmessage:  null,
    onerror:    null,
    onclose:    null,

    addEventListener: function(eventType, listener, useCapture) {
    this._listeners = this._listeners || {};
    var list = this._listeners[eventType] =

this._listeners[eventType] || [];
    list.push(listener);
      },

removeEventListener: function(eventType, listener, useCapture) {
if (!this._listeners || !this._listeners[eventType]) return;

if (!listener) {
    delete this._listeners[eventType];
    return;
    }
    var list = this._listeners[eventType],
    i    = list.length;

    while (i--) {
    if (listener !== list[i])
    continue;
    list.splice(i,1);
    }
    },

    dispatchEvent:

function(event)
{
    event.target = event.currentTarget = this;
    event.eventPhase = Event.AT_TARGET;

    if (this['on' + event.type])
        this['on' + event.type](event);

    if (!this._listeners || !this._listeners[event.type]) return;

    this._listeners[event.type].forEach(function(listener) {
        listener(event);
    }, this);
    }
};
    '''
    return js


def test_js_beautify(js_beautify, js_fragment):
    func = js_beautify
    expected = '''var Event = require('./event');
var EventTarget = {
    onopen: null,
    onmessage: null,
    onerror: null,
    onclose: null,
    addEventListener: function(eventType, listener, useCapture) {
        this._listeners = this._listeners || {
        };
        var list = this._listeners[eventType] = this._listeners[eventType] || [];
        list.push(listener);
    },
    removeEventListener: function(eventType, listener, useCapture) {
        if (!this._listeners || !this._listeners[eventType]) return;
        if (!listener) {
            delete this._listeners[eventType];
            return;
        }
        var list = this._listeners[eventType], i = list.length;
        while (i--) {
            if (listener !== list[i]) continue;
            list.splice(i, 1);
        }
    },
    dispatchEvent: function(event) {
        event.target = event.currentTarget = this;
        event.eventPhase = Event.AT_TARGET;
        if (this['on' + event.type]) this['on' + event.type](event);
        if (!this._listeners || !this._listeners[event.type]) return;
        this._listeners[event.type].forEach(function(listener) {
            listener(event);
        }, this);
    }
};'''
    assert func(js_fragment, 4) == expected

"""
def test_html_beautify_multiline_tag(html5_beautify, html_fragment):
    func = html5_beautify
    got = func(html_fragment)
    expected = textwrap.dedent('''
    <html>
      <head>
      </head>
      <body>
        <div id="page-wrap">
          <img alt="Some binary data=" pic"="" src="data:image/png;base64,
                    iVBORw0KGgoAAAANSUhEUgAAAOgAAAEvCAYAAABPM43AAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAL
                    EwAACxMBAJqcGAAAAAd0SU1FB90FCgQSFKAOxjcAAAAdaVRYdENvbW1lbnQAAAAAAENyZWF0ZWQg
                    d2l0aCBHSU1QZC5lBwAAIABJREFUeNrsvVmSJElyJfiYRVTVzNwjIzd09xThCHOK+Z7vukOfoqiu
                    g5+5TROB8DuNAhqoyiUi3MxUVYTng1lEWMTUoxJd4dgmg8gpNnczNVXh7fHjx4Rff/3669dfAAAR
                    YQAzgMW+Tvb7bF/vAHwP4L8C+BbA/0NE/+Mtryn++lh+/fWfzMgIALuv4P4cATwBeA/gGzOyb+zv
                    TwAuZoRf279/Z7+/A3C2n2cAnHNOOef/AeBXA/3116+/DqLc7CLca1Hu/wDw3+zP35gBzi46+q/J
                    jO8X/fr5xx+3v/+Hf3j63e9+x7///e/zrwb666//bFGOhujG9m/TQZT7+pUoVyLcNwC+sigX3OuG
                    g/f4S68d+7bhD3//9/jbv/3br3/zm98EAL8a6K+//kMZYDBD8/XcYv+2DFHuv9nXX7koV77/7L5K
                    lOQ3vnj97bX/Tgm3lxe8vLxQSun7bz5+jAC2Xw3011//VlFujHB8EOV8FLvY/71zEXCs5cLBl38P
                    +ksN7HNG5r+n+/P4bwf/JzlDcgaHQEL0X/8Q4wTg+quB/vrrXyPKza9Euf/qotzXrpYr0e1iv5/s
                    3/8yI/tLotxoXKORifzFb0/MiCFQIPqry+Xypjb0q4H+54ly9EqU+xoNlfx6iHJfDVGu1HqnV6Jc
                    7u6/fv/7dWJ+4JTyOo/qAwKsSfUOUlqvEDfTbvc0vXt33O12+vHjR6493T9+/z3/01uWe3v8GT3+
                    F2hm2H/e+SvoAAAAAElFTkSuQmCC"/>
        </div>
      </body>
    </html>
    ''')
    expected = expected.replace('\n', '', 1)
    assert got == expected, 'Expected "{}", Got "{}"'.format(expected, got)
"""
