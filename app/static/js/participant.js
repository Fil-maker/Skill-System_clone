$(function() {
    $('.promote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        $.ajax("/ajax/participants/promote/" + data[2] + "/" + data[0] + "/" + data[1], {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully promoted'});
                location.reload();
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.demote-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        $.ajax("/ajax/participants/demote/" + data[2] + "/" + data[0] + "/" + data[1], {
	        method: 'post',
	        dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully demoted'});
                location.reload();
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.assign-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        $.ajax("/ajax/participants/assign/" + data[1] + "/" + data[0], {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully assigned'});
                location.reload();
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });

    $('.delete-btn').on("click", function() {
        var data = this.value.split(",");
        var href = window.location.href;
        $.ajax("/ajax/participants/exclude/" + data[1] + "/" + data[0], {
            method: 'post',
            dataType: 'json',

            success: function(data) {
                $.jGrowl('', {'header': 'Successfully deleted'});
                location.reload();
            },

            error: function(data) {
                $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
    });
});
