'''Functions for python 2/3 compatibility.'''

from __future__ import division, print_function, unicode_literals
import sys

IS_PYTHON3 = sys.version_info >= (3,)

if IS_PYTHON3:
    def is_string(s):
        return isinstance(s, (str, bytes))
else:
    def is_string(s):
        return isinstance(s, basestring)
