$(function(){
    $('.assign-btn').on("click", function() {
        var data = this.value;
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/forms/assign/" + event_id + "/" + data, {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully assigned'});
                location.reload(); // Заглушка TODO
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.delete-btn').on("click", function() {
        var data = this.value;
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/forms/delete/" + event_id + "/" + data, {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully deleted'});
                location.reload(); // Заглушка TODO
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });
});