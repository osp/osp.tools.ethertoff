function remy(target) {          
    pattern = /(\b[A-Z].{0,2}|, .{0,3}) /g;
    text = target.html();          
    target.html(text.replace(pattern, '$1 ')); // I actually put a non-breaking space charcter after $1! You don’t see it, but it’s there. This is to not have this &nbsp; value pop up in places.
}    

$(document).ready(function() {

    // COUNT ITEMS
    words = $("#content").text().split(" ").length;
    $("dl.meta").append("<dt>Words</dt><dd><p>" + words + "</p></dd>");
    characters = $("#content").text().split("").length;
    $("dl.meta").append("<dt>Characters</dt><dd><p>" + characters + "</p></dd>");
    images = $("#content img").length;
    $("dl.meta").append("<dt>Images</dt><dd><p>" + images + "</p></dd>");

    // ORPHANS AND WIDOWS
    remy($("#content"));  

    // DIV WRAPPER AROUND EACH H2
    $("#content h2").each(function(){
        h2 = $(this).attr('id');
        $(this).nextUntil('h2').andSelf().wrapAll('<div class="slide ' + h2 + '"></div>');
    });

    // OFFSET ANCHOR BECAUSE OF FIXED MENU
    $('a.footnote-ref, a.footnote-backref').click(function(e){
        e.preventDefault();
        href = $(this).attr("href").replace("#", "");
        target = $("[id='" + href + "']");
        $(".target").removeClass("target");
        target.addClass("target");
        $("html, body").scrollTop(target.offset().top - 100);
      }
    );

// Django gives us elements like:
// <a id="include-example.html" class="include" href="/r/include-example.html">include-example.html</a>
// in which we include the relevant pages

var included = $("#content .include").length - 1;
$("#content .include").each(function(i, el) {
    var url = $(el).attr('href') + ' .middle';
    console.log("trying to load!");
    $(el).load(url,  function( responseText, textStatus, jqXHR ) {
        console.log('succesfully loaded ' + url);
        if (i == included){
            // DIV WRAPPER AROUND EACH H2
            $("#content h2").each(function(){
                h2 = $(this).attr('id');
                $(this).nextUntil('h2').wrapAll('<div class="' + h2 + '"></div>');
            });
        }
    });
});

});

// make external links open in new window
var isExternal = function(href) {
    /*
     * isExternal("http://i.liketightpants.net/")
     * true
     * isExternal("/publications/")
     * false
     * isExternal("http://www.f-u-t-u-r-e.org/publications/")
     * false
     * isExternal("http://localhost:8000/publications/")
     * false
     * isExternal("http://127.0.0.1:8000/publications/")
     * false
     */
    if (href.indexOf("http") === -1 || href.indexOf(document.location.host) !== -1 || href.indexOf("localhost") !== -1 || href.indexOf("127.0.0.1") !== -1 ) {
        return false;
    }
    return true;
};

$("a[href]").each(
    function() { 
        if (isExternal($(this).attr('href')) ) { 
            $(this).attr('target', '_blank');
        }
    }
);



$(".logged-out a.write-button").click(function(e) {
    e.preventDefault();
    $(".popup-wrapper").removeClass("hidden");
});

$(".slide-button").click(function(e) {
    e.preventDefault();
    $.getScript( "/static/js/slidy.js", function( data, textStatus, jqxhr ) {
      w3c_slidy.init();
      $("body").append("<link rel='stylesheet' href='/static/js/slidy.css/' type='text/css' media='all' />");
      $("body").append("<link rel='stylesheet' href='/css-slide/' type='text/css' media='all' />");
    });
});

$(".popup-wrapper").click(function(e) {
    $(this).addClass("hidden");
});

$(".popup").click(function(e) {
    e.stopPropagation();
});

$(document).keydown(function(e) {
    if (e.keyCode == 27) {
        $(".popup-wrapper").addClass("hidden");
    }
});

