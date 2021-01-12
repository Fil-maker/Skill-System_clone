$(function(){

    function assign(e) {
        var data = e.value.split(',');
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/forms/assign/" + event_id + "/" + data[0], {
            method: 'post',
            dataType: 'json',

            success: function() {
                $.jGrowl('', {'header': 'Successfully assigned'});
            },

            error: function() {
                $.jGrowl(data["message"], {'header': 'Error'});
                location.reload();
            }
        });
    }

    function del(e) {
        var data = e.value;
        var href = window.location.href;
        var event_id = href.split("/")[4];
        $.ajax("/ajax/forms/delete/" + event_id + "/" + data[0], {
            method: 'post',
            dataType: 'json',

            success: function() {
                $.jGrowl('', {'header': 'Successfully deleted'});
            },

            error: function() {
                $.jGrowl(data["message"], {'header': 'Error'});
                location.reload();
            }
        });
    }

    $('.assign-btn').click(function(){
        var self = this;
        var val = this.value;
        data = val.split(',');

        if(data[1] % 2 == 0){
            assign(self);
            $(this).attr('class', 'assign-btn btn btn-danger');
            $(this).text('delete');
            self.value = data[0] + ',' + (Number.parseInt(data[1]) + 1);
        }else{
            del(self);
            $(this).attr('class', 'assign-btn btn btn-success');
            $(this).text('assign');
            self.value = data[0] + ',' + (Number.parseInt(data[1]) + 1);
        }
    });

    $('.delete-btn').on("click", function(){
        var self = this;
        var val = this.value;
        data = val.split(',');

        if(data[1] % 2 == 0){
            assign(self);
            $(this).attr('class', 'delete-btn btn btn-danger');
            $(this).text('delete');
            self.value = data[0] + ',' + (Number.parseInt(data[1]) + 1);
        }else{
            del(self);
            $(this).attr('class', 'delete-btn btn btn-success');
            $(this).text('assign');
            self.value = data[0] + ',' + (Number.parseInt(data[1]) + 1);
        }
    });
});



