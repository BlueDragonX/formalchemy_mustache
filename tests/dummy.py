# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Dummy classes for testing.
"""

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class DummyPackage(object):

    """
    Dummy Pyramid package class.
    """

    def __init__(self, name):
        """Initialize the package object with a name."""
        self.__name__ = name


class DummyConfig(object):

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


class DummyModel(Base):

    """
    Dummy SqlAlchemy model.
    """

    __tablename__ = 'dummy'
    name = Column(String, primary_key=True)
    text = Column(String)
    quantity = Column(Integer)
    instock = Column(Boolean)

    def __init__(self, name=None, text=None, quantity=None, instock=None):
        """Initialize the model object."""
        if name is not None:
            self.name = name
        if text is not None:
            self.text = text
        if quantity is not None:
            self.quantity = quantity
        if instock is not None:
            self.instock = instock


class DummyFieldSet(object):

    """
    Dummy FieldSet object.
    """

    def __init__(self, errors):
        """Initialize the object."""
        self.errors = errors

