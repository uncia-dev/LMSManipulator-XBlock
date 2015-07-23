function AnalyticsExtrasXBlock(runtime, xblock_element) {

    var sequence_list = [];

    /*
    ajax request here to change the settings above
     */


    $('.button-previous').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase());
    $('.button-next').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase());
    $('.sequence-bottom').toggle("{{ self.hide_sequence_bottom }}".toLocaleLowerCase());
    $("#sequence-list li").each(function() {
        $(this).hide();
    });

    // Send the server a ping
    function ticks(freq) {

        setInterval(function() {
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'session_tick'),
                data: JSON.stringify({}),
                async: false
            });
        }, freq);

    }

    $(function ($) {
        ticks("{{ self.tick_period }}");
        console.log("test");
    });

    // Tell the server that this session is over
    $( window ).unload(function() {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'session_end'),
            data: JSON.stringify({}),
            async: false
        });
    });

}
