# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Mustache field renderers.
"""

from formalchemy import config, fields
from pystache.renderer import Renderer


class MustacheFieldRenderer(fields.FieldRenderer):

    """
    Renderer a FormAlchemy field using a Mustache template.
    """

    def __init__(self, field, template, directories=None):
        """
        Initialize the field renderer.

        :param field: The field to render.
        :param template: The template to use.
        :param directories: The directories to search for the template in. If
            None then this will be taken from formalchemy.config.engine.
        """
        fields.FieldRenderer.__init__(self, field)
        if directories is None:
            directories = config.engine.directories
        self.template = template
        self.renderer = Renderer(search_dirs=directories)

    def render(self, **kw):
        """
        Render the field.

        :param **kw: Additional to substitute in the template.
        """
        kw.update({
            'name': self.name,
            'value': self.value})
        content = self.renderer.load_template(self.template)
        return self.renderer.render(content, kw)

    @classmethod
    def factory(cls, template, directories=None):
        """
        Create a field renderer that uses the given template.

        :param field: The field to render.
        :param template: The template to use.
        :param directories: The directories to search for the template in. If
            None then this will be taken from formalchemy.config.engine.
        """
        class MustacheMetaFieldRenderer(MustacheFieldRenderer):
            """
            Renderer a FormAlchemy field using a mustache template.
            """
            def __init__(self, field):
                """Initialize the field renderer."""
                MustacheFieldRenderer.__init__(self, field, template,
                    directories)
        return MustacheMetaFieldRenderer

