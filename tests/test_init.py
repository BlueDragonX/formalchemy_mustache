# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Tests for formalchemy_mustache.__init__.
"""

import os
import unittest
import formalchemy_mustache
from formalchemy import config
from formalchemy_mustache import configure, MustacheEngine


class TestModule(unittest.TestCase):

    """
    Test the formalchemy_mustache module.
    """

    def test_configure(self):
        """Test the configure function."""
        here = os.path.abspath(os.path.dirname(__file__))
        pkgpath = os.path.abspath(
            os.path.dirname(formalchemy_mustache.__file__))
        pkgtemplates = [os.path.join(pkgpath, 'templates')]
        dirs = [os.path.join(here, 'templates')]
        configure(dirs)
        self.assertIsInstance(config.engine, MustacheEngine,
            'config.engine is invalid')
        self.assertEqual(config.engine.directories, dirs + pkgtemplates,
            'config.engine.directories is invalid')
        self.assertEqual(config.engine.renderer.search_dirs,
            dirs + pkgtemplates,
            'config.engine.search_dirs is invalid')

