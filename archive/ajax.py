from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from archive.models import Location, Stage

@dajaxice_register
def updatestages(request, option):
    dajax = Dajax()
    loc = Location.objects.get(pk=int(option))
    stages = Stage.objects.filter(venue=loc)
    out = "<option value selected='selected'>--------------</option>"
    for stage in stages:
        out += "<option value='%d'>%s</option>" % (stage.pk, stage.__unicode__())
    dajax.assign('#id_stage', 'innerHTML', out)
    return dajax.json()
