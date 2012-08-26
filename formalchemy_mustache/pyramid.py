# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Configure FormAlchemy to use Mustache through pyramid_mustache.
"""

from __future__ import absolute_import
import os
import formalchemy
import formalchemy_mustache
import pyramid_mustache
from formalchemy_mustache.engines import MustacheEngine
from pyramid.path import AssetResolver


__all__ = ['configure']


def resolve_search_path(path):
    """Resolve a template form search path."""
    if ':' in path:
        path = [AssetResolver().resolve(path).abspath()]
    elif os.path.isabs(path):
        path = [path]
    else:
        path = [os.path.join(base, path)
            for base in pyramid_mustache.session.search]
    return [os.path.realpath(p) for p in path]

def configure(config):
    """
    Use Pyramid to configure FormAlchemy to use Mustache.

    Settings:
      mustache.forms -- The search directories for form templates. Either a
          comma separated list of asset specs or relative directories. If not
          an asset spec then it will be resolved relative to the
          mustache.search value.
    """
    paths = []
    forms_key = 'mustache.forms'
    settings = config.get_settings()

    if forms_key in settings:
        paths = settings[forms_key].split(',')
    if len(paths) == 0:
        paths.append('.')

    directories = []
    [directories.extend(resolve_search_path(path)) for path in paths]
    formalchemy_mustache.configure(directories)

