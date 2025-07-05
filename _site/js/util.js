/*
 * util.js | (c) @ajlkn | MIT licensed
 * Utility functions for scroll behavior and browser checks.
 */
(function() {
  var $ = jQuery;

  $.fn._scrollTo = function(target, options) {
    if (this.length == 0)
      return this;

    if (typeof target == 'string')
      target = $(target);

    if (target.length == 0)
      return this;

    if (!options)
      options = {};

    var x, y;

    x = (target.offset().left + target.outerWidth() / 2) - $(window).width() / 2;
    y = (target.offset().top + target.outerHeight() / 2) - $(window).height() / 2;

    if ('scroll' in this)
      this.scroll(x, y);
    else
      this.animate({ scrollTop: y }, typeof options.speed != 'undefined' ? options.speed : 1000);

    return this;
  };
})();
