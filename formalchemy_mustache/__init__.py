# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implement Mustaches support in FormAlchemy
"""

from formalchemy import config
from formalchemy_mustache.engines import MustacheEngine


def configure(directories=None):
    """
    Configure FormAlchemy to use the Mustache template engine.

    :param directories: A list of directories to search for templates in.
    """
    config.engine = MustacheEngine(directories=directories)

