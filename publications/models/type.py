__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from publications.models.orderedmodel import OrderedModel
from string import replace, split, strip

class Type(OrderedModel):
	class Meta:
		ordering = ('order',)
		app_label = 'publications'

	type = models.CharField(max_length=128)
	description = models.TextField(verbose_name=_('Description'))
	bibtex_types = models.CharField(max_length=256, default='article',
			verbose_name='BibTex types',
			help_text='Possible BibTex types, separated by comma.')
	hidden = models.BooleanField(
		help_text='Hide publications in all view.')
	owned_by_library = models.BooleanField(verbose_name=_('Display in Front End'),
		help_text='Show in publications type display in front end.')
	

	def __unicode__(self):
		return self.type


	def __init__(self, *args, **kwargs):
		OrderedModel.__init__(self, *args, **kwargs)

		self.bibtex_types = replace(self.bibtex_types, '@', '')
		self.bibtex_types = replace(self.bibtex_types, ';', ',')
		self.bibtex_types = replace(self.bibtex_types, 'and', ',')
		self.bibtex_type_list = [strip(s).lower()
			for s in split(self.bibtex_types, ',')]
		self.bibtex_types = ', '.join(self.bibtex_type_list)
		self.bibtex_type = self.bibtex_type_list[0]
