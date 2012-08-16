# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the formalchemy_mustache.proxy module.
"""


import os
import unittest
import formalchemy_mustache
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
            DummyModel('apple', 
                'a red fruit that grows on trees'),
            DummyModel('carrot', 
                'an orange vegetable that grows in the ground'),
            DummyModel('kiwi',
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
    Test the FieldSetProxy class.
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


class TestRowProxy(BaseCase):

    """
    Test the RowProxy class.
    """

    def setUp(self):
        """Set up test data."""
        BaseCase.setUp(self)
        self.row = self.grid_rw.rows[0]

    def test_row(self):
        """Test the row attribute after __init__."""
        proxy = proxies.RowProxy(self.grid_rw, self.row, True)
        self.assertEqual(proxy.row, self.row,
            'proxy.row is invalid')

    def test_errors(self):
        """Test the errors attribute after __init__."""
        proxy = proxies.RowProxy(self.grid_rw, self.row, True)
        errors = self.grid_rw.get_errors(self.row)
        proxyerrors = proxy.errors
        self.assertEqual(len(errors), len(proxyerrors),
            'proxy.errors returned incorrect error count')
        for e in proxyerrors:
            self.assertTrue(e['error'] in errors,
                'proxy.errors returned invalid error')

    def test_fields(self):
        """Test the fields attribute after __init__."""
        proxy = proxies.RowProxy(self.grid_rw, self.row, True)
        fields = self.grid_rw.render_fields.values()
        proxyfields = proxy.fields
        self.assertEqual(len(fields), len(proxyfields),
            'proxy.fields returned incorrect error count')
        for f in proxyfields:
            self.assertTrue(f.field in fields,
                'proxy.fields returned invalid field')

    def test_mod(self):
        """Test the mod attribute after __init__."""
        proxy = proxies.RowProxy(self.grid_rw, self.row, True)
        self.assertEqual(proxy.mod, 'even',
            'proxy.mod is invalid when event is True')

        proxy = proxies.RowProxy(self.grid_rw, self.row, False)
        self.assertEqual(proxy.mod, 'odd',
            'proxy.mod is invalid when event is False')


class TestGridProxy(BaseCase):

    """
    Test the GridProxy class.
    """

    def test_init(self):
        """Test the init class."""
        proxy = proxies.GridProxy(self.grid_rw)
        self.assertEqual(proxy.grid, self.grid_rw,
            'proxy.grid is invalid')

    def test_readonly(self):
        """Test the readonly method."""
        proxy = proxies.GridProxy(self.grid_rw)
        self.assertFalse(proxy.readonly(),
            'proxy.readonly is invalid when read/write')

        proxy = proxies.GridProxy(self.grid_ro)
        self.assertTrue(proxy.readonly(),
            'proxy.readonly is invalid when read only')

    def test_labels(self):
        """Test the labels method."""
        labels = ['Name', 'Text']
        proxy = proxies.GridProxy(self.grid_rw)
        proxylabels = proxy.labels()
        self.assertEqual(len(labels), len(proxylabels),
            'proxy.labels returned incorrect label count')
        for l in proxylabels:
            self.assertTrue(l['label'] in labels,
                'proxy.labels returned invalid label')


    def test_rows(self):
        """Test the rows method."""
        proxy = proxies.GridProxy(self.grid_rw)
        rows = proxy.rows()
        self.assertEqual(len(self.models), len(rows),
            'proxy.rows returned incorrect error count')
        for r in rows:
            self.assertTrue(r.row in self.models,
                'proxy.rows returned invalid row')


class TestRender(BaseCase):

    """
    Test rendering of proxied fieldsets.
    """

    def setUp(self):
        BaseCase.setUp(self)
        formalchemy_mustache.configure()

    def get_output(self, name):
        """Get the contents of an output file."""
        outputfile = os.path.join(self.outputpath, "%s.out" % name)
        with open(outputfile) as fd:
            return fd.read()

    def check_render_output(self, name):
        """Check rendered output against an output file."""
        fs = getattr(self, name)
        output = fs.render()
        expected = self.get_output(name)
        self.assertEqual(output, expected,
            '%s.render is invalid' % name)

    def test_render_fieldset_rw(self):
        """Test rendering a read/write fieldset."""
        self.check_render_output('fieldset_rw')
    '''
    def test_render_fieldset_ro(self):
        """Test rendering a readonly fieldset."""
        self.check_render_output('fieldset_ro')

    def test_render_grid_rw(self):
        """Test rendering a read/write grid."""
        self.check_render_output('grid_rw')

    def test_render_grid_ro(self):
        """Test rendering a readonly grid."""
        self.check_render_output('grid_ro')
    '''
