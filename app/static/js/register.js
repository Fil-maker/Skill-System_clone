$('#cntry-fld').onclick = function(){
    if($('#cntry-fld: selected').text() == "Russian Federation (the)"){
        $('#region-div').show();
    }
    else{
        $('#region-div').hide();
    }
}