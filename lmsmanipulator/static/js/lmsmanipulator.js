function LMSManipulatorXBlock(runtime, xblock_element) {

    var sequence_list = [];

    // Initialize this XBlock via an AJAX request
    $.ajax({
        type: "POST",
        url: runtime.handlerUrl(xblock_element, 'lmx_init'),
        data: JSON.stringify({}),
        success: function(result) {

        },
        async: false
    });

    $('.button-previous').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $('.button-next').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $(".sequence-list-wrapper").toggle("{{ self.hide_nav }}".toLocaleLowerCase() === "false");
    $('.sequence-bottom').toggle("{{ self.hide_sequence_bottom }}".toLocaleLowerCase() === "false");
    $('.course-index').toggle("{{ self.hide_sidebar }}".toLocaleLowerCase() === "false");

    // Refresh LMS top navigation bar sequence
    function refresh_sequence() {

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'refresh_sequence'),
            data: JSON.stringify({}),
            success: function(result) {

                console.log("csv reading here...");

            },
            async: false
        });

    }

    /* URL to unit

    course_url + jump_to/block-v1:edX+DemoX+Demo_Course+type@vertical+block@ + unit_id
     */


    /* Accessing specific chapter and unit

    $("#ui-accordion-accordion-panel-0 > li").eq(0).find("a")[0].click()
    $("tab_0").click()

     */

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
    $('.lmx_prev').click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $('.lmx_next').click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $('.lmx_sidebar').click(function() {
        $('.course-index').toggle()
    });

    $( window ).unload(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $(function ($) {

        refresh_sequence();

    });

}