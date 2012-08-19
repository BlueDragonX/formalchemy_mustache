# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Mustache field renderers.
"""

from formalchemy import config, fields
from pystache.renderer import Renderer
from formalchemy import FieldSet, fatypes
from formalchemy_mustache.proxies import proxy_object, DictProxy


class TemplateNameError(Exception):
    """
    Error raised when the template name is invalid.
    """


class BaseFieldRenderer(fields.FieldRenderer):

    """
    Render a FormAlchemy field using Mustache. This is a base class that all
    other Mustache field renderers inherit from.

    Inheriting classes should override the template, readonly_template, and
    directories attributes in order to modify the render behavior.

    The template attribute holds the name of the Mustache template used when
    rendering the field.

    The readonly_template attribute holds the name of the Mustache template
    used when rendering the field readonly. If this attribute evaluates to
    False it will be set to 'field_readonly'.

    The directories  attribute holds the Mustache template search path. If it
    evaluates to False it will be set to formalchemy.config.engine.directories.
    """

    template = None
    readonly_template = None
    directories = None

    def __init__(self, field):
        """
        Initialize the field renderer. The values of the template,
        readonly_template, and directories attributes will be validated and
        updated as necessary.

        :param field: The field to render.
        """
        fields.FieldRenderer.__init__(self, field)
        if not self.template:
            raise TemplateNameError('field renderer template may not evaluate'
                + ' to False: %s' % self.template)
        if not self.readonly_template:
            self.readonly_template = 'field_readonly'
        if not self.directories:
            self.directories = config.engine.directories
        self.renderer = Renderer(search_dirs=self.directories)

    def _render(self, template, options):
        """
        Render a template.

        :param template: The name of the template.
        :param options: Field options.
        """
        subs = {
            'name': self.name,
            'value': self.value,
            'label': self.field.label(),
            'renderer': self,
            'field': proxy_object(self.field),
            'options': proxy_object(options),
            'html': proxy_object(self.field.html_options)}
        content = self.renderer.load_template(template)
        return self.renderer.render(content, subs)

    def render(self, **options):
        """
        Render the field. The following objects are available in the template:

        name -- The name of the field.
        value -- The value of the field.
        label -- The label for the field.
        renderer -- This object.
        field -- The field being renderer. Proxied with FieldProxy.
        options -- The configured field options. Proxied with DictProxy.
        html -- Additional HTML tag attributes. Proxied with DictProxy.

        :param **options: Field renderer options.
        """
        return self._render(self.template, options)

    def render_readonly(self, **options):
        """
        Render the field readonly. See the docstring for render() for available
        template objects.

        :param **options: Field renderer options.
        """
        return self._render(self.readonly_template, options)


class MustacheFieldRenderer(BaseFieldRenderer):

    """
    Generic Mustache field renderer.
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
        self.template = template
        self.readonly_template = readonly_template
        self.directories = directories
        BaseFieldRenderer.__init__(self, field)


class WidgetSet(BaseFieldRenderer):

    """
    Render a set of widgets. Primarily used for rendering sets of radio buttons
    or checkboxes.
    """

    def selected(self, choice):
        """Check if a choice is selected."""
        if self.value is None:
            return False
        if self.field.is_collection:
            return choice in self.value
        return choice == self.value

    def proxy_choices(self, choices):
        """Format and proxy the set choices."""
        def choice(name, value, label, selected):
            return {'name': name, 'value': value, 'label': label,
                'selected': bool(selected)}
        if isinstance(choices, dict):
            choices = choices.items()
        return [choice(self.name, value, label, self.selected(value))
            for value, label in choices]

    def _serialized_value(self):
        """Serialize the value."""
        if self.name not in self.params:
            if self.field.is_collection:
                return []
            return None
        return FieldRenderer._serialized_value(self)

    def _render(self, template, options):
        """
        Render the set. The available choices should be provided in keyword
        parameter 'options'.
        """
        if 'options' not in options:
            options['options'] = []
        options['options'] = self.proxy_choices(options['options'])
        return BaseFieldRenderer._render(self, template, options)


class RadioSet(WidgetSet):
    """Render a set of radio buttons."""
    template = 'field_radio_set'


class CheckBoxSet(WidgetSet):
    """Render a set of check boxes."""
    template = 'field_checkbox_set'


class CheckBoxFieldRenderer(BaseFieldRenderer):
    """Render a checkbox input field."""
    template = 'field_checkbox'

    def _render(self, template, options):
        """Render the field."""
        options['selected'] = bool(self.value)
        return BaseFieldRenderer._render(self, template, options)


class SelectFieldRenderer(WidgetSet):
    """Render a select list."""
    template = 'field_select'
    readonly_template = 'field_select_readonly'

    def _render(self, template, options):
        """Render the select list."""
        if 'options' in options:
            if isinstance(options['options'], dict):
                options['options'] = options['options'].items()
            options['options'] = [(v, k) for k, v in options['options']]
        return WidgetSet._render(self, template, options)


class TextFieldRenderer(BaseFieldRenderer):
    """Render a text input field."""
    template = 'field_text'


class TextAreaFieldRenderer(BaseFieldRenderer):
    """Render a text field as a text area."""
    template = 'field_textarea'


class PasswordFieldRenderer(BaseFieldRenderer):
    """Render a password input field."""
    template = 'field_password'
    readonly_template = 'field_password_readonly'


class NumberFieldRenderer(BaseFieldRenderer):
    """Render a number input field."""
    template = 'field_number'


def get_default_renderers():
    """
    Generate the default_renderers attribute for a FieldSet. Overrides the
    default renderers with their formalchemy_mustache counterparts.
    """
    renderers = dict(FieldSet.default_renderers)
    renderers.update({
        fatypes.String: TextFieldRenderer,
        fatypes.Unicode: TextFieldRenderer,
        fatypes.Text: TextFieldRenderer,
        fatypes.Integer: NumberFieldRenderer,
        fatypes.Boolean: CheckBoxFieldRenderer,
        fatypes.List: SelectFieldRenderer,
        fatypes.Set: SelectFieldRenderer,
        'dropdown': SelectFieldRenderer,
        'checkbox': CheckBoxSet,
        'radio': RadioSet,
        'password': PasswordFieldRenderer,
        'textarea': TextAreaFieldRenderer,
        fatypes.HTML5Number: NumberFieldRenderer,
        'number': NumberFieldRenderer})
    return renderers

