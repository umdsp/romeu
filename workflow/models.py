from django.db import models
from django.db.models import Min, Max, Avg, Count
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

from unidecode import unidecode
from archive.models import DigitalObject

class Queue(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("queue title"))
    
    def __unicode__(self):
        return self.title

class QueueItem(models.Model):
    object = models.ForeignKey(DigitalObject, related_name="queue_item", verbose_name=_("digital object"))
    phys_assessed = models.BooleanField(default=False, verbose_name=_("physical assessment"))
    captured = models.BooleanField(default=False, verbose_name=_("capture"))
    post_proc = models.BooleanField(default=False, verbose_name=_("post-processing"))
    supervisor_qc = models.BooleanField(default=False, verbose_name=_("supervisor QC"))
    edited = models.BooleanField(default=False, verbose_name=_("editing"))
    metadata = models.BooleanField(default=False, verbose_name=_("final metadata"))
    prepped = models.BooleanField(default=False, verbose_name=_("prep for release"))
    high_priority = models.BooleanField(default=False, verbose_name=_("high priority?"))
    queue = models.ForeignKey("Queue", related_name="queue_items", verbose_name=_("queue"))
    
    def object_number(self):
        return self.object.object_number()
    
    def __unicode__(self):
        return self.object.title
        
    def link_to(self):
        return "<a href='/admin/archive/digitalobject/" + str(self.object.id) + "/'>Edit Digital Object Record</a>"
    link_to.allow_tags = True
    link_to.short_description = _("link")