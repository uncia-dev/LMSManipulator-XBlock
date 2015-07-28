function AnalyticsExtrasXBlockStudio(runtime, xblock_element) {

    $(function ($) {

        // Add Save Button
        $('ul', '.modal-actions')
            .append(
                $('<li>', {class: "action-item"}).append(
                    $('<a />', {class: "action-primary", id: "aex_submit", text: "Save"})
                )
            );

        $('#aex_submit').click(function(eventObject) {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(xblock_element, 'studio_submit'),
                data: JSON.stringify({
                    "display_name": $('.aex_display_name').val(),
                    "hide_nav_buttons": ($('.aex_hide_nav_buttons').attr("checked") === "checked") ? 1 : 0,
                    "hide_sequence_bottom": ($('.aex_hide_sequence_bottom').attr("checked") === "checked") ? 1 : 0,
                    "tick_interval": $('.aex_tick_interval').val(),
                    "csv_url": $('.aex_csv_url').val(),
                    "sequence_list_staff": $('.aex_sequence_list_staff').val()
                })
            });

            setTimeout(function(){location.reload();},200);

        });

    });
}
