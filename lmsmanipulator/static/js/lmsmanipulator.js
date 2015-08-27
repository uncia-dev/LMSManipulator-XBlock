function LMSManipulatorXBlock(runtime, xblock_element) {

    var location_id = ""; // url of this unit
    var course_tree = {}; // course tree JSON
    var unit_data = {}; // data of current unit

    // Set component visibilities depending on the Studio side settings
    $(".course-index").toggle("{{ self.hide_bar }}" == "False");
    $("#global-navigation").toggle("{{ self.hide_global_nav_bar }}" == "False");
    $(".course-material").toggle("{{ self.hide_course_material_bar }}" == "False");
    $(".sequence-nav").toggle("{{ self.hide_nav }}" == "False");
    $(".button-previous").toggle("{{ self.hide_nav_buttons }}" == "False");
    $(".button-next").toggle("{{ self.hide_nav_buttons }}" == "False");
    $(".course-index").toggle("{{ self.hide_sidebar }}" == "False");
    $(".sequence-bottom").toggle("{{ self.hide_sequence_bottom }}" == "False");
    $("div.wrapper.wrapper-footer").toggle("{{ self.hide_footer }}" == "False");
    $(".container-footer").toggle("{{ self.hide_footer }}" == "False");

    if ("{{ self.hide_sidebar }}" == "False" ) {

        $("<div class=\"lmx_sidebar\" role=\"navigation\"></div>").insertAfter(".course-index");
        $(".lmx_sidebar").css({
            "display": "table-cell",
            "width": "5px",
            "border-width": "1px",
            "background-color": "gray"
        }).hover(
            function() { $(this).css("background-color", "#0078B0");},
            function() { $(this).css("background-color", "gray"); }
        ).click(function() { $(".course-index").toggle(); });

    }

    /*
    Return unit data at specified chapter, subsection, unit indices.
    If all fields are blank, return current unit data.
    */
    function get_unit(chapter, subsection, unit){

        var unit_data = {};

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, "get_unit"),
            data: JSON.stringify({
                "chapter": (chapter === undefined) ? "" : chapter,
                "subsection": (subsection === undefined) ? "": chapter,
                "unit": (unit === undefined) ? "": unit
            }),
            success: function(result) {
                unit_data["name"] = (result.name == undefined) ? "" : result.name;
                unit_data["url"] = (result.name == undefined) ? "" : result.url;
                unit_data["required"] = (result.required == undefined) ? false : result.required;
                unit_data["enabled"] = (result.enabled == undefined) ? false : result.enabled;
                unit_data["visible"] = (result.visible == undefined) ? false : result.visible;
                unit_data["unlocks"] = (result.unlocks == undefined) ? [] : result.unlocks;
                unit_data["completed"] = (result.completed == undefined) ? false : result.completed;
                unit_data["chapter"] = (result.chapter == undefined) ? -1 : result.chapter;
                unit_data["subsection"] = (result.subsection == undefined) ? -1 : result.subsection;
                unit_data["unit"] = (result.unit == undefined) ? -1 : result.unit;
            },
            async: false
        });

        return unit_data;
    }

    /*
    Refresh the LMS chapter, subsection and unit buttons
    */
    function refresh_navigation() {

        // Update the course tree
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, "refresh_navigation"),
            data: JSON.stringify({}),
            success: function(result) {
                location_id = result.location_id;
                course_tree = result.course_tree;
            },
            async: false
        });

        // TODO: DELETE THESE
        console.log(location_id);
        console.log(course_tree);

        // Override the LMS navigation
        if (course_tree["name"] !== "") {

            unit_data = get_unit();

            // Override chapter and subsection sidebar
            $("#accordion nav div").each(function(idxc, chapter) {

                // Manipulate the chapters
                $(chapter).css({
                    "visibility": "hidden",
                    "pointer-events": "none",
                    "background-color": "lightgrey"
                });

                var curr_chapter = course_tree["chapter"][idxc];
                if (curr_chapter) $(chapter).css({
                    "visibility": curr_chapter["visible"] ? "visible" : "hidden",
                    "pointer-events": curr_chapter["enabled"] ? "auto" : "none",
                    "background-color": curr_chapter["enabled"] ?
                        (($(chapter).prop("class").indexOf("is-open") > -1) ? "white" : "lightgrey") : "grey"
                });

                // Manipulate the subsections of each chapter
                $(chapter).children("ul").children("li").each(function (idxs, subsection) {

                    $(subsection).css({
                        "visibility": "hidden",
                        "pointer-events": "none",
                        "background-color": "grey"
                    });

                    var curr_subsection = course_tree["chapter"][idxc]["subsection"][idxs];
                    if (curr_subsection) $(subsection).css({
                        "visibility": curr_subsection["visible"] ? "visible" : "hidden",
                        "pointer-events": curr_subsection["enabled"] ? "auto" : "none",
                        "background-color": curr_subsection["enabled"] ? "" : "grey"
                    });

                });

            });

            // Override subsection tabs (ie units)
            $("#sequence-list li a").each(function(idx, unit) {

                $(unit).css({
                    "visibility": "hidden",
                    "pointer-events": "none",
                    "background-color": "grey"
                });

                var loc = course_tree["indexof"][$(unit).attr("data-id").split("@")[2]];
                if (loc) {

                    var curr_unit = course_tree["chapter"][loc[0]]["subsection"][loc[1]]["unit"][loc[2]];
                    if (curr_unit) $(unit).css({
                        "visibility": curr_unit["visible"] ? "visible": "hidden",
                        "pointer-events": curr_unit["enabled"] ? "auto": "none",
                        "background-color": curr_unit["enabled"] ?
                            (($(unit).prop("class").indexOf(" active") > -1) ? "white" : "lightgrey") : "grey"
                   });

                }

            });

        }

    }

    /*
    Redirect to the unit at specified chapter, subsection, unit indices.
    */
    function goto_unit(chapter, subsection, unit) {

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(xblock_element, "goto_unit"),
            data: JSON.stringify({
                    "chapter": chapter.toString(),
                    "subsection": subsection.toString(),
                    "unit": unit.toString()
            }),
            success: function(result) {
                if (result.url) $(location).attr("href", result.url); // note, can get 404s if not careful
                if (result.tab) $("#tab_" + result.tab).click();
                if (result.error) console.log(result.error);
            },
            async: false
        });

    }

    // Extends the specified chapter accordion
    function extend_chapter(chapter) {
        $("#ui-accordion-accordion-header-" + chapter + " > a").click();
    }

    //
    $(".lmx_lmx_controls").click(function() {
       $(".lmx_controls").toggle();
    });

    // Toggle top navigation bar
    $(".lmx_nav_top_bar").click(function() {
        $(".sequence-nav").toggle();
        $(".button-previous").toggle();
        $(".button-next").toggle();
    });

    // Toggle top navigation bar buttons
    $(".lmx_nav_top_bar_buttons").click(function() {
        $(".button-previous").toggle();
        $(".button-next").toggle();
    });

    // Toggle bottom navigation bars
    $(".lmx_nav_bottom_bar").click(function() {
        $(".sequence-bottom").toggle();
    });

    // Toggle top most LMS bar
    $(".lmx_global_nav_bar").click(function() {
        $("#global-navigation").toggle();
    });

    // Toggle second top most LMS bar
    $(".lmx_course_material_bar").click(function() {
        $(".course-material").toggle();
    });

    // Toggle LMS footer
    $(".lmx_footer").click(function() {
        $("div.wrapper.wrapper-footer").toggle();
        $(".container-footer").toggle();
    });

    // For development
    $(".lmx_sidebar_dev").click(function() {
       $(".course-index").toggle();
    });

    // For development
    $(".lmx_sidebar_toggle").click(function() {
        $(".lmx_sidebar").toggle();
    });

    // For development
    $(".lmx_complete_unit").click(function() {

    });

    // Send the server the end of session message if using ComplexHTML
    function chx_session_end() {
        $(".chx_end_session").click();
    }

    $(".lmx_prev").click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $(".lmx_next").click(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    $("#sequence-list > li > a").click(function() {
       chx_session_end(); // only works if using ComplexHTML
    });

    $( window ).unload(function() {
        chx_session_end(); // only works if using ComplexHTML
    });

    function clearUnit() {

        $(".lmx_error").show();
        for (var i=0; i < $(".vert-mod > div").length; i++)
            if ($(("#seq_content > div > div > div.vert.vert-" + i)).attr("data-id").indexOf("lmsmanipulator+block") == -1)
                $((".vert-" + i)).empty();

    }

    $(function ($) {

        refresh_navigation();
        if (unit_data["visible"] === false || unit_data["enabled"] === false) clearUnit();
        if (unit_data["completed"] === true) $(".lmx_completed").show();

    });

}