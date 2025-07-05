/*
 * main.js | (c) @ajlkn | MIT licensed
 * Main initialization script for Prologue layout behavior
 */
(function($) {

  var $window = $(window),
      $body = $('body');

  // Breakpoints
  breakpoints({
    wide:    [ '1281px',  '1680px' ],
    normal:  [ '981px',   '1280px' ],
    narrow:  [ '737px',   '980px'  ],
    mobile:  [ null,      '736px'  ]
  });

  // Play initial animations on page load
  $window.on('load', function() {
    setTimeout(function() {
      $body.removeClass('is-preload');
    }, 100);
  });

  // Scrolly links
  $('.scrolly').scrolly();

})(jQuery);
