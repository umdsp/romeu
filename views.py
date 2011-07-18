from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

from datatrans import utils
from datatrans.models import KeyValue

def _get_model_slug(model):
        ct = ContentType.objects.get_for_model(model)
        return u'%s.%s' % (ct.app_label, ct.model)

def _get_model_entry(slug):
    app_label, model_slug = slug.split('.')
    ct = ContentType.objects.get(app_label=app_label, model=model_slug)
    model_class = ct.model_class()
    registry = utils.get_registry()
    if not model_class in registry:
        raise Http404(u'No registered model found for given query.')
    return model_class

def _get_model_stats(model, filter=lambda x: x):
    default_lang = utils.get_default_language()
    registry = utils.get_registry()
    keyvalues = filter(KeyValue.objects.for_model(model, registry[model].values()).exclude(language=default_lang))
    total = keyvalues.count()
    done = keyvalues.filter(edited=True, fuzzy=False).count()
    return (done * 100 / total if total > 0 else 0, done, total)

@staff_member_required
def model_list(request):
    '''
    Shows an overview of models to translate, along with the fields, languages and progress information.
    The context structure is defined as follows:

    context = {'models': [{'languages': [('nl', 'NL', (<percent_done>, <todo>, <total>)), ('fr', 'FR', (<percent_done>, <todo>, <total>))],
                           'field_names': [u'description'],
                           'stats': (75, 15, 20),
                           'slug': u'flags_app.flag',
                           'model_name': u'flag'}]}
    '''
    registry = utils.get_registry()

    default_lang = utils.get_default_language()
    languages = [l for l in settings.LANGUAGES if l[0] != default_lang]

    models = [{'slug': _get_model_slug(model),
               'model_name': u'%s' % model._meta.verbose_name,
               'field_names': [u'%s' % f.verbose_name for f in registry[model].values()],
               'stats': _get_model_stats(model),
               'languages': [(l[0], l[1], _get_model_stats(model, filter=lambda x: x.filter(language=l[0]))) for l in languages],
               } for model in registry]


    context = {'models': models}

    return render_to_response('datatrans/model_list.html', context, context_instance=RequestContext(request))

@staff_member_required
def model_detail(request, slug, language):
    '''
    The context structure is defined as follows:

    context = {'model': '<name of model>',
               'fields': {'name': '<name of field>',
                          'items': [{'original': '<KeyValue object with original value>',
                                     'translations': [<KeyValue objects with translation>]}]
                         }
              }
    '''

    if request.method == 'POST':
        translations = [(KeyValue.objects.get(pk=int(k.split('_')[1])), v) for k, v in request.POST.items() if 'translation_' in k]
        section = [k for k, v in request.POST.items() if 'section_' in k]
        section = '#%s' % section[0] if len(section) > 0 else ''
        for keyvalue, translation in translations:
            empty = 'empty_%d' % keyvalue.pk in request.POST
            ignore = 'ignore_%d' % keyvalue.pk in request.POST
            if translation != '' or empty or ignore:
                if keyvalue.value != translation:
                    if not ignore:
                        keyvalue.value = translation
                    keyvalue.fuzzy = False
                if ignore:
                    keyvalue.fuzzy = False
                keyvalue.edited = True
                keyvalue.save()
        return HttpResponseRedirect(reverse('datatrans_model_detail', args=(slug, language)) + section)

    model = _get_model_entry(slug)
    registry = utils.get_registry()
    fields = registry[model]

    default_lang = utils.get_default_language()
    model_name = u'%s' % model._meta.verbose_name

    field_list = []
    first_unedited_translation = None
    for field in fields.values():
        items = []
        objects = model.objects.values(field.name).distinct().all().order_by(field.name)
        for object in objects:
            key = object[field.name]
            original = KeyValue.objects.get_keyvalue(key, default_lang)
            translation = KeyValue.objects.get_keyvalue(key, language)
            if first_unedited_translation is None and (not translation.edited or translation.fuzzy):
                first_unedited_translation = translation
            items.append({'original': original, 'translation': translation})
        field_list.append({'name': field.name, 'verbose_name': unicode(field.verbose_name), 'items': items})


    context = {'model': model_name,
               'fields': field_list,
               'original_language': default_lang,
               'other_language': language,
               'progress': _get_model_stats(model, lambda x: x.filter(language=language)),
               'first_unedited': first_unedited_translation}


    return render_to_response('datatrans/model_detail.html', context, context_instance=RequestContext(request))

@staff_member_required
def make_messages(request):
    utils.make_messages()
    return HttpResponseRedirect(reverse('datatrans_model_list'))

@staff_member_required
def obsolete_list(request):
    from django.db.models import Q

    default_lang = utils.get_default_language()
    all_obsoletes = utils.find_obsoletes().order_by('digest')
    obsoletes = all_obsoletes.filter(Q(edited=True) | Q(language=default_lang))

    if request.method == 'POST':
        all_obsoletes.delete()
        return HttpResponseRedirect(reverse('datatrans_obsolete_list'))

    context = {'obsoletes': obsoletes}
    return render_to_response('datatrans/obsolete_list.html', context, context_instance=RequestContext(request))
