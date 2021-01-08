##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Ready2Go Browser Layer
"""
from zope.viewlet.interfaces import IViewletManager
import z3c.layer.pagelet
import z3c.form.interfaces
import z3c.formui.interfaces


class IReady2GoBrowserLayer(
        z3c.layer.pagelet.IPageletBrowserLayer,
        z3c.formui.interfaces.IDivFormLayer,
        z3c.form.interfaces.IFormLayer):
    """A ready 2 go layer useful for custom applications."""


class ICSS(IViewletManager):
    """CSS viewlet manager."""


class IJavaScript(IViewletManager):
    """JavaScript viewlet manager."""


class IBreadcrumb(IViewletManager):
    """Breadcrumb viewlet manager."""


class ISideBar(IViewletManager):
    """SideBar viewlet manager."""
