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
"""Setup

$Id:$
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='z3c.layer.ready2go',
    version='0.6.1dev',
    author="Stephan Richter, Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="A ready to go layer for Zope3",
    long_description=(
        read('README.txt')
        + '\n\n' +
        '.. contents::\n'
        + '\n\n' +
        read('src', 'z3c', 'layer', 'ready2go', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license="ZPL 2.1",
    keywords="zope3 z3c ready 2 go layer",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url='http://pypi.python.org/pypi/z3c.layer.ready2go',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=[
            'zope.testbrowser',
            'zope.app.authentication',
            'zope.app.testing',
            'zope.browserresource',
            'zope.principalregistry',
            'zope.publisher',
            'zope.security',
            'zope.securitypolicy',
            'zope.testing',
            'z3c.form [test]',
            ],
        ),
    install_requires=[
        'setuptools',
        'z3c.form',
        'z3c.formui',
        'z3c.layer.pagelet',
        'zope.viewlet',
        ],
    zip_safe=False,
)
