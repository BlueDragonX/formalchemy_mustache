# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Mustache template engine.
"""

from formalchemy.templates import TemplateEngine
from pystache.renderer import Renderer
from formalchemy_mustache.proxies import proxy_object


__all__ = ['MustacheEngine']


class MustacheEngine(TemplateEngine):

    """
    Mustache template engine.
    """

    def __init__(self, **kw):
        """
        Initialize the template renderer.

        :param directories: Keyword parameter. A list of directories used as
            the search path for templates.
        """
        self.renderer = Renderer(search_dirs=kw['directories'])
        TemplateEngine.__init__(self, **kw)

    def get_template(self, name, **kw):
        """
        Get a template.

        :param name: The name of the template.
        """
        parts = name.rsplit('.', 2)
        if len(parts) > 1 and parts[1] == 'mustache':
            name = parts[0]
        return self.renderer.load_template(name)


    def render(self, name, **kw):
        """
        Render a template.

        :param name: The name of the template.
        :param **kw: The values to substitute in the template.
        """
        kw = {k: proxy_object(v) for k, v in kw.iteritems()}
        template = self.templates.get(name, None)
        return self.renderer.render(template, kw)

