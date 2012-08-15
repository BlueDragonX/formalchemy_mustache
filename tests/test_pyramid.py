# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Tests for formalchemy_mustache.pyramid.
"""

import os
import unittest
import pyramid_mustache
import formalchemy_mustache
from .dummy import DummyConfig
from formalchemy import config
from formalchemy_mustache import MustacheEngine
from formalchemy_mustache.pyramid import configure


class TestMustacheEngine(unittest.TestCase):

    """
    Test the MustacheEngine class.
    """

    def setUp(self):
        here = os.path.abspath(os.path.dirname(__file__))
        pkgpath = os.path.abspath(
            os.path.dirname(formalchemy_mustache.__file__))
        pkgtemplates = os.path.join(pkgpath, 'templates')
        self.package = 'formalchemy_mustache'
        self.directories_default = [os.path.join(here, 'templates'),
            pkgtemplates]
        self.directories_custom = [os.path.join(here, 'templates/forms'),
            pkgtemplates]
        self.settings_default = {
            'mustache.templates': ':'.join(self.directories_default[:-1])}
        self.config_default = DummyConfig(self.package, self.settings_default)
        self.settings_custom = {
            'mustache.templates': ':'.join(self.directories_default[:-1]),
            'mustache.forms': 'forms'}
        self.config_custom = DummyConfig(self.package, self.settings_custom)

    def test_init_default(self):
        """Test the __init__ method with default settings."""
        pyramid_mustache.configure(self.config_default)
        configure(self.config_default)
        expected = "fieldset template\n"
        output = config.engine.render('fieldset')
        self.assertIsInstance(config.engine, MustacheEngine,
            'config.engine is invalid')
        self.assertEqual(config.engine.directories, self.directories_default,
            'config.engine.directories is invalid')
        self.assertEqual(config.engine.renderer.search_dirs, self.directories_default,
            'config.engine.renderer.search_dirs is invalid')
        self.assertEqual(output, expected,
            'config.engine.render is invalid')

    def test_init_custom(self):
        """Test the __init__ method with custom settings."""
        pyramid_mustache.configure(self.config_custom)
        configure(self.config_custom)
        expected = "fieldset template in forms\n"
        output = config.engine.render('fieldset')
        self.assertIsInstance(config.engine, MustacheEngine,
            'config.engine is invalid')
        self.assertEqual(config.engine.directories, self.directories_custom,
            'config.engine.directories is invalid')
        self.assertEqual(config.engine.renderer.search_dirs, self.directories_custom,
            'config.engine.renderer.search_dirs is invalid')
        self.assertEqual(output, expected,
            'config.engine.render is invalid')

