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
    Generic FormAlchemy field renderer using Mustache.
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

    def _render(self, template, opts):
        """
        Render a template.

        :param template: The name of the template.
        :param opts: Field options.
        """
        subs = {
            'renderer': self,
            'field': proxy_object(self.field),
            'options': proxy_object(opts),
            'html': proxy_object(self.field.html_options)}
        content = self.renderer.load_template(template)
        return self.renderer.render(content, subs)

    def render(self, **opts):
        """
        Render the field.

        :param **opts: Field renderer options.
        """
        return self._render(self.template, opts)

    def render_readonly(self, **opts):
        """
        Render the field readonly.

        :param **opts: Field renderer options.
        """
        return self._render(self.readonly_template, opts)


class BaseFieldRenderer(MustacheFieldRenderer):

    """
    Mustache field renderer which uses class attributes to configure itself.
    """

    template = None
    readonly_template = None
    directories = None

    def __init__(self, field):
        """
        Initialize the field renderer. Calls MustacheFieldRenderer.__init__
        with self.template, self.readonly_template, and self.directories for
        the template, readonly_template, and directories parameters. These
        values are None by default and should be overridden by the inheriting
        class. The template attribute is required at minimum.

        :param field: The field to render.
        """
        MustacheFieldRenderer.__init__(self, field, self.template,
            self.readonly_template, self.directories)


class TextFieldRenderer(BaseFieldRenderer):
    """Render a text input field."""
    template = 'field_text'


