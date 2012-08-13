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
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext as _

from selectable.forms.widgets import AutoCompleteSelectWidget, AutoComboboxSelectWidget
from selectable.forms.widgets import AutoCompleteSelectMultipleWidget, AutoComboboxSelectMultipleWidget

__all__ = (
    'AutoCompleteSelectField',
    'AutoComboboxSelectField',
    'AutoCompleteSelectMultipleField',
    'AutoComboboxSelectMultipleField',
)


class AutoCompleteSelectField(forms.Field):
    widget = AutoCompleteSelectWidget

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.limit = kwargs.pop('limit', None)
        kwargs['widget'] = self.widget(lookup_class, allow_new=self.allow_new, limit=self.limit)
        super(AutoCompleteSelectField, self).__init__(*args, **kwargs)


    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, list):
            # Input comes from an AutoComplete widget. It's two
            # components: text and id
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid_choice'])
            lookup =self.lookup_class()
            if value[1] in EMPTY_VALUES:
                if not self.allow_new:
                    if value[0]:
                        raise ValidationError(self.error_messages['invalid_choice'])
                    else:
                        return None
                value = lookup.create_item(value[0])  
            else:
                value = lookup.get_item(value[1])
                if value is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
        return value


class AutoComboboxSelectField(AutoCompleteSelectField):
    widget = AutoComboboxSelectWidget


class AutoCompleteSelectMultipleField(forms.Field):
    widget = AutoCompleteSelectMultipleWidget

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of the available choices.'),
    }

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.limit = kwargs.pop('limit', None)
        kwargs['widget'] = self.widget(lookup_class, limit=self.limit)
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        lookup = self.lookup_class()
        items = []
        for v in value:
            if v not in EMPTY_VALUES:
                item = lookup.get_item(v)
                if item is None:
                    raise ValidationError(self.error_messages['invalid_choice'])
                items.append(item)
        return items


class AutoComboboxSelectMultipleField(AutoCompleteSelectMultipleField):
    widget = AutoComboboxSelectMultipleWidget
