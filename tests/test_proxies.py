# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the formalchemy_mustache.proxy module.
"""


import os
import unittest
from formalchemy_mustache import proxies
from .dummy import DummyModel, DummyFieldSet
from formalchemy.fields import Field
from formalchemy.forms import FieldSet
from formalchemy.tables import Grid


class BaseCase(unittest.TestCase):

    """
    Set up test data for test cases.
    """

    def setUp(self):
        """Set up test data."""
        self.outputpath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'output')

        self.models = [
            DummyModel.create('apple', 
                'a red fruit that grows on trees'),
            DummyModel.create('carrot', 
                'an orange vegetable that grows in the ground'),
            DummyModel.create('kiwi',
                'a brown fruit that is not a flightless bird')]
        self.model = self.models[0]

        fs = FieldSet(DummyModel)
        fs.configure(include=[fs.name, fs.text])
        self.fieldset_rw = fs.bind(self.model)
        fs.configure(include=[fs.name, fs.text], readonly=True)
        self.fieldset_ro = fs.bind(self.model)

        grid = Grid(DummyModel)
        grid.configure(include=[grid.name, grid.text])
        self.grid_rw = grid.bind(self.models)
        grid.configure(include=[grid.name, grid.text], readonly=True)
        self.grid_ro = grid.bind(self.models)

    def get_output(self, name):
        """Get the contents of an output file."""
        outputfile = os.path.join(self.outputpath, "%s.out" % name)
        with open(outputfile) as fd:
            return fd.read()


class TestFunctions(BaseCase):

    """
    Test module functions.
    """

    def test_proxy_errors(self):
        """Test the proxy_errors function."""
        errorlist = ['error one', 'error two']
        errordict = [{'error': 'error one'}, {'error': 'error two'}]
        result = proxies.proxy_errors(errorlist)
        self.assertEqual(result, errordict,
            'proxy_errors is invalid')

    def test_proxy_fields(self):
        """Test the proxy_fields function."""
        fields = self.fieldset_rw.render_fields
        fieldproxies = proxies.proxy_fields(fields)
        self.assertEqual(len(fields), len(fieldproxies),
            'proxy_fields returned wrong number of proxies')
        for proxy in fieldproxies:
            self.assertIsInstance(proxy, proxies.FieldProxy,
                'field proxy has invalid type')
            self.assertTrue(proxy.field in fields.values(),
                'field proxy contains invalid field object')
            self.assertTrue(proxy._focus is False,
                'field proxy has invalid focus value')

    def test_proxy_fields_focus(self):
        """Test the focus parameter of the proxy_fields function."""
        fields = self.fieldset_rw.render_fields
        focus = fields.values()[1]
        fieldproxies = proxies.proxy_fields(fields, focus)
        fieldproxy = [fp for fp in fieldproxies if fp.field == focus]
        self.assertEqual(fieldproxy[0]._focus, True,
            'field proxy did not gain focus when focus==field')

        fieldproxies = proxies.proxy_fields(fields, True)
        self.assertEqual(fieldproxies[0]._focus, True,
            'field proxy did not gain focus when focus==True')

    def test_proxy_object(self):
        """Test the proxy_object function."""
        proxy = proxies.proxy_object(self.fieldset_rw)
        self.assertIsInstance(proxy, proxies.FieldSetProxy,
            'fieldset proxy has invalid type')
        self.assertEqual(proxy.fieldset, self.fieldset_rw,
            'fieldset proxy contains invalid fieldset')

        proxy = proxies.proxy_object(self.grid_rw)
        self.assertIsInstance(proxy, proxies.GridProxy,
            'grid proxy has invalid type')
        self.assertEqual(proxy.grid, self.grid_rw,
            'grid proxy contains invalid grid')

        field = self.fieldset_rw.text
        proxy = proxies.proxy_object(field)
        self.assertIsInstance(proxy, proxies.FieldProxy,
            'field proxy has invalid type')
        self.assertEqual(proxy.field, field,
            'field proxy contains invalid field')


class TestFieldProxy(BaseCase):

    """
    Test the FieldProxy class.
    """

    def test_init(self):
        """Test the __init__ method."""
        field = self.fieldset_rw.text

        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.field, field,
            'proxy.field is invalid')
        self.assertEqual(proxy._focus, False,
            'proxy._focus is invalid when focus is default')
        self.assertEqual(proxy.mod, 'even',
            'proxy.mod is invalid when even is default')

        proxy = proxies.FieldProxy(field, even=True)
        self.assertEqual(proxy.field, field,
            'proxy.field is invalid when even is True')
        self.assertEqual(proxy._focus, False,
            'proxy._focus is invalid when even is True')
        self.assertEqual(proxy.mod, 'even',
            'proxy.mod is invalid when even is True')

        proxy = proxies.FieldProxy(field, even=False)
        self.assertEqual(proxy.field, field,
            'proxy.field is invalid when even is False')
        self.assertEqual(proxy._focus, False,
            'proxy._focus is invalid when even is False')
        self.assertEqual(proxy.mod, 'odd',
            'proxy.mod is invalid when even is False')

        proxy = proxies.FieldProxy(field, focus=True)
        self.assertEqual(proxy.field, field,
            'proxy.field is invalid when focus is True')
        self.assertEqual(proxy._focus, True,
            'proxy._focus is invalid when focus is True')
        self.assertEqual(proxy.mod, 'even',
            'proxy.mod is invalid when focus is True')

        proxy = proxies.FieldProxy(field, focus=False)
        self.assertEqual(proxy.field, field,
            'proxy.field is invalid when focus is False')
        self.assertEqual(proxy._focus, False,
            'proxy._focus is invalid when focus is False')
        self.assertEqual(proxy.mod, 'even',
            'proxy.mod is invalid when focus is False')

    def test_name(self):
        """Test the name method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.name(), field.name,
            'proxy.name is invalid')

    def test_value(self):
        """Test the value method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.value(), field.value,
            'proxy.value is invalid')

    def test_focus(self):
        """Test the focus method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertFalse(proxy.focus(),
            'proxy.focus is invalid when False and RW')
        proxy = proxies.FieldProxy(field, focus=True)
        self.assertTrue(proxy.focus(),
            'proxy.focus is invalid when True and RW')

        field = field._modified(_readonly=True)
        proxy = proxies.FieldProxy(field)
        self.assertFalse(proxy.focus(),
            'proxy.focus is invalid when False and RO')
        proxy = proxies.FieldProxy(field, focus=True)
        self.assertFalse(proxy.focus(),
            'proxy.focus is invalid when True and RO')

    def test_rendererer(self):
        """Test the renderer method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(field.renderer, proxy.renderer(),
            'proxy.renderer is invalid')

    def test_requires_label(self):
        """Test the requires_label tag."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.requires_label(), field.requires_label,
            'proxy.requires_label is invalid when RW')

        field = field._modified(_readonly=True)
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.requires_label(), field.requires_label,
            'proxy.requires_label is invalid when RO')

    def test_label_tag(self):
        """Test the label_tag method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.label_tag(), field.label_tag(),
            'proxy.label_tag is invalid when RW')

    def test_label(self):
        """Test the label method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.label(), field.label(),
            'proxy.label is invalid')

    def test_instructions(self):
        """Test the instructions method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        key = 'instructions'
        meta = field.metadata
        instructions = None
        if key in meta and meta[key]:
            instructions = meta[key]
        self.assertEqual(proxy.instructions(), instructions,
            'proxy.instructions is invalid')

    def test_metadata(self):
        """Test the metadata method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(proxy.metadata(), field.metadata,
            'proxy.metadata is invalid')

    def test_errors(self):
        """Test the errors method."""
        field = self.fieldset_rw.text
        fielderrors = field.errors
        proxy = proxies.FieldProxy(field)
        proxyerrors = proxy.errors()
        self.assertEqual(len(fielderrors), len(proxyerrors),
            'proxy.errors returned an invalid list length')
        msg = 'proxy.errors item not in field.errors'
        [self.assertEqual(e in fielderrors, msg) for e in proxyerrors]

    def test_render(self):
        """Test the render method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(field.render(), proxy.render(),
            'proxy.render is invalid')

    def test_render_readonly(self):
        """Test the render_readonly method."""
        field = self.fieldset_rw.text
        proxy = proxies.FieldProxy(field)
        self.assertEqual(field.render_readonly(), proxy.render_readonly(),
            'proxy.render_readonly is invalid')


class TestFieldSetProxy(BaseCase):

    """
    Test the FieldSetProxy object.
    """

    def test_init(self):
        """Test the __init__ method."""
        proxy = proxies.FieldSetProxy(self.fieldset_rw)
        self.assertEqual(proxy.fieldset, self.fieldset_rw,
            'proxy.fieldset is invalid')

    def test_readonly(self):
        """Test the readonly method."""
        proxy = proxies.FieldSetProxy(self.fieldset_rw)
        self.assertFalse(proxy.readonly(),
            'proxy.readonly is invalid when read/write')

        proxy = proxies.FieldSetProxy(self.fieldset_ro)
        self.assertTrue(proxy.readonly(),
            'proxy.readonly is invalid when read only')
            
    def test_fields(self):
        fields = self.fieldset_rw.render_fields.values()
        proxy = proxies.FieldSetProxy(self.fieldset_rw)
        proxyfields = proxy.fields()
        self.assertEqual(len(fields), len(proxyfields),
            'proxy.fields returns invalid number of fields')
        for pf in proxyfields:
            self.assertTrue(pf.field in fields,
                'proxy.fields contains invalid field')

    def test_errors(self):
        errorlist = ['error one', 'error two']
        errordict = [{'error': 'error one'}, {'error': 'error two'}]
        fieldset = DummyFieldSet(errorlist)
        proxy = proxies.FieldSetProxy(fieldset)
        self.assertEqual(proxy.errors(), errordict,
            'proxy.errors is invalid')

