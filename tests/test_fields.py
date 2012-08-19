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


class TestWidgetSet(BaseCase):

    """
    Test the WidgetSet class.
    """

    class TestSet(fields.WidgetSet):
        """Test WidgetSet class."""
        template = 'field_radio_set'

    def test_selected(self):
        """Test the selected method."""
        renderer = self.TestSet(self.field)
        self.assertTrue(renderer.selected('apple'),
            'renderer.selected is invalid for selected value')
        self.assertFalse(renderer.selected('orange'),
            'renderer.selected is invalid for unselected value')

    def test_proxy_choices(self):
        """Test the proxy_choices method."""
        renderer = self.TestSet(self.field)
        itemlist = [(1, 'one'), (2, 'two')]
        itemdict = {1: 'one', 2: 'two'}
        expected = [
            {'name': renderer.name, 'value': 1, 'label': 'one', 
                'selected': False},
            {'name': renderer.name, 'value': 2, 'label': 'two', 
                'selected': False}]

        result = renderer.proxy_choices(itemlist)
        self.assertEqual(result, expected,
            'renderer.proxy_choices is invalid for lists')

        result = renderer.proxy_choices(itemdict)
        self.assertEqual(len(result), len(expected),
            'renderer.proxy_choices returned results of invalid length')
        for item in result:
            self.assertIn(item, expected,
                'renderer.proxy_choices returned results with an invalid' +
                ' item')


class TestFieldRenderers(BaseCase):

    """
    Test generated renderers.
    """

    def debug_output(self, expected, output):
        return ("Rendered output:\n\t" +
            output.replace("\n", "\n\t") +
            "\nExpected output:\n\t" +
            expected.replace("\n", "\n\t"))

    def check_renderer(self, name, field, field_none=None, readonly=False,
            **options):
        """Test a renderer."""
        configure(self.templates)
        if 'renderer' not in options:
            options['renderer'] = getattr(fields,
                '%sFieldRenderer' % name.title())
                
        field.set(**options)
        expected = self.get_output('field_%s' % name).strip()
        output = field.render().strip()
        self.assertEqual(output, expected,
            "%s.render is invalid\n%s" % (type(field.renderer).__name__,
                self.debug_output(expected, output)))

        if readonly:
            expected = self.get_output('field_%s_readonly' % name).strip()
            output = field.render_readonly().strip()
            self.assertEqual(output, expected,
                "%s.render is invalid\n%s" % (type(field.renderer).__name__,
                    self.debug_output(expected, output)))

        if field_none:
            field_none.set(**options)
            expected = self.get_output('field_%s_none' % name).strip()
            output = field_none.render().strip()
            self.assertEqual(output, expected,
                "%s.render is invalid for None value\n%s" % (type(field.renderer).__name__,
                    self.debug_output(expected, output)))

            if readonly:
                expected = self.get_output('field_%s_none_readonly' %
                    name).strip()
                output = field_none.render_readonly().strip()
                self.assertEqual(output, expected,
                    "%s.render is invalid for None value\n%s" % (type(field.renderer).__name__,
                        self.debug_output(expected, output)))

    def test_text(self):
        """Test the TextFieldRenderer class."""
        html = {'class': 'test', 'maxlength': 12}
        self.check_renderer('text', self.field, self.field_none, html=html)

    def test_textarea(self):
        """Test the TextAreaFieldRenderer class."""
        html = {'class': 'test', 'cols': 80, 'rows': 30}
        self.check_renderer('textarea', self.field_text, self.field_none, html=html,
            renderer=fields.TextAreaRenderer)

    def test_number(self):
        """Test the NumberFieldRenderer class."""
        html = {'class': 'test', 'min': 1, 'max': 20, 'step': 1}
        self.check_renderer('number', self.field_quantity, self.field_none,
            html=html)

    def test_password(self):
        """Test the PasswordFieldRenderer class."""
        html = {'class': 'test'}
        self.check_renderer('password', self.field, self.field_none, True,
            html=html)

    def test_checkbox(self):
        """Test the CheckBoxFieldRenderer class."""
        html = {'class': 'test'}
        self.check_renderer('checkbox', self.field_instock, self.field_none,
            html=html, renderer=fields.CheckBoxFieldRenderer)

    def test_radio_set(self):
        """Test the RadioSet class."""
        html = {'class': 'test'}
        self.check_renderer('radio_set', self.field, self.field_none,
            html=html, renderer=fields.RadioSet, options=self.set_options)

    def test_checkbox_set(self):
        """Test the CheckBoxSet class."""
        html = {'class': 'test'}
        self.check_renderer('checkbox_set', self.field, self.field_none,
            renderer=fields.CheckBoxSet, html=html, options=self.set_options)

    def test_select(self):
        """Test the SelectFieldRenderer class."""
        html = {'class': 'test'}
        self.check_renderer('select', self.field, self.field_none, True,
            html=html, options=self.select_options)

