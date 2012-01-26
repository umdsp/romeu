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
