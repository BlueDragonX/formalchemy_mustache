# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Configure FormAlchemy to use Mustache through pyramid_mustache.
"""

import os
import formalchemy
import formalchemy_mustache
from pyramid_mustache import session
from formalchemy_mustache.engines import MustacheEngine

__all__ = ['configure']


def configure(config):
    """
    Use Pyramid to configure FormAlchemy to use Mustache.

    Settings:
      mustache.forms -- A subdirectory under the templates path to search for
        form templates in.
    """
    templates_key = 'mustache.forms'
    settings = config.get_settings()
    directories = session.get_templates(config.package)
    if templates_key in settings:
        s = settings[templates_key]
        directories = [os.path.join(d, s) for d in directories]
    formalchemy_mustache.configure(directories)

