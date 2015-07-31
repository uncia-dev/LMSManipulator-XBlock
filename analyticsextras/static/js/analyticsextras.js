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

    $('.button-previous').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $('.button-next').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $(".sequence-list-wrapper").toggle("{{ self.hide_nav }}".toLocaleLowerCase() === "false");
    $('.sequence-bottom').toggle("{{ self.hide_sequence_bottom }}".toLocaleLowerCase() === "false");
    $('.course-index').toggle("{{ self.hide_sidebar }}".toLocaleLowerCase() === "false");

/*
    // Populate tabs bar, hide some of the tabs
    $("#sequence-list li").each(function() {
        $(this).hide();
        // add end() event for each click ??
    });
*/

    // Send the server the end of session message if using ComplexHTML
    function chx_session_end() {
        $('.chx_end_session').click();
    }

    // Tell the server that this session is over
    $('.aex_prev').click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $('.aex_next').click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $('.aex_sidebar').click(function() {
        $('.course-index').toggle()
    });

    $( window ).unload(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $(function ($) {

    });

}