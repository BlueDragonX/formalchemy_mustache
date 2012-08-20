# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implement Mustaches support in FormAlchemy
"""

import os
from formalchemy import config
from formalchemy_mustache.engines import MustacheEngine


__all__ = ['configure']


def configure(directories=None):
    """
    Configure FormAlchemy to use the Mustache template engine.

    :param directories: A list of directories to search for templates in.
    """
    if directories is None:
        directories = []
    here = os.path.abspath(os.path.dirname(__file__))
    directories = directories + [os.path.join(here, 'templates')]
    config.engine = MustacheEngine(directories=directories)

