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
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


TESTS_REQUIRE = [
    'WebTest',
    'lxml',
    'z3c.macro',
    'zope.app.wsgi',
    'zope.browserresource',
    'zope.principalregistry',
    'zope.publisher',
    'zope.security',
    'zope.securitypolicy',
    'zope.testing',
    'zope.testrunner',
    'z3c.form [test]',
    'zope.tal >= 4.0.0',  # attribute order changes
]

setup(
    name='z3c.layer.ready2go',
    version='1.0.1.dev0',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3'],
    url='https://github.com/zopefoundation/z3c.layer.ready2go',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=TESTS_REQUIRE,
    ),
    setup_requires=[
        'eggtestinfo',
        'zope.testrunner',
    ],
    install_requires=[
        'setuptools',
        'z3c.form',
        'z3c.formui',
        'z3c.layer.pagelet',
        'zope.viewlet',
    ],
    tests_require=TESTS_REQUIRE,
    test_suite='z3c.layer.ready2go.tests.test_suite',
    test_loader='zope.testrunner.eggsupport:SkipLayers',
    zip_safe=False,
)
