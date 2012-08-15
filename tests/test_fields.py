# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the field formalchemy_mustache.fields module.
"""

import os
import unittest
from .dummy import DummyModel
from formalchemy_mustache import configure, MustacheFieldRenderer
from formalchemy import config, FieldSet


class TestMustacheFieldRenderer(unittest.TestCase):

    """
    Test the MustacheFieldRenderer class.
    """

    def setUp(self):
        """Set up the test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        self.model = DummyModel(text='some test data')
        self.fieldset = FieldSet(DummyModel).bind(self.model)
        self.field = self.fieldset.text
        self.directories = [os.path.join(here, 'templates')]
        self.template = 'field'

        self.output_extra = 'some extra data'
        self.output_expected = "Name: %s--%s\nValue: %s\nExtra: %s\n" % (
            type(self.model).__name__, 'text', self.model.text, self.output_extra)

    def test_init_without_dirs(self):
        """Test the __init__ method without the directories param."""
        configure(self.directories)
        renderer = MustacheFieldRenderer(self.field, self.template)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, self.template,
            'renderer.template is invalid')
        self.assertEqual(renderer.renderer.search_dirs,
            config.engine.directories,
            'renderer.directories is invalid')

    def test_init_with_dirs(self):
        """Test the __init__ method with the directories param."""
        renderer = MustacheFieldRenderer(self.field, self.template,
            self.directories)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, self.template,
            'renderer.template is invalid')
        self.assertEqual(renderer.renderer.search_dirs, self.directories,
            'renderer.directories is invalid')
        
    def test_render(self):
        """Test the render method."""
        renderer = MustacheFieldRenderer(self.field, self.template,
            self.directories)
        output = renderer.render(extra=self.output_extra)
        self.assertEqual(output, self.output_expected,
            'renderer.render is invalid')

    def test_factory_without_dirs(self):
        """Test the factory method without the directories param."""
        configure(self.directories)
        clazz = MustacheFieldRenderer.factory(self.template)
        renderer = clazz(self.field)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, self.template,
            'renderer.template is invalid')
        self.assertEqual(renderer.renderer.search_dirs,
            config.engine.directories,
            'renderer.directories is invalid')

    def test_factory_with_package(self):
        """Test the factory method with the directories param."""
        configure(self.directories)
        clazz = MustacheFieldRenderer.factory(self.template, self.directories)
        renderer = clazz(self.field)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, self.template,
            'renderer.template is invalid')
        self.assertEqual(renderer.renderer.search_dirs, self.directories,
            'renderer.directories is invalid')

