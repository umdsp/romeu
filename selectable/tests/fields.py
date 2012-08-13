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

from selectable.forms import fields
from selectable.tests import ThingLookup
from selectable.tests.base import BaseSelectableTestCase


__all__ = (
    'AutoCompleteSelectFieldTestCase',
    'AutoComboboxSelectFieldTestCase',
    'AutoCompleteSelectMultipleFieldTestCase',
    'AutoComboboxSelectMultipleFieldTestCase',
)


class BaseFieldTestCase(BaseSelectableTestCase):
    field_cls = None
    lookup_cls = None

    def get_field_instance(self, allow_new=False, limit=None):
        return self.__class__.field_cls(self.__class__.lookup_cls, allow_new=allow_new, limit=limit)

    def test_init(self):
        field = self.get_field_instance()
        self.assertEqual(field.lookup_class, self.__class__.lookup_cls)

    def test_init_with_limit(self):
        field = self.get_field_instance(limit=10)
        self.assertEqual(field.limit, 10)
        self.assertEqual(field.widget.limit, 10)

    def test_clean(self):
        self.fail('This test has not yet been written')


class AutoCompleteSelectFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoCompleteSelectField
    lookup_cls = ThingLookup

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual(thing, value)

    def test_new_not_allowed(self):
        field = self.get_field_instance()
        value = self.get_random_string()
        self.assertRaises(forms.ValidationError, field.clean, [value, ''])

    def test_new_allowed(self):
        field = self.get_field_instance(allow_new=True)
        value = self.get_random_string()
        value = field.clean([value, ''])
        self.assertTrue(isinstance(value, ThingLookup.model))


class AutoComboboxSelectFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoComboboxSelectField
    lookup_cls = ThingLookup

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.name, thing.id])
        self.assertEqual(thing, value)

    def test_new_not_allowed(self):
        field = self.get_field_instance()
        value = self.get_random_string()
        self.assertRaises(forms.ValidationError, field.clean, [value, ''])

    def test_new_allowed(self):
        field = self.get_field_instance(allow_new=True)
        value = self.get_random_string()
        value = field.clean([value, ''])
        self.assertTrue(isinstance(value, ThingLookup.model))


class AutoCompleteSelectMultipleFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoCompleteSelectMultipleField
    lookup_cls = ThingLookup

    def get_field_instance(self, limit=None):
        return self.__class__.field_cls(self.__class__.lookup_cls, limit=limit)

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.id])
        self.assertEqual([thing], value)

    def test_clean_multiple(self):
        thing = self.create_thing()
        other_thing = self.create_thing()
        field = self.get_field_instance()
        ids = [thing.id, other_thing.id]
        value = field.clean(ids)
        self.assertEqual([thing, other_thing], value)


class AutoComboboxSelectMultipleFieldTestCase(BaseFieldTestCase):
    field_cls = fields.AutoComboboxSelectMultipleField
    lookup_cls = ThingLookup

    def get_field_instance(self, limit=None):
        return self.__class__.field_cls(self.__class__.lookup_cls, limit=limit)

    def test_clean(self):
        thing = self.create_thing()
        field = self.get_field_instance()
        value = field.clean([thing.id])
        self.assertEqual([thing], value)

    def test_clean_multiple(self):
        thing = self.create_thing()
        other_thing = self.create_thing()
        field = self.get_field_instance()
        ids = [thing.id, other_thing.id]
        value = field.clean(ids)
        self.assertEqual([thing, other_thing], value)

