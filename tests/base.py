# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Base test case classes.
"""

import os
import unittest
import formalchemy_mustache
from .dummy import DummyModel
from formalchemy.forms import FieldSet
from formalchemy.tables import Grid


class BaseCase(unittest.TestCase):

    """
    Set up test data for test cases.
    """

    def setUp(self):
        """Set up test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        package_here = os.path.abspath(
            os.path.dirname(formalchemy_mustache.__file__))

        self.templates = [os.path.join(here, 'templates')]
        self.package_templates = [os.path.join(package_here, 'templates')]


        self.outputpath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'output')

        self.models = [
            DummyModel('apple', 
                'a red fruit that grows on trees', 5, True),
            DummyModel('carrot', 
                'an orange vegetable that grows in the ground', 2, True),
            DummyModel('kiwi',
                'a brown fruit that is not a flightless bird', 12, False)]
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

        self.field = self.fieldset_rw.name
        self.field_text = self.fieldset_rw.text
        self.field_quantity = self.fieldset_rw.quantity
        self.field_instock = self.fieldset_rw.instock
        self.field_none = fs.name

        self.set_options = [
            ('apple', 'Red Apple'),
            ('orange', 'Florida Orange'),
            ('grape', 'Green Grape')]
        self.select_options = [(v, k) for k, v in self.set_options]

    def get_output(self, name):
        """Get the contents of an output file."""
        outputfile = os.path.join(self.outputpath, "%s.out" % name)
        with open(outputfile) as fd:
            return fd.read()

