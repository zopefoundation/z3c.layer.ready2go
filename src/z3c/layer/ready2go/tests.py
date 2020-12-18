##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Ready2Go Tests
"""
import doctest
import re
import unittest
from zope.app.wsgi.testlayer import BrowserLayer

import z3c.layer.ready2go
from z3c.layer.ready2go.outputchecker import OutputChecker

TestLayer = BrowserLayer(z3c.layer.ready2go, allowTearDown=True)


class IReady2GoTestSkin(z3c.layer.ready2go.IReady2GoBrowserLayer):
    """The ready2go layer test skin."""


DOCTEST_OPTION_FLAGS = (doctest.NORMALIZE_WHITESPACE |
                        doctest.ELLIPSIS |
                        doctest.IGNORE_EXCEPTION_DETAIL
                        )


def test_suite():
    s = doctest.DocFileSuite(
        'README.txt',
        globs=dict(
            getRootFolder=TestLayer.getRootFolder,
            make_wsgi_app=TestLayer.make_wsgi_app),
        optionflags=DOCTEST_OPTION_FLAGS,
        checker=OutputChecker(patterns=[
            # Python 3 unicode removed the "u".
            (re.compile("u('.*?')"), r"\1"),
        ])
    )
    s.layer = TestLayer
    return unittest.TestSuite((s,))
