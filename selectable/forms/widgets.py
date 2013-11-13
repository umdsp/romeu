# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.http import urlencode
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


__all__ = (
    'AutoCompleteWidget',
    'AutoCompleteSelectWidget',
    'AutoComboboxWidget',
    'AutoComboboxSelectWidget',
    'AutoCompleteSelectMultipleWidget',
    'AutoComboboxSelectMultipleWidget',
)


MEDIA_URL = settings.MEDIA_URL
STATIC_URL = getattr(settings, 'STATIC_URL', '')
MEDIA_PREFIX = STATIC_URL or MEDIA_URL


class SelectableMediaMixin(object):

    class Media(object):
        css = {
            'all': ('%scss/dj.selectable.css' % MEDIA_PREFIX, )
        }
        js = ('%sjs/jquery.dj.selectable.js' % MEDIA_PREFIX, )


class AutoCompleteWidget(forms.TextInput, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.qs = {}
        self.limit = kwargs.pop('limit', None)
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def update_query_parameters(self, qs_dict):
        self.qs.update(qs_dict)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoCompleteWidget, self).build_attrs(extra_attrs, **kwargs)
        url = self.lookup_class.url()
        if self.limit and 'limit' not in self.qs:
            self.qs['limit'] = self.limit
        if self.qs:
            url = '%s?%s' % (url, urlencode(self.qs))
        attrs[u'data-selectable-url'] = url
        attrs[u'data-selectable-type'] = 'text'
        attrs[u'data-selectable-allow-new'] = str(self.allow_new).lower()
        return attrs

class SelectableMultiWidget(forms.MultiWidget):

    def update_query_parameters(self, qs_dict):
        self.widgets[0].update_query_parameters(qs_dict)


class AutoCompleteSelectWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        widgets = [
            AutoCompleteWidget(lookup_class, allow_new=self.allow_new, limit=self.limit),
            forms.HiddenInput(attrs={u'data-selectable-type': 'hidden'})
        ]
        self.choices = None
        super(AutoCompleteSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            model = getattr(self.lookup_class, 'model', None)
            if model and isinstance(value, model):
                item = value
                value = lookup.get_item_id(item)
            else:
                item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]


class AutoComboboxWidget(AutoCompleteWidget, SelectableMediaMixin):

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoComboboxWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs[u'data-selectable-type'] = 'combobox'
        return attrs


class AutoComboboxSelectWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        widgets = [
            AutoComboboxWidget(lookup_class, allow_new=self.allow_new, limit=self.limit),
            forms.HiddenInput(attrs={u'data-selectable-type': 'hidden'})
        ]
        super(AutoComboboxSelectWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            lookup = self.lookup_class()
            model = getattr(self.lookup_class, 'model', None)
            if model and isinstance(value, model):
                item = value
                value = lookup.get_item_id(item)
            else:
                item = lookup.get_item(value)
            item_value = lookup.get_item_value(item)
            return [item_value, value]
        return [None, None]


class LookupMultipleHiddenInput(forms.MultipleHiddenInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        super(LookupMultipleHiddenInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        lookup = self.lookup_class()
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        model = getattr(self.lookup_class, 'model', None)
        for i, v in enumerate(value):
            item = None
            if model and isinstance(v, model):
                item = v
                v = lookup.get_item_id(item)
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            if v:
                item = item or lookup.get_item(v)
                input_attrs['title'] = lookup.get_item_value(item)
            inputs.append(u'<input%s />' % flatatt(input_attrs))
        return mark_safe(u'\n'.join(inputs))

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(LookupMultipleHiddenInput, self).build_attrs(extra_attrs, **kwargs)
        attrs[u'data-selectable-type'] = 'hidden-multiple'
        return attrs


class AutoCompleteSelectMultipleWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.limit = kwargs.pop('limit', None)
        self.choices = None
        position = kwargs.pop('position', 'bottom')
        attrs = {
            u'data-selectable-multiple': 'true',
            u'data-selectable-position': position
        }
        widgets = [
            AutoCompleteWidget(lookup_class, allow_new=False, limit=self.limit, attrs=attrs),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoCompleteSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return self.widgets[1].value_from_datadict(data, files, name + '_1')

    def render(self, name, value, attrs=None):
        if value and not hasattr(value, '__iter__'):
            value = [value]
        value = [u'', value]
        return super(AutoCompleteSelectMultipleWidget, self).render(name, value, attrs)


class AutoComboboxSelectMultipleWidget(SelectableMultiWidget, SelectableMediaMixin):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.limit = kwargs.pop('limit', None)
        position = kwargs.pop('position', 'bottom')
        attrs = {
            u'data-selectable-multiple': 'true',
            u'data-selectable-position': position
        }
        widgets = [
            AutoComboboxWidget(lookup_class, allow_new=False, limit=self.limit, attrs=attrs),
            LookupMultipleHiddenInput(lookup_class)
        ]
        super(AutoComboboxSelectMultipleWidget, self).__init__(widgets, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return self.widgets[1].value_from_datadict(data, files, name + '_1')

    def render(self, name, value, attrs=None):
        if value and not hasattr(value, '__iter__'):
            value = [value]
        value = [u'', value]
        return super(AutoComboboxSelectMultipleWidget, self).render(name, value, attrs)

