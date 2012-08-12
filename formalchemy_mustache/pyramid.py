# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Configure FormAlchemy to use Mustache through pyramid_mustache.
"""

from formalchemy import config
from pyramid_mustache import session
from formalchemy_mustache.engines import MustacheEngine


def configure(config):
    """
    Use pyramid and pyramid_mustache to configure FormAlchemy to use Mustache.
    """
    directories = session.get_templates(config.package)
    config.engine = MustacheEngine(directories=directories)

