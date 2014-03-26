# -*- coding: utf-8 -*-

__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.http import urlquote_plus
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from string import split, strip, join, replace, ascii_uppercase

from publications.fields import PagesField
from publications.models import Type


from taggit_autocomplete_modified.managers import TaggableManager

try:
	from south.modelsinspector import add_introspection_rules

	add_introspection_rules(
	[
		(
			(TaggableManager, ), [], {},
		),
	
	],
	["^taggit_autocomplete_modified\.managers\.TaggableManager",
	 ])

except ImportError:
	pass


class Publication(models.Model):
	class Meta:
		app_label = 'publications'
		ordering = ['-year', '-month', '-id']
		verbose_name = _('bibliographic record')
		verbose_name_plural = _('bibliographic records')
		

	# names shown in admin area
	MONTH_CHOICES = (
			(1, 'January'),
			(2, 'February'),
			(3, 'March'),
			(4, 'April'),
			(5, 'May'),
			(6, 'June'),
			(7, 'July'),
			(8, 'August'),
			(9, 'September'),
			(10, 'October'),
			(11, 'November'),
			(12, 'December')
		)

	# abbreviations used in BibTex
	MONTH_BIBTEX = {
			1: 'Jan',
			2: 'Feb',
			3: 'Mar',
			4: 'Apr',
			5: 'May',
			6: 'Jun',
			7: 'Jul',
			8: 'Aug',
			9: 'Sep',
			10: 'Oct',
			11: 'Nov',
			12: 'Dec'
		}

	type = models.ForeignKey(Type)
	annote=models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Annotation"),
		help_text='An annotation. It is not used by the standard bibliography styles.')
	citekey = models.CharField(max_length=512, blank=True, null=True, db_index=True,
		help_text='BibTex citation key. Leave blank if unsure.')
	title = models.CharField(max_length=255,
							 help_text="The work's title")
	short_title = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("short title"))
	authors = models.CharField(max_length=2048,
		help_text='List of authors separated by commas or <i>and</i>.', verbose_name=_("author(s)"))
	book_title = models.CharField(max_length=255, null=True, blank=True,
								  help_text=_("Only for works contained in a larger book"),
								  verbose_name=_("book title"))
	chapter = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("chapter"))
	how_published = models.CharField(max_length=20, null=True, blank=True,
							   verbose_name=_("How Published"),
							   help_text="How something strange has been published. The first word should be capitalized.")
	year = models.PositiveIntegerField(max_length=4, db_index=True)
	month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
	journal = models.CharField(max_length=256, blank=True, db_index=True)

	isbn = models.CharField(max_length=32, verbose_name="ISBN", blank=True,
		help_text='Only for a book.') # A-B-C-D
	issn = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("ISSN"))
	doi = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("DOI"))
	editor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("editor(s)"))
	institution = models.CharField(max_length=256, blank=True, null=True,
								   help_text="The sponsoring institution of a technical report. ")
	organization = models.CharField(max_length=256, blank=True, null=True,
								   help_text="The organization that sponsors a conference or that publishes a manual.",
								   verbose_name=_("Organization"))
	price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Price"),
								help_text="The price of the document. ")
	table_of_content = models.TextField(null=True, blank=True, verbose_name=_("Table of Content"))
	note = models.CharField(max_length=256, blank=True)
	keywords = models.CharField(max_length=256, blank=True,
		help_text='List of keywords separated by commas.')
	url = models.URLField(null=True, blank=True, verbose_name='URL',
		help_text='Link to PDF or journal page.')
	code = models.URLField(blank=True,
		help_text='Link to page with code.')
	pdf = models.FileField(upload_to='publications/', verbose_name='PDF', blank=True, null=True)
	external = models.BooleanField(
		help_text='If publication was written in another lab, mark as external.')
	abstract = models.TextField(null=True, blank=True, verbose_name=_("abstract"))

	translator = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("translator(s)"))
	volume = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Volume number"))
	number = models.CharField(max_length=40, null=True, blank=True, help_text=_("Issue number"), verbose_name=_("issue number"))
	series = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series title"), verbose_name=_("series"))
	series_text = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series subtitle"), verbose_name=_("series text"))
	series_num = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("series number"))

	edition = models.CharField(max_length=255, null=True, blank=True, help_text=_("Enter as an ordinal number ('Second', 'Third')"), verbose_name=_("edition"))
	section = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("section"))

	pub_date = models.DateField(null=True, blank=True, verbose_name=_("publication date"))
	season = models.CharField(max_length=255, null=True, blank=True, help_text=_("Publication time in the year, ex: Spring, Fall, etc."), verbose_name=_("Season"))
	access_date = models.DateField(null=True, blank=True, verbose_name=_("accessed date"))
	
	language = models.CharField(max_length=60, null=True, blank=True, verbose_name=_("language"))
	pages = models.CharField(max_length=30, null=True, blank=True, help_text=_("Enter one or more pages / page ranges"), verbose_name=_("pages"))
	publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publisher"))
	address = models.CharField(max_length=255, null=True, blank=True, help_text=_("Publisher's address; omit for major publishers"), verbose_name=_("address"))
	medium = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("medium"))

	art_size = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("artwork size"))
	label = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("label"))
	runtime = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("running time"))
	archive = models.CharField(max_length=255, null=True, blank=True, help_text=_("An archive that holds this item"), verbose_name=_("archive"))
	archive_location = models.CharField(max_length=200, null=True, blank=True, help_text=_("A call number or location within the archive holding this item"), verbose_name=_("location in archive"))
	version = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("version"))
	system = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("system"))

	university = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("university"))
	library = models.CharField(max_length=255, null=True, blank=True, help_text=_("A library that holds this item"), verbose_name=_("library"))
	library_catalog_num = models.CharField(max_length=255, null=True, blank=True, help_text=_("The catalog call number for the library holding this item"), verbose_name=_("library catalog number"))
	rights = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("rights"))
	extra = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("extra"))
	tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)
	
	
	def __init__(self, *args, **kwargs):
		models.Model.__init__(self, *args, **kwargs)

		# post-process keywords
		self.keywords = replace(self.keywords, ';', ',')
		self.keywords = replace(self.keywords, ', and ', ', ')
		self.keywords = replace(self.keywords, ',and ', ', ')
		self.keywords = replace(self.keywords, ' and ', ', ')
		self.keywords = [strip(s).lower() for s in split(self.keywords, ',')]
		self.keywords = join(self.keywords, ', ').lower()

		# post-process author names
		self.authors = replace(self.authors, ', and ', ', ')
		self.authors = replace(self.authors, ',and ', ', ')
		self.authors = replace(self.authors, ' and ', ', ')
		self.authors = replace(self.authors, ';', ',')

		# list of authors
		self.authors_list = [strip(author) for author in split(self.authors, ',')]

		# simplified representation of author names
		self.authors_list_simple = []

		# tests if title already ends with a punctuation mark
		self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] \
			if len(self.title) > 0 else False

		suffixes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', "Jr.", "Sr."]
		prefixes = ['Dr.']
		prepositions = ['van', 'von', 'der', 'de', 'den']

		# further post-process author names
		for i, author in enumerate(self.authors_list):
			if author == '':
				continue

			names = split(author, ' ')

			# check if last string contains initials
			if (len(names[-1]) <= 3) \
				and names[-1] not in suffixes \
				and all(c in ascii_uppercase for c in names[-1]):
				# turn "Gauss CF" into "C. F. Gauss"
				names = [c + '.' for c in names[-1]] + names[:-1]

			# number of suffixes
			num_suffixes = 0
			for name in names[::-1]:
				if name in suffixes:
					num_suffixes += 1
				else:
					break

			"""		
			# abbreviate names
			for j, name in enumerate(names[:-1 - num_suffixes]):
				# don't try to abbreviate these
				if j == 0 and name in prefixes:
					continue
				if j > 0 and name in prepositions:
					continue

				if (len(name) > 2) or (len(name) and (name[-1] != '.')):
					k = name.find('-')
					if 0 < k + 1 < len(name):
						# take care of dash
						names[j] = name[0] + '.-' + name[k + 1] + '.'
					else:
						names[j] = name[0] + '.'
			"""
			
			if len(names):
				self.authors_list[i] = join(names, ' ')

				# create simplified/normalized representation of author name
				if len(names) > 1:
					for name in names[0].split('-'):
						name_simple = self.simplify_name(join([name, names[-1]], ' '))
						self.authors_list_simple.append(name_simple)
				else:
					self.authors_list_simple.append(self.simplify_name(names[0]))

		# list of authors in BibTex format
		self.authors_bibtex = join(self.authors_list, ' and ')

		# overwrite authors string
		if len(self.authors_list) > 2:
			self.authors = join([
				join(self.authors_list[:-1], ', '),
				self.authors_list[-1]], ', and ')
		elif len(self.authors_list) > 1:
			self.authors = "%s, %s" % (self.authors_list[0], self.authors_list[1])
		else:
			self.authors = "%s" % (self.authors_list[0]) #self.authors_list #[0]

	def __unicode__(self):
		return self.title

	"""
	def __unicode__(self):
		if self.journal:
			return "%s, %s. %s. %s" % (self.author, self.title, self.journal, self.year)
		else:
			return "%s, %s (%s)" % (self.author, self.title, self.year)
	"""


	def keywords_escaped(self):
		return [(strip(keyword), urlquote_plus(strip(keyword)))
			for keyword in split(self.keywords, ',')]


	def authors_escaped(self):
		return [(author, replace(author.lower(), ' ', '+'))
			for author in self.authors_list]

	def authors_mla_escaped(self):
		self.authors = replace(self.authors, ',and ', ', and ')
		self.authors = replace(self.authors, ' and ', ', and ')
		mla_authors_list = [strip(author) for author in split(self.authors, ',')]
		sppos = mla_authors_list[0].find(' ',0)
		first_author_firstName =  mla_authors_list[0][0:sppos]
		first_author_lastName = mla_authors_list[0][sppos:]
		mla_authors_list[0] = "%s, %s" % (first_author_lastName, first_author_firstName)
		
		return [(author, replace(author.lower(), ' ', '+'))
			for author in mla_authors_list]

	def key(self):
		# this publication's first author
		author_lastname = self.authors_list[0].split(' ')[-1]

		publications = Publication.objects.filter(
			year=self.year,
			authors__icontains=author_lastname).order_by('month', 'id')

		# character to append to BibTex key
		char = ord('a')

		# augment character for every publication 'before' this publication
		for publication in publications:
			if publication == self:
				break
			if publication.authors_list[0].split(' ')[-1] == author_lastname:
				char += 1

		return self.authors_list[0].split(' ')[-1] + str(self.year) + chr(char)


	def month_bibtex(self):
		return self.MONTH_BIBTEX.get(self.month, '')

	def month_long(self):
		for month_int, month_str in self.MONTH_CHOICES:
			if month_int == self.month:
				return month_str
		return ''

	def first_author(self):
		first_author_name = self.authors_list[0]
		if len(self.authors_list) > 1:
			first_author_name = first_author_name + ', ' + self.authors_list[1] 
		return first_author_name

	def journal_or_book_title(self):
		if self.journal:
			return self.journal
		else:
			return self.book_title

	def clean(self):
		if not self.citekey:
			self.citekey = self.key()

	@staticmethod
	def simplify_name(name):
		name = name.lower()
		name = replace(name, u'ä', u'ae')
		name = replace(name, u'ö', u'oe')
		name = replace(name, u'ü', u'ue')
		name = replace(name, u'ß', u'ss')
		return name
