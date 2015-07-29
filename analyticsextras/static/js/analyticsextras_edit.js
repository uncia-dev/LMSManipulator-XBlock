function AnalyticsExtrasXBlockStudio(runtime, xblock_element) {

    if ($('.aex_hide_sidebar').prop('checked'))
        $('.aex_toggle_sidebar').prop('disabled', true).prop('checked', false);

    $(function ($) {

        // Add Save Button
        $('ul', '.modal-actions')
            .append(
                $('<li>', {class: "action-item"}).append(
                    $('<a />', {class: "action-primary", id: "aex_submit", text: "Save"})
                )
            );


        $('.aex_hide_sidebar').click(function(eventObject) {

            if ($('.aex_hide_sidebar').prop('checked'))
                $('.aex_toggle_sidebar').prop('disabled', true).prop('checked', false);
            else
                $('.aex_toggle_sidebar').prop('disabled', false);

        });

        $('#aex_submit').click(function(eventObject) {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'studio_submit'),
                data: JSON.stringify({
                    "display_name": $('.aex_display_name').val(),
                    "hide_nav_buttons": $('.aex_hide_nav_buttons').prop('checked') ? 1 : 0,
                    "hide_nav": $('.aex_hide_nav').prop('checked') ? 1 : 0,
                    "hide_sequence_bottom": $('.aex_hide_sequence_bottom').prop('checked') ? 1 : 0,
                    "hide_sidebar": $('.aex_hide_sidebar').prop('checked') ? 1 : 0,
                    "toggle_sidebar": $('.aex_toggle_sidebar').prop('checked') ? 1 : 0,
                    "tick_interval": $('.aex_tick_interval').val(),
                    "csv_url": $('.aex_csv_url').val(),
                    "sequence_list_staff": $('.aex_sequence_list_staff').val()
                })
            });

            setTimeout(function(){location.reload();},200);

        });

    });
}
