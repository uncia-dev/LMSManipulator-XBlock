function LMSManipulatorXBlock(runtime, xblock_element) {

    var course_tree = {};

    $('.button-previous').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $('.button-next').toggle("{{ self.hide_nav_buttons }}".toLocaleLowerCase() === "false");
    $(".sequence-list-wrapper").toggle("{{ self.hide_nav }}".toLocaleLowerCase() === "false");
    $('.sequence-bottom').toggle("{{ self.hide_sequence_bottom }}".toLocaleLowerCase() === "false");
    $('.course-index').toggle("{{ self.hide_sidebar }}".toLocaleLowerCase() === "false");

    // Refresh LMS top navigation bar sequence
    function refresh_navigation() {

        /*
            // Populate tabs bar, hide some of the tabs
            $("#sequence-list li").each(function() {
                $(this).hide();
                // add end() event for each click ??
            });
        */

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'refresh_navigation'),
            data: JSON.stringify({}),
            success: function(result) {
                course_tree['name'] = result.name;
                course_tree['chapter'] = result.chapter;
            },
            async: false
        });

    }

    /*
    Redirect to unit at specified indices.
     */
    function goto_unit(chapter, subsection, unit) {

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, 'goto_unit'),
            data: JSON.stringify(
                {
                    "chapter": chapter.toString(),
                    "subsection": subsection.toString(),
                    "unit": unit.toString()
                }
            ),
            success: function(result) {

                if (result.url) $(location).attr("href", result.url); // note, can get 404s if not careful
                if (result.tab) $("#tab_" + result.tab).click();
                if (result.error) console.log(result.error);
            },
            async: false
        });

    }

    /*
    Extends the specified chapter accordion
     */
    function extend_chapter(chapter) {
        $("#ui-accordion-accordion-header-" + chapter + " > a").click();
    }

    // Send the server the end of session message if using ComplexHTML
    function chx_session_end() {
        $('.chx_end_session').click();
    }

    // Tell the server that this session is over
    $('.lmx_prev').click(function() {
        chx_session_end(); // only works if using ComplexHTML
        goto_unit(0,0,0);
    });

    $('.lmx_next').click(function() {
        chx_session_end(); // only works if using ComplexHTML
        goto_unit(3,1,0);
    });

    $('.lmx_sidebar').click(function() {
        $('.course-index').toggle()
    });

    $('.lmx_nav_top_bar').click(function() {
        $('.sequence-nav').toggle()
    });

    $('.lmx_nav_bottom_bar').click(function() {
        $('.sequence-bottom').toggle()
    });

    $('.lmx_course_material_bar').click(function() {
        $('.course-material').toggle()
    });

    $('.lmx_global_nav_bar').click(function() {
        $('#global-navigation').toggle()
    });

    $('.lmx_footer').click(function() {
        $('div.wrapper.wrapper-footer').toggle()
    });

    $( window ).unload(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $(function ($) {

        refresh_navigation();
        console.log(course_tree);

    });

}