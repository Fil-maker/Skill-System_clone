$(function() {
    $('.promote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/participants/promote/" + event_id + "/" + data[0] + "/" + data[1], {
            method: 'post',
            dataType: 'json',

            success: function() {
                $.jGrowl('', {'header': 'Successfully promoted'});
                location.reload(); // Заглушка TODO
            },

            error: function() {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.demote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/participants/demote/" + event_id + "/" + data[0] + "/" + data[1], {
	        method: 'post',
	        dataType: 'json',

            success: function() {
                $.jGrowl('', {'header': 'Successfully demoted'});
                location.reload(); // Заглушка TODO
            },

            error: function() {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.assign-btn').on("click", function() {
        var user_id = this.value;
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/participants/assign/" + event_id + "/" + user_id, {
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
        var user_id = this.value;
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/participants/exclude/" + event_id + "/" + user_id, {
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
