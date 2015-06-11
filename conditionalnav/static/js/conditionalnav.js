function ConditionalNavigatorXBlock(runtime, element) {

    $(function ($) {

        $('.button-previous').hide();
        $('.button-next').hide();
        $('.sequence-bottom').hide();
        $("#sequence-list li").each(function() {
            $(this).hide();
        })

    });
}
