# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Mustache field renderers.
"""

from formalchemy import config, fields
from pystache.renderer import Renderer
from formalchemy_mustache.proxies import proxy_object


class MustacheFieldRenderer(fields.FieldRenderer):

    """
    Renderer a FormAlchemy field using a Mustache template.
    """

    def __init__(self, field, template, readonly_template=None,
            directories=None):
        """
        Initialize the field renderer.

        :param field: The field to render.
        :param template: The template to use when rendering the field.
        :param readonly_template: The template to use when rendering the field
            readonly. If None defaults to 'field_readonly'.
        :param directories: The directories to search for the template in. If
            None then this will be taken from formalchemy.config.engine.
        """
        fields.FieldRenderer.__init__(self, field)
        if directories is None:
            directories = config.engine.directories
        if readonly_template is None:
            readonly_template = 'field_readonly'
        self.template = template
        self.readonly_template = readonly_template
        self.renderer = Renderer(search_dirs=directories)

    def _render(self, template, subs):
        """
        Render a template.

        :param template: The name of the template.
        :param subs: Template substitutions.
        """
        subs.update({'field': proxy_object(self.field)})
        content = self.renderer.load_template(template)
        return self.renderer.render(content, subs)

    def render(self, **kw):
        """
        Render the field.

        :param **kw: Additional template substitutions.
        """
        return self._render(self.template, kw)

    def render_readonly(self, **kw):
        """
        Render the field readonly.

        :param **kw: Additional template substitutions.
        """
        return self._render(self.readonly_template, kw)

    @classmethod
    def factory(cls, template, readonly_template=None, directories=None):
        """
        Create a field renderer that uses the given template.

        :param field: The field to render.
        :param template: The template to use when rendering the field.
        :param readonly_template: The template to use when rendering the field
            readonly. If None defaults to 'field_readonly'.
        :param directories: The directories to search for the template in. If
            None then this will be taken from formalchemy.config.engine.
        """
        class Renderer(MustacheFieldRenderer):
            def __init__(self, field):
                """Initialize the field renderer."""
                MustacheFieldRenderer.__init__(self, field, template,
                    readonly_template, directories)
        Renderer.__doc__ = ('Render a field using the %s Mustache template.' %
            template)
        return Renderer

