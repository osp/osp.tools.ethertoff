$(window).load(function() {
    h = $("div#content").height();
    $("iframe#ether").height(h);

    // COUNT WORDS
    words = $("#content").text().split(" ").length;
    $("dl.meta").append("<dt>Words</dt><dd><p>" + words + "</p></dd>");
    characters = $("#content").text().split("").length;
    $("dl.meta").append("<dt>Characters</dt><dd><p>" + characters + "</p></dd>");

    // PRINT PREVIEW
    $("#print-preview").click(function(){
        if(! $("html").hasClass("print-preview")){
            $("html").addClass("print-preview");
            $("style[media='print']").attr("media", "print, screen");
            $("body").append("<section id='master-page' class='page'></section>");
            nb_page = Math.floor($("#content").height() / $("#master-page").height());
            for (i = 1; i <= nb_page; i++){
                $("#master-page").clone().attr("id","page-"+i).insertAfter($("#master-page"));
            }
            $("#content").css("-webkit-flow-into", "myFlow");
        } else {
            $(html).removeClass("print-preview");
            $("style[media='print, screen']").attr("media", "print");
        }
    });
});

// just for testing:
var pads = ["2013::debrief", "2013::general-publication", "2013::introducing-by-couple", "2013::introduction-script", "2013::schedule", "cheat-sheet::git-and-the-command-line", "cheat-sheet::how-to-install-free-software", "cheat-sheet::tex", "cheat-sheet::tracing", "cheat-sheet::using-the-plotter", "cover", "css", "images", "notes::copyright-licenses", "notes::merging", "pedagogy::learning-situations", "pedagogy::references", "relearn::about", "relearn::contact", "relearn::repositories", "relearn::start", "relearn::utrecht", "relearn::welcome", "worksessions::can-it-scale-to-the-universe::introduction", "worksessions::can-it-scale-to-the-universe::notes", "worksessions::gesturing-paths::introduction", "worksessions::gesturing-paths::notes", "worksessions::off-grid::introduction", "worksessions::off-grid::notes", "worksessions::off-grid::xtreme-pattern-methods"];


var navigation = function(padLinks) {

    var setupPads = function(padLinks) {
        return _.map(padLinks, function(padLink) {
            // "/r/cooking-with-epub".replace(/\/[^\/]+\//, '') -> "cooking-with-epub"
            var slug = padLink.replace(/\/[^\/]+\//, '');
            return {
                name : slug,
                slug : slug,
                href : padLink,
                namespaces : slug.split('::')
            };
        });
    };

    var obj = {
        pads : setupPads(padLinks),
        sections : {}
    };

    var unpackPads = function(obj) {
        obj.pads = _.uniq(_.compact(_.map(obj.pads, function(pad) {
            if (pad.namespaces.length > 1) {
                if ( typeof obj.sections[pad.namespaces[0]] === 'undefined') {
                    obj.sections[pad.namespaces[0]] = {
                        pads : [],
                        sections : {}
                    };
                }
                obj.sections[pad.namespaces[0]].pads.push({
                    name : pad.name,
                    slug : pad.slug,
                    href : pad.href,
                    namespaces : pad.namespaces.splice(1)
                });
                return null;
            } else {
                return {
                    name : pad.namespaces[0],
                    slug : pad.slug,
                    href : pad.href
                };
            }
        })), true);

        _.each(obj.sections, function(section) {
            unpackPads(section);
        });
        return obj;
    };

    return unpackPads(obj);
};

var padLinks = _.map($('#pads_list li a'), function(padLink) {
    return padLink.getAttribute('data-uid');
});

var renderSection = function(section) {
    var lis = [];
    var lis = lis.concat(_.map(_.keys(section.sections), function(sectionKey) {
        return '<li><a class="namespace">' + sectionKey + ' →</a>' + renderSection(section.sections[sectionKey]) + '</li>';
    }));
    var lis = lis.concat(_.map(section.pads, function(pad) {
        return '<li><a href="/r/' + encodeURIComponent(pad.href) + '">' + pad.name + '</a></li>';
    }));
    return '<ul>' + lis.join('') + '</ul>';
};


var padsList = $(renderSection(navigation(padLinks)));
$("#pads_list").html( padsList.html() );

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

// Django gives us elements like:
// <a id="include-example.html" class="include" href="/r/include-example.html">include-example.html</a>
// in which we include the relevant pages

$("#content .include").each(function(i, el) {
    $(el).load($(el).attr('href') + ' .middle');
});

$(".logged-out a.write-button").click(function(e) {
    e.preventDefault();
    $(".popup-wrapper").removeClass("hidden");
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
