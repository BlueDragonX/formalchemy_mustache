# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the field formalchemy_mustache.fields module.
"""

import os
import unittest
import formalchemy_mustache
from formalchemy_mustache import fields
from .base import BaseCase
from .dummy import DummyModel
from formalchemy_mustache import configure, MustacheFieldRenderer
from formalchemy import config, FieldSet


class TestMustacheFieldRenderer(BaseCase):

    """
    Test the MustacheFieldRenderer class.
    """

    def setUp(self):
        """Set up the test data."""
        BaseCase.setUp(self)
        self.template = 'field'

    def test_init_without_dirs(self):
        """Test the __init__ method without the directories param."""
        configure(self.templates)
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
        configure(self.templates)
        renderer = MustacheFieldRenderer(self.field, self.template,
            self.templates)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, self.template,
            'renderer.template is invalid')
        self.assertEqual(renderer.renderer.search_dirs,
            self.templates + self.package_templates,
            'renderer.directories is invalid')
        
    def test_render(self):
        """Test the render method."""
        configure(self.templates)
        renderer = MustacheFieldRenderer(self.field, self.template,
            self.templates)
        extra = 'some extra data'
        expected = "Name: %s-%s-%s\nValue: %s\nExtra: %s" % (
            type(self.model).__name__, self.field.value, self.field.name,
            self.model.name, extra)
        output = renderer.render(extra=extra).strip()
        self.assertEqual(output, expected,
            'renderer.render is invalid')


class TestBaseFieldRenderer(BaseCase):

    """
    Test the BaseFieldRenderer class.
    """

    def test_init(self):
        """Test the __init__ method."""
        self.assertRaises(fields.TemplateNameError, fields.BaseFieldRenderer,
            self.field)

    def test_implementation_default(self):
        """Test inheriting from BaseFieldRenderer."""
        templates = self.templates
        class TestFieldRenderer(fields.BaseFieldRenderer):
            template = 'field_test'
        renderer = TestFieldRenderer(self.field)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, 'field_test',
            'renderer.template is invalid')
        self.assertEqual(renderer.readonly_template, 'field_readonly',
            'renderer.readonly_template is invalid')
        self.assertEqual(renderer.renderer.search_dirs, config.engine.directories,
            'renderer.directories is invalid')

    def test_implementation_override(self):
        """Test inheriting from BaseFieldRenderer."""
        templates = self.templates
        class TestFieldRenderer(fields.BaseFieldRenderer):
            template = 'field_test'
            readonly_template = 'field_ro_test'
            directories = templates
        renderer = TestFieldRenderer(self.field)
        self.assertEqual(renderer.field, self.field,
            'renderer.field is invalid')
        self.assertEqual(renderer.template, 'field_test',
            'renderer.template is invalid')
        self.assertEqual(renderer.readonly_template, 'field_ro_test',
            'renderer.readonly_template is invalid')
        self.assertEqual(renderer.renderer.search_dirs, templates,
            'renderer.directories is invalid')


class TestFieldRenderers(BaseCase):

    """
    Test generated renderers.
    """

    def check_renderer(self, name, field, html):
        """Test a renderer."""
        configure(self.templates)
        classname = '%sFieldRenderer' % name.title()
        clazz = getattr(fields, classname)
        renderer = clazz(field)
        field.set(renderer=renderer, html=html)
        expected = self.get_output('field_%s' % name).strip()
        output = field.render().strip()

        self.assertEqual(output, expected,
            '%s.render is invalid' % classname)

    def test_text(self):
        """Test the TextFieldRenderer."""
        html = {'class': 'test', 'maxlength': 12}
        self.check_renderer('text', self.field, html)

