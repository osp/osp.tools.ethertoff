$(window).load(function(){
if($("body").hasClass("p-mode")){

    // Visualizes print css on screen
    $("style[media='print']").attr("media", "print, screen");
    $("link[media='print']").attr("media", "print, screen");

    // POLYFILL HACK: move metadata and footnotes outside of div#content
    footnotes = $(".footnote").detach();
    footnotes.insertAfter($("#content"));
    //metadata = $("#metadata").detach();
    //metadata.insertAfter($(".footnote"));

    // OVERRIDES PAGE FORMAT SET ON PAD
    try{
        var pageWidthCrop = parseInt(customPageWidth) + parseInt(crop);
        var pageHeightCrop = parseInt(customPageHeight) + parseInt(crop);
        var pageHeightCropx = pageHeightCrop - 1;
        var styles = "                                                  \
            @page {                                                     \n \
                size:" + pageWidthCrop + "mm " + pageHeightCrop + "mm;      \n \
            }                                                           \n \
            html,                                                       \n \
            body {                                                      \n \
                width: " + pageWidthCrop + "mm;                           \n \
            }                                                           \n \
            #master-page,                                               \n \
            .page,                                                      \n \
            div.print-marks {                                           \n \
                width: " + pageWidthCrop + "mm;                           \n \
                height: " + pageHeightCropx + "mm;                         \n \
            }                                                           \n \
        "

        // IF NO CROP MARKS
        if (crop == 0) {
            styles += " \
                .print-marks {                                          \n \
                    display: none;                                      \n \
                }                                                       \n \
                section.header {                                        \n \
                    top: 0;                                             \n \
                    left: 0;                                            \n \
                    right: 0;                                           \n \
                }                                                       \n \
                section.main-section {                                  \n \
                    top: 0;                                             \n \
                    left: 0;                                            \n \
                    bottom: 0;                                          \n \
                    right: 0;                                           \n \
                }                                                       \n \
                section.footer {                                        \n \
                    bottom: 0;                                          \n \
                    left: 0;                                            \n \
                    right: 0;                                           \n \
                }                                                       \n \
                #master-page,                                           \n \
                .page {                                                 \n \
                    outline-offset: 0;                                  \n \
                }                                                       \n \
            "
        }
        var style = document.createElement('style');
        document.body.appendChild(style);
        style.id = "publish-css";
        style.media = "screen, print";
        $("#publish-css").html(styles);
    } catch(e){}

    
    // Create pages
    $("body").append('<div id="pages"><section id="master-page" class="page"></section></div>');
    $("#master-page").append('\
            <div class="print-marks">\
                <div class="crop-top-left">\
                    <div class="crop-right" style="top: 0; right: 0;"></div>\
                    <div class="crop-bottom" style="bottom: 0cm; left: 0;"></div>\
                </div>\
                <div class="crop-top-right">\
                    <div class="crop-left" style="top: 0; left: 0;"></div>\
                    <div class="crop-bottom" style="bottom: 0; right: 0;"></div>\
                </div>\
                <div class="crop-bottom-right">\
                    <div class="crop-left" style="left: 0; bottom: 0;"></div>\
                    <div class="crop-top" style="right: 0cm; top: 0;"></div>\
                </div>\
                <div class="crop-bottom-left">\
                    <div class="crop-right" style="bottom: 0cm; right: 0;"></div>\
                    <div class="crop-top" style="left: 0cm; top: 0"></div>\
                </div>\
            </div>\
    ');

    $("#master-page").append('<section class="header" data-title="'+ $("h2[property='dc:title']").text() + '"></section>').append('<section class="main-section"><div class="column"></div></section>').append('<section class="footer"></section>');

    // OPTIONAL COLUMNS
    try {
        for (i = 1; i < columnNumber; i++){
            $(".main-section").append("<div class='column'></div>");
            $(".column").css("width", 100 / columnNumber + "%");
        }
    } catch(e){}


    height = $($(".middle")[0]).height() + $($(".middle")[1]).height();
    page_height = $("#master-page").height();

    // OPTIONAL CUSTOM PAGE NUMBER
    try {
        nb_page = customPageNumber;
    } catch(e) {
        nb_page = Math.ceil(height / page_height);
    }
    console.log("Content = " + height);
    console.log("page height = " + page_height);
    console.log("nb page = " + nb_page);
    for (i = 1; i <= nb_page; i++){
        $("#master-page").clone().addClass("page").attr("id","page-"+i).insertBefore($("#master-page"));
    }
    $("#master-page").hide();



    // __________________________________ DEBUG __________________________________ //
    $("button#debug").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("html").toggleClass("debug");
    });



    // __________________________________ SPREAD __________________________________ //
    $("button#spread").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("html").toggleClass("spread");
        w = parseInt($("html").css("width")) * 2;
        console.log(w);
        $("html").css("width",  w + "px");
    });


    // __________________________________ HIGH RESOLUTION __________________________________ //
    $("button#hi-res").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("html").toggleClass("export");
        $("img").each(function(){
            if ($("html").hasClass("export")){
                var lores = $(this).attr("src");
                hires = lores.split("/");
                hires.splice(-1, 0, "HD");
                hires = hires.join("/");
                $(this).attr("src", hires);
        console.log("Wait for hi-res images to load");
        window.setTimeout(function(){
            console.log("Check image resolution");
            // Redlights images too small for printing
            $("img").each(function(){
                if (Math.ceil(this.naturalHeight / $(this).height()) < 3) {
                    console.log($(this).attr("src") + ": " + Math.floor(this.naturalHeight / $(this).height()) );
                    if($(this).parent().hasClass("moveable")) {
                        $(this).parent().toggleClass("lo-res");
                    } else {
                        $(this).toggleClass("lo-res");
                    }
                }
            });
        }, 2000);
            } else {
                var hires = $(this).attr("src");
                lores = hires.split("/");
                lores.splice(-2, 1);
                lores = lores.join("/");
                $(this).attr("src", lores);
                $("img").removeClass("lo-res");
            }
        });
    });


    // __________________________________ TOC __________________________________ //
    $(".page:not(#master-page)").each(function(){
        page = $(this).attr("id");
        $("#toc-pages").append("<li><a href='#" + page + "'>" + page.replace("-", " ") + "</a></li>")
    });
    $("#goto").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("#toc-pages").toggle();
    });

    // __________________________________ ZOOM __________________________________ //
    $("#zoom").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("#zoom-list").toggle();
    });
    $("#zoom-list a").click(function(e){
        e.preventDefault();
        zoom = $(this).attr("title") / 100 ;
        console.log(zoom);
        $("#pages").css("-webkit-transform", "scale(" + zoom + ")");
        $("#pages").css("-webkit-transform-origin", "0 0");
    });

    // __________________________________ FOOTNOTES __________________________________ //
    setTimeout(function() {
        foot = 1;
        $("div.footnote").each(function(){
            ol = $("ol", $(this));
            console.log(foot);
            console.log(ol);
            height = ($(ol).height() / 3) * 2;
            $(ol).css("-webkit-flow-into", "footnotes-" + foot);
            $(this).append("<div style='height: " + height + "px; -webkit-flow-from: footnotes-" + foot + ";' class='footnote-column'></div><div style='height: " + height + "px; -webkit-flow-from: footnotes-" + foot + ";' class='footnote-column'></div>");
            foot += 1;
        });
    }, 3000);

}
});
