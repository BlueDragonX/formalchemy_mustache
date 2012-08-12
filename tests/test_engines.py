# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the pyramid_mustache.engines module.
"""

import os
import unittest
from formalchemy_mustache import MustacheEngine


class TestMustacheEngine(unittest.TestCase):

    """
    Test the MustacheEngine class.
    """

    def setUp(self):
        """Set up the test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        self.directories = [os.path.join(here, 'templates')]

    def test_init(self):
        """Test the __init__ method."""
        engine = MustacheEngine(directories=self.directories)
        self.assertEqual(engine.directories, self.directories,
            'engine.directories is invalid')
        self.assertEqual(engine.renderer.search_dirs, self.directories,
            'engine.renderer.search_dirs is invalid')

    def test_get_template(self):
        """Test the get_template method."""
        expected = "Test: {{test}}\n"
        engine = MustacheEngine(directories=self.directories)
        output = engine.get_template('test')
        self.assertEqual(output, expected,
            'engine.get_template is invalid')

    def test_render(self):
        name = 'test'
        data = {'test': 'this is a test'}
        expected = "Test: %s\n" % data['test']
        engine = MustacheEngine(directories=self.directories)
        engine.templates[name] = engine.get_template(name)
        output = engine.render(name, **data)
        self.assertEqual(output, expected,
            'engine.render is invalid')

