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

from django import template
from archive.models import DigitalObject, DigitalFile, DigitalObjectType, HomePageInfo
from random import randrange
from sorl.thumbnail import get_thumbnail

register = template.Library()

def random_object_fig(parser, token):
    try:
        tag_name = token
    except ValueError:
        raise template.TemplateSyntaxError("Something went wrong while creating a random object figure.")
    return RandomObjectFigNode()

class RandomObjectFigNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        imagetype = DigitalObjectType.objects.get(title="Image")
        dos = DigitalObject.objects.filter(published=True, files__isnull=False, digi_object_format=imagetype)
        length = len(dos) - 1
        notfound = True
        while notfound:
            num = randrange(0, length)
            if dos[num].files.count() > 0 and dos[num].files.all()[0]:
                im = get_thumbnail(dos[num].files.all()[0].filepath, "210x210", crop="center")
                fig = "<figure><a href='/digitalobject/"
                fig += str(dos[num].pk)
                fig += "'><img src='"
                fig += im.url
                fig += "' alt='' /></a><figcaption><a href='/digitalobject/"
                fig += str(dos[num].pk)
                fig += "'>"
                fig += dos[num].title
                fig += "</a></figcaption></figure>"
                notfound = False
                return fig

register.tag('random_object_fig', random_object_fig)
