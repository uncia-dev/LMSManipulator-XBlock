function LMSManipulatorXBlockStudio(runtime, xblock_element) {

    $('.lmx_location_id').val($(".unit-id-value").text());

    if ($('.lmx_hide_sidebar').prop('checked'))
        $('.lmx_toggle_sidebar').prop('disabled', true).prop('checked', false);

    $(function ($) {

        // Add Save Button
        $('ul', '.modal-actions')
            .append(
                $('<li>', {class: "action-item"}).append(
                    $('<a />', {class: "action-primary", id: "lmx_submit", text: "Save"})
                )
            );


        $('.lmx_hide_sidebar').click(function(eventObject) {

            if ($('.lmx_hide_sidebar').prop('checked'))
                $('.lmx_toggle_sidebar').prop('disabled', true).prop('checked', false);
            else
                $('.lmx_toggle_sidebar').prop('disabled', false);

        });

        $('#lmx_submit').click(function(eventObject) {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'studio_save'),
                data: JSON.stringify({
                    "display_name": $('.lmx_display_name').val(),
                    "hide_global_nav_bar": $('.lmx_hide_global_nav_bar').prop('checked') ? 1 : 0,
                    "hide_course_material_bar": $('.lmx_hide_course_material_bar').prop('checked') ? 1 : 0,
                    "hide_nav_buttons": $('.lmx_hide_nav_buttons').prop('checked') ? 1 : 0,
                    "hide_nav": $('.lmx_hide_nav').prop('checked') ? 1 : 0,
                    "hide_sequence_bottom": $('.lmx_hide_sequence_bottom').prop('checked') ? 1 : 0,
                    "hide_sidebar": $('.lmx_hide_sidebar').prop('checked') ? 1 : 0,
                    "toggle_sidebar": $('.lmx_toggle_sidebar').prop('checked') ? 1 : 0,
                    "hide_footer": $('.lmx_hide_footer').prop('checked') ? 1 : 0,
                    "course_url": $('.lmx_course_url').val(),
                    "location_id": $('.lmx_location_id').val(),
                    "csv_url": $('.lmx_csv_url').val(),
                    "dev_stuff": $('.lmx_dev_stuff_studio').prop('checked') ? 1 : 0
                })
            });

            setTimeout(function(){location.reload();},200);

        });

    });
}
