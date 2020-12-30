$(function() {
    $('.promote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/promote/" + event_id + "/" + data[0] + "/" + data[1], {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully promoted'});
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.demote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/demote/" + event_id + "/" + data[0] + "/" + data[1], {
	        method: 'post',
	        dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully demoted'});
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });
});
