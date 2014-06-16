(function($) {
    /**
     * function jQuery.fn.comments (options)
     *
     * Takes a jquery collection and finds recursively all the comment nodes.
     * Returns an array of all the found comment nodes.
     *    
     *    >>> $('body').comments();
     */

    $.fn.comments = function (options) {
        var opts = $.extend({}, $.fn.comments.defaults, options);

        var comments = new Array();

        /*
         * Adapted from
         * http://stackoverflow.com/questions/2912710/getelementsbytagname-does-not-return-comment-nodes-in-javascript/2912981#2912981
         */

        function traverseDom(curr_element) { // this is the recursive function
            var comments = new Array();
            // base case: node is a comment node
            if (curr_element.nodeName == "#comment" || curr_element.nodeType == 8) {
                // You need this OR because some browsers won't support either nodType or nodeName... I think...
                comments[comments.length] = curr_element;
            }
            // recursive case: node is not a comment node
            else if(curr_element.childNodes.length > 0) {
                for (var i = 0; i < curr_element.childNodes.length; i++) {
                    // adventures with recursion!
                    comments = comments.concat(traverseDom(curr_element.childNodes[i]));
                }
            }
            return comments;
        }

        $(this).each(function() {
            comments = comments.concat(traverseDom(this));
        });
        
        return comments;
    };

    $.fn.comments.defaults = {};


    /**
     * function jQuery.fn.revealComments (options)
     *
     * Takes a jquery collection and makes visible its comment nodes.
     * Returns the original jquery collection.
     *    
     *    >>> $('body').revealComments();
     */

    $.fn.revealComments = function (options) {
        var opts = $.extend({}, $.fn.revealComments.defaults, options);

        var comments = $(this).comments();

        $.each(comments, function(index, comment) {
            var newNode = $('<span>').addClass('comment').attr('title', comment.data).get(0);
            comment.parentNode.replaceChild(newNode, comment);
        });

        return $(this);
    };

    $.fn.revealComments.defaults = {};
})(jQuery);
