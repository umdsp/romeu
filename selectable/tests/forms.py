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

from django.conf import settings

from selectable.forms import BaseLookupForm
from selectable.tests.base import BaseSelectableTestCase, PatchSettingsMixin


__all__ = (
    'BaseLookupFormTestCase',
)


class BaseLookupFormTestCase(PatchSettingsMixin, BaseSelectableTestCase):

    def get_valid_data(self):
        data = {
            'term': 'foo',
            'limit': 10,
        }
        return data

    def test_valid_data(self):
        data = self.get_valid_data()
        form = BaseLookupForm(data)
        self.assertTrue(form.is_valid(), u"%s" % form.errors)

    def test_invalid_limit(self):
        """
        Test giving the form an invalid limit.
        """

        data = self.get_valid_data()
        data['limit'] = 'bar'
        form = BaseLookupForm(data)
        self.assertFalse(form.is_valid())

    def test_no_limit(self):
        """
        If SELECTABLE_MAX_LIMIT is set and limit is not given then
        the form will return SELECTABLE_MAX_LIMIT.
        """

        data = self.get_valid_data()
        if 'limit' in data:
            del data['limit']
        form = BaseLookupForm(data)
        self.assertTrue(form.is_valid(), u"%s" % form.errors)
        self.assertEqual(form.cleaned_data['limit'], settings.SELECTABLE_MAX_LIMIT)

    def test_no_max_set(self):
        """
        If SELECTABLE_MAX_LIMIT is not set but given then the form
        will return the given limit.
        """

        settings.SELECTABLE_MAX_LIMIT = None
        data = self.get_valid_data()
        form = BaseLookupForm(data)
        self.assertTrue(form.is_valid(), u"%s" % form.errors)
        if 'limit' in data:
            self.assertTrue(form.cleaned_data['limit'], data['limit'])

    def test_no_max_set_not_given(self):
        """
        If SELECTABLE_MAX_LIMIT is not set and not given then the form
        will return no limit.
        """

        settings.SELECTABLE_MAX_LIMIT = None
        data = self.get_valid_data()
        if 'limit' in data:
            del data['limit']
        form = BaseLookupForm(data)
        self.assertTrue(form.is_valid(), u"%s" % form.errors)
        self.assertFalse(form.cleaned_data.get('limit'))

    def test_over_limit(self):
        """
        If SELECTABLE_MAX_LIMIT is set and limit given is greater then
        the form will return SELECTABLE_MAX_LIMIT.
        """

        data = self.get_valid_data()
        data['limit'] = settings.SELECTABLE_MAX_LIMIT + 100
        form = BaseLookupForm(data)
        self.assertTrue(form.is_valid(), u"%s" % form.errors)
        self.assertEqual(form.cleaned_data['limit'], settings.SELECTABLE_MAX_LIMIT)
