$(document).ready(function() {
  $('#setlang-en').click(function(e) {
      e.preventDefault();
      $('#langselect select').val('en');
      $('#langselect form').submit();
      return false;
  });

  $('#setlang-es').click(function(e) {
      e.preventDefault();
      $('#langselect select').val('es');
      $('#langselect form').submit();
      return false;
  });

  $('#wrapper').css('min-height', window.innerHeight - 50);

  $('#archivenav li:eq(4)').hover(function() {
      $(this).children('ul').slideDown('slow');
    }, function() {
      $(this).children('ul').slideUp('slow');
  });

  if ($('#digitalobjects').length) {
      $('#digitalobjects').cycle({
        timeout: 8000,
        height: 240,
        width: 210,
        next: '#next',
        prev: '#prev',
        after: function() {
          $('#caption').attr("href", $(this).children('img').attr('data-href'));
        }
      });
  }

  $('.linkeditems ul, .linkeditems div').slideUp(0);
  $('.linkeditems h3').click(function() {
      $(this).siblings('ul, div').slideToggle(1200);
  });

});

