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
                course_tree['current_unit'] = result.current_unit;
            },
            async: false
        });

    }

    /*
    Redirect to unit at specified indices.
     */
    function redirect(chapter, subsection, unit) {

        // won't work for now. will check for current location
        // check to see if student already in chapter and subsection specified in parameters
        if (chapter === undefined || subsection === undefined) {

            // Just changing a tab, no need to redirect as it changes the page
            console.log("Implement me!");
            // switch tab via JQuery click

            /* Accessing specific chapter and unit

            $("#ui-accordion-accordion-panel-0 > li").eq(0).find("a")[0].click()
            $("tab_0").click()

             */

        // Unit is located in another subsection; need to generate a URL
        } else {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'redirect'),
                data: JSON.stringify(
                    {
                        "chapter": chapter.toString(),
                        "subsection": subsection.toString(),
                        "unit": unit.toString()
                    }
                ),
                success: function(result) {

                    console.log(result);
                    // do redirect here via JS
                    // TODO: Implement redirect function

                },
                async: false
            });

        }

    }

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
        redirect(3,1,1);

    });

}