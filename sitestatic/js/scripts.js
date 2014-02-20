django.jQuery(document).ready(function() {
    if (django.jQuery('#nameparts-group').length) {
        var first_group = django.jQuery('#nameparts-group').parent().children().eq(0);
        django.jQuery('#nameparts-group').insertBefore(first_group);
    }
    
    if (django.jQuery('#workrecordcreator_set-group').length) {
        var first_group = django.jQuery('#workrecordcreator_set-group').parent().children().eq(0);
        django.jQuery('#workrecordcreator_set-group').insertAfter(first_group);
    }
    
    if (django.jQuery('#id_bib_type').length) {
        formrows = django.jQuery('.form-row');
        bookrows = django.jQuery('.bib_type, .title, .booktitle, .author, .editor, .volume, .series, .chapter, .edition, .year, .pages, .publisher, .address, .work_record');
        journalrows = django.jQuery('.bib_type, .title, .journal, .author, .editor, .volume, .number, .month, .year, .pages, .publisher, .work_record');
        bibtype = django.jQuery('#id_bib_type');
        
        
        bibtype.change(function() {
            if (bibtype.val() == 'book') {
                formrows.slideUp();
                bookrows.slideDown();
            }
            else if (bibtype.val() == 'journ') {
                formrows.slideUp();
                journalrows.slideDown();
            }
            else {
                formrows.slideDown();
            }
        });
    }
    
});