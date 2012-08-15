# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Proxy FormAlchemy objects for Mustache ease-of-use.
"""

from formalchemy.forms import FieldSet
from formalchemy.tables import Grid
from formalchemy.fields import AbstractField


def proxy_errors(errors):
    """
    Proxy a list of errors. Returns a list of dicts. Each dict contains one
    item with key 'error'. This item contains the error text.
    """
    if errors is None:
        return []
    return [{'error': error} for error in errors]


def proxy_fields(fields, focus=None):
    """
    Proxy a list of fields. If focus is a field object in fields then that
    proxied field will have its focus attribute set to True. If focus is True
    then the first proxied field in fields will have its focus attribute set to
    True.
    """
    fields = fields.values()
    fields = [FieldProxy(fields[i], i % 2, fields[i]==focus)
        for i in range(len(fields))]
    if len(fields) > 0 and focus is True:
        fields[0]._focus = True
    return fields


def proxy_object(obj):
    """
    Proxy an object. Uses the appropriate proxy class for that object type. If
    the object type is not supported the object is returned unmodified.
    """
    if isinstance(obj, Grid):
        return GridProxy(obj)
    if isinstance(obj, FieldSet):
        return FieldSetProxy(obj)
    if isinstance(obj, AbstractField):
        return FieldProxy(obj)
    return obj


class FieldProxy(object):

    """
    Proxy a Field object.
    """

    def __init__(self, field, even=None, focus=False):
        """Initialize the object."""
        self.field = field
        self._focus = focus
        if even is None:
            even = True
        self.mod = even and 'even' or 'odd'

    def name(self):
        """Get the name of the field."""
        if not hasattr(self.field, 'name'):
            return None
        return self.field.name

    def value(self):
        """Get the value of the field."""
        if not hasattr(self.field, 'value'):
            return None
        return self.field.value

    def focus(self):
        """Return true if the field should have focus."""
        return self._focus and not self.field.is_readonly()

    def renderer(self):
        """Get the field renderer."""
        return self.field.renderer

    def requires_label(self):
        """Return true if the label is required."""
        return self.field.requires_label

    def label_tag(self):
        """Render the label tag."""
        return self.field.label_tag()

    def label(self):
        """Get the label text."""
        label = self.field.label()
        if not label:
            return None
        return label

    def instructions(self):
        """Get the field instructions."""
        key = 'instructions'
        meta = self.field.metadata
        if key not in meta or not meta[key]:
            return None
        return meta[key]

    def metadata(self):
        """Get the field metadata."""
        return self.field.metadata

    def errors(self):
        """
        Get a list of errors that have occurred. Each item in the list is a one
        element dict with 'error' as the key.
        """
        return proxy_errors(self.field.errors)

    def render(self):
        """Render the field."""
        return self.field.render()

    def render_readonly(self):
        """Render the field read-only."""
        return self.field.render_readonly()


class FieldSetProxy(object):

    """
    Proxy a FieldSet object.
    """

    def __init__(self, fieldset):
        """Initialize the object."""
        self.fieldset = fieldset

    def readonly(self):
        """Return true if the fieldset is readonly."""
        return bool(self.fieldset.readonly)

    def fields(self):
        """Get a list of fields to render."""
        return proxy_fields(self.fieldset.render_fields, self.fieldset.focus)

    def errors(self):
        """
        Get a list of errors that have occurred. Each item in the list is a one
        element dict with 'error' as the key.
        """
        return proxy_errors(self.fieldset.errors)


class RowProxy(object):

    """
    Proxy a grid row.
    """

    def __init__(self, grid, row, even):
        """Initialize the row."""
        grid._set_active(row)
        self.errors = proxy_errors(grid.get_errors(row))
        self.fields = proxy_fields(grid.render_fields, grid.focus)
        self.mod = even and 'even' or 'odd'


class GridProxy(object):

    """
    Proxy a Grid object.
    """

    def __init__(self, grid):
        """Initialize the object."""
        self.grid = grid

    def readonly(self):
        """Return wether or not the fieldset is readonly."""
        return bool(self.grid.readonly)

    def labels(self):
        """
        Get a list of column labels. Each item in the list is a dict with a
        single item 'label'.
        """
        fields = self.grid.render_fields
        return {'label': v.label() for v in fields.itervalues()}

    def rows(self):
        """Return a list of rows on the grid."""
        rows = self.grid.rows
        return [RowProxy(self.grid, rows[i], i % 2) for i in range(len(rows))]

