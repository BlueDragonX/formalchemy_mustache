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
from formalchemy import config
from formalchemy_mustache import MustacheEngine
from formalchemy_mustache.pyramid import configure


class DummyPackage:

    """
    Dummy Pyramid package class.
    """

    def __init__(self, name):
        """Initialize the package object with a name."""
        self.__name__ = name


class DummyConfig:

    """
    Dummy Pyramid config class.
    """

    def __init__(self, package, settings=None):
        """Initialize dummy config data."""
        if isinstance(package, basestring):
            package = DummyPackage(package)
        self.package = package
        if settings is None:
            settings = {}
        self.settings = settings
        self.renderers = []

    def get_settings(self):
        """Get the config settings."""
        return self.settings

    def add_renderer(self, name, renderer):
        """Add a renderer to the config."""
        self.renderers.append((name, renderer))


class TestMustacheEngine(unittest.TestCase):

    """
    Test the MustacheEngine class.
    """

    def setUp(self):
        here = os.path.abspath(os.path.dirname(__file__))
        self.directories = [os.path.join(here, 'templates')]
        self.settings = {
            'mustache.templates': ':'.join(self.directories)}
        self.package = 'formalchemy_mustache'
        self.config = DummyConfig(self.package, self.settings)

    def test_init(self):
        """Test the __init__ method."""
        pyramid_mustache.configure(self.config)
        configure(self.config)
        self.assertIsInstance(config.engine, MustacheEngine,
            'config.engine is invalid')
        self.assertEqual(config.engine.directories, self.directories,
            'config.engine.directories is invalid')
        self.assertEqual(config.engine.renderer.search_dirs, self.directories,
            'config.engine.directories is invalid')

