function AnalyticsExtrasXBlock(runtime, xblock_element) {

    $('.button-previous').hide();
    $('.button-next').hide();
    $('.sequence-bottom').hide();
    $("#sequence-list li").each(function() {
        $(this).hide();
    });

    $(function ($) {


    });

    $( window ).unload(function() {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'session_end'),
            data: JSON.stringify({}),
            async: false
        });
    });

}
