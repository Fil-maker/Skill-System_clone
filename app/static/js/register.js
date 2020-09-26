$(function(){
    $('#cntry-fld').change(function(){
        if($('#cntry-fld').val() == "Russian Federation (the)"){
            $('#region-div').show();
        }
        else{
            $('#region-div').hide();
        }
    })

    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#preload').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
      }
    }

    $("#photoField").change(function() {
      readURL(this);
    });

});
