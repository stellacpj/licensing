/*<*******************

Copyright 2017 Juniper Networks, Inc. All rights reserved.
Licensed under the Juniper Networks Script Software License (the "License").
You may not use this script file except in compliance with the License, which is located at
http://www.juniper.net/support/legal/scriptlicense/
Unless required by applicable law or otherwise agreed to in writing by the parties, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

*******************>*/
(function($, undefined) {
  $.web2py.ajax_fields = function(target) {
    /*
     *this attaches something to a newly loaded fragment/page
     * Ideally all events should be bound to the document, so we can avoid calling
     * this over and over... all will be bound to the document
     */
    /*adds btn class to buttons*/
    $('button:not([class^="btn"])', target).addClass('btn btn-default');
    $("p.w2p-autocomplete-widget input").addClass('form-control');
    $('form input[type="submit"]:not([class^="btn"]), form input[type="button"]:not([class^="btn"])', target).addClass('btn btn-default');
    /* javascript for PasswordWidget*/
    $('input[type=password][data-w2p_entropy]', target).each(function() {
      web2py.validate_entropy($(this));
    });
    /* javascript for ListWidget*/
    $('ul.w2p_list', target).each(function() {
      function pe(ul, e) {
        var new_line = ml(ul);
        rel(ul);
        if ($(e.target).closest('li').is(':visible')) {
          /* make sure we didn't delete the element before we insert after */
          new_line.insertAfter($(e.target).closest('li'));
        } else {
          /* the line we clicked on was deleted, just add to end of list */
          new_line.appendTo(ul);
        }
        new_line.find(":text").focus();
        return false;
      }

      function rl(ul, e) {
        if ($(ul).find('li').length > 1) {
          /* only remove if we have more than 1 item so the list is never empty */
          $(e.target).closest('li').remove();
        }
      }

      function ml(ul) {
        /* clone the first field */
        var line = $(ul).find("li:first").clone(true);
        line.find(':text').val('');
        return line;
      }

      function rel(ul) {
        /* keep only as many as needed*/
        $(ul).find("li").each(function() {
          var trimmed = $.trim($(this).find(":text").val());
          if (trimmed == '') $(this).remove();
          else $(this).find(":text").val(trimmed);
        });
      }
      var ul = this;
      $(ul).find(":text").addClass('form-control').wrap("<div class='input-group'></div>").after('<div class="input-group-addon"><i class="glyphicon glyphicon-plus"></i></div><div class="input-group-addon"><i class="glyphicon glyphicon-minus"></i></div>').keypress(function(e) {
        return (e.which == 13) ? pe(ul, e) : true;
      }).next().click(function(e) {
        pe(ul, e);
        e.preventDefault();
      }).next().click(function(e) {
        rl(ul, e);
        e.preventDefault();
      });
    });
  }

  $(function() {
    $(".nav ul.dropdown-menu").each(function() {
      var toggle = jQuery(this).parent();
      if (toggle.parent().hasClass("nav")) {
        toggle.attr("data-w2pmenulevel", "l0");
        toggle.children("a")
          .addClass("dropdown-toggle")
          .append('<span class="caret"> </span>')
          .attr("data-toggle", "dropdown");
      } else {
        toggle.addClass("dropdown-submenu").removeClass("dropdown");
      };
    });
  });

})(jQuery);