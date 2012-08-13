# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the field formalchemy_mustache.fields module.
"""

import os
import unittest
from formalchemy_mustache import configure, MustacheFieldRenderer
from formalchemy import config, FieldSet
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class DummyModel(Base):

    """
    Dummy SqlAlchemy model.
    """

    __tablename__ = 'dummy'
    text = Column(String, primary_key=True)


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
        extra = 'some more data'
        expected = "Name: %s-%s-%s\nValue: %s\nExtra: %s\n" % (
            type(self.model).__name__, self.model.text, 'text', self.model.text, extra)
        renderer = MustacheFieldRenderer(self.field, self.template,
            self.directories)
        output = renderer.render(extra=extra)
        self.assertEqual(output, expected,
            'renderer.render is invalid')

