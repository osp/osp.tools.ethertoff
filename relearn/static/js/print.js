//$(".page").css("height", "auto");

//// PRINT PREVIEW
$("#print-preview").click(function(){
    $("body").addClass("print-mode");
    $("style[media='print']").attr("media", "print, screen");
    $("link[media='print']").attr("media", "print, screen");

    $("body").append('<section id="master-page" class="page"></section>');

    height = $($(".middle")[0]).height() + $($(".middle")[1]).height();
    page_height = $("#master-page").height();
    nb_page = Math.ceil(height / page_height);
    console.log("Content = " + height);
    console.log("page height = " + page_height);
    console.log("nb page = " + nb_page);
    //if (nb_page == 0) { nb_page = 1}
    for (i = 1; i <= nb_page; i++){
        $("#master-page").clone().addClass("page").attr("id","page-"+i).insertAfter($("#master-page"));
    }
    $("#master-page").hide();




    //    if(! $("html").hasClass("print-mode")){
    //$(".page").height(page_height);
    //CSSRegions.doLayout();
    //        $("html").addClass("print-preview");
    //        $("style[media='print']").attr("media", "print, screen");
    //        $("link[media='print']").attr("media", "print, screen");
    //    } else {
    //        $(html).removeClass("print-preview");
    //        $("style[media='print, screen']").attr("media", "print");
    //        $("link[media='print, screen']").attr("media", "print");
    //    }
});

