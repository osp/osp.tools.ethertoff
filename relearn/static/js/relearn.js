$(window).load(function() {
    h = $("div#content").height();
    $("iframe#ether").height(h);
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
