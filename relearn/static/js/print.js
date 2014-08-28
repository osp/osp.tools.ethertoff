$(window).load(function(){

if($("body").hasClass("logged-in")) {
    $("style"[attr="publish"]).remove();
}


if($("body").hasClass("print-mode")){

    // Visualizes print css on screen
    $("style[media='print']").attr("media", "print, screen");
    $("link[media='print']").attr("media", "print, screen");

    // Create pages
    $("body").append('<section id="master-page" class="page"></section>');
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

    $("#master-page").append('<section class="header"></section>').append('<section class="main-section"></section>').append('<section class="footer"></section>');

    height = $($(".middle")[0]).height() + $($(".middle")[1]).height();
    page_height = $("#master-page").height();
    nb_page = Math.ceil(height / page_height);
    console.log("Content = " + height);
    console.log("page height = " + page_height);
    console.log("nb page = " + nb_page);
    //if (nb_page == 0) { nb_page = 1}
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


    // __________________________________ HIGH RESOLUTION __________________________________ //
    $("button#hi-res").click(function(e){
        e.preventDefault();
        $(this).toggleClass("button-active");
        $("html").toggleClass("export");
        $("img").each(function(){
            var hires = $(this).attr("data-alt-src");
            var lores = $(this).attr("src");
            $(this).attr("data-alt-src", lores)
            $(this).attr("src", hires)
        });
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




}
});
