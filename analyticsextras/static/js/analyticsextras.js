function AnalyticsExtrasXBlock(runtime, xblock_element) {

    var sequence_list = [];


    // Initialize this XBlock via an AJAX request
    $.ajax({
        type: "POST",
        url: runtime.handlerUrl(xblock_element, 'aex_init'),
        data: JSON.stringify({}),
        success: function(result) {
            console.log("make me work!");
        },
        async: false
    });


    $('.button-previous').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase());
    $('.button-next').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase());
    $('.sequence-bottom').toggle("{{ self.hide_sequence_bottom }}".toLocaleLowerCase());

    // Populate tabs bar, hide some of the tabs
    $("#sequence-list li").each(function() {
        $(this).hide();
        // add end() event for each click ??
    });

    // Send the server a ping
    function session_ticks(freq) {

        setInterval(function() {
            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'session_tick'),
                data: JSON.stringify({}),
                async: false
            });
        }, freq);

    }

    // Send the server the end of session message
    function session_end() {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'session_end'),
            data: JSON.stringify({}),
            async: false
        });
    }

    $(function ($) {
        
        // Periodically tell the server that the student is still viewing this slide
        session_ticks("{{ self.tick_interval }}");

        // Tell the server that this session is over
        $('.aex_prev').click(function() { session_end(); });
        $('.aex_next').click(function() { session_end(); });

    });

    // Tell the server that this session is over
    $( window ).unload(function() { session_end(); });

}