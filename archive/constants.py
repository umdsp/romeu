from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
	(u'M', _(u'Male')),
	(u'F', _(u'Female')),
	(u'O', _(u'Other')),
	(u'N', _(u'Not applicable')),
)

DATE_PRECISION_CHOICES = (
	(u'f', _(u'Full date')),
	(u'm', _(u'Month')),
	(u'y', _(u'Year')),
	(u'd', _(u'Decade')),
	(u'e', _(u'Era')),
	(u'c', _(u'Century')),
    (u'n', _(u'Month and day (no year)')),
    (u'b', _(u'Month, day, and decade')),
)

NAME_PART_CHOICES = (
	(u'prefix', _(u'Prefix')),
	(u'given', _(u'Given name')),
	(u'middle', _(u'Middle name')),
	(u'family', _(u'Family name')),
	(u'suffix', _(u'Suffix')),
	(u'orgname', _(u'Organization name')),
)

CREATOR_TYPE_CHOICES = (
	(u'person', _(u'Personal name')),
	(u'family', _(u'Family name')),
	(u'corp', _(u'Corporate name')),
)

CREATOR_RELATIONSHIP_TYPES = (
	(u'member', _(u'Member of')),
	(u'family', _(u'Related to')),
	(u'ident', _(u'Identical to')),
)

BIB_TYPE_CHOICES = (
	(u'book', _(u'Book')),
	(u'journ', _(u'Journal article')),
	(u'other', _(u'Other')),
)

SPECIAL_PERFORMANCE_CHOICES = (
	(u'reading', _(u'Reading')),
	(u'stageread', _(u'Staged reading')),
	(u'workshop', _(u'Workshop')),
	(u'perfart', _(u'Performance art')),
	(u'collab', _(u'Collaboration')),
	(u'online', _(u'Online performance')),
	(u'onlinecollab', _(u'Online collaboration')),
)

SUBJECT_TYPE_CHOICES = (
	(u'corpname', _(u'Corporate Name')),
	(u'date', _(u'Date')),
	(u'famname', _(u'Family Name')),
	(u'function', _(u'Function')),
	(u'genre', _(u'Genre/Form of Material')),
	(u'geoname', _(u'Geographic Name')),
	(u'occupation', _(u'Occupation')),
	(u'persname', _(u'Personal Name')),
	(u'title', _(u'Title')),
	(u'topic', _(u'Topical Term')),
)

RELATIONSHIP_TYPE_CHOICES = (
	(u'part', _(u'is part of')),
	(u'trans', _(u'is a translation of')),
	(u'adapt', _(u'is an adaptation of')),
	(u'vers', _(u'is a version of')),
	(u'refer', _(u'is referenced by')),
	(u'like', _(u'is similar to')),
	(u'after', _(u'follows after')),
)

PREMIER_CHOICES = (
	(u'w', _(u'World')),
	(u'u', _(u'US')),
	(u'c', _(u'Cuba')),
	(u'f', _(u'Florida')),
	(u'o', _(u'Other')),
)

AWARD_RESULT_CHOICES = (
	(u'w', _(u'Winner')),
	(u'n', _(u'Nominee')),
	(u'h', _(u'Honorable mention')),
	(u'o', _(u'Other')),
)
