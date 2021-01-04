$(function(){
    $('.delete-btn').on('click', function() {
        var start_url = "/ajax/delete";
        var data = this.value.split(',')
        var objType = data[0];
        var objId = data[1];
        if (objType == '1'){
            start_url += "/user/" + objId;
        }else if (objType == '2'){
            start_url += "/event/" + objId;
        }else if (objType == '3'){
            start_url += "/form/" + objId;
        }
            $.ajax({
                url: start_url,
                method: 'post',
                dataType: 'json',

                success: function() {
                    window.location.href = "/";
                },

                error: function() {
                    $.jGrowl(data["message"], {'header': 'Error'});
            }
        });
   });
});