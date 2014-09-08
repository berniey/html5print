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

from .cssprint import CSSBeautifier
from .jsprint import JSBeautifier
from .html5print import HTMLBeautifier
from .utils import decodeText

__version__ = '0.1'
__author__ = 'Bernard Yue'
__doc__ = """
This module provides function(s) to pretty print HTML, CSS and
Javascript.  It supports HTML5 and loosely CSS3
"""
