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

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from archive.models import Location, Stage

@dajaxice_register
def updatestages(request, option):
    dajax = Dajax()
    loc = Location.objects.get(pk=int(option))
    stages = Stage.objects.filter(venue=loc)
    out = "<option value selected='selected'>------------</option>"
    for stage in stages:
        out += "<option value='%d'>%s</option>" % (stage.pk, stage.__unicode__())
    dajax.remove('#id_stage option')
    dajax.assign('#id_stage', 'innerHTML', out)
    return dajax.json()
