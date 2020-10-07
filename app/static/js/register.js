$(function(){
    show_regions_if_needed();
    $('#cntry-fld').on("change", show_regions_if_needed);

    function show_regions_if_needed() {
        if($('#cntry-fld').val() == $('#cntry-fld').attr('data-ru_id')){
            $('#region-div').show();
        }
        else{
            $('#region-div').hide();
        }
    }

    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $("#preload").attr("src", e.target.result);
          $("#photo_base64").val(e.target.result);
          $("#photoField").val("");
          $("#croppie-toggler").attr("disabled", false);
        }

        reader.readAsDataURL(input.files[0]);
      }
    }

    $("#photoField").change(function() {
      readURL(this);
    });

    if ($("#photo_base64").val() != "") {
      $("#preload").attr("src", $("#photo_base64").val());
      $("#croppie-toggler").attr("disabled", false);
    }
});

var thumbnail = $(".thumbnail").croppie({
  viewport: {
    width: 400,
    height: 400,
    type: "square"
  },
  boundary: {
    width: "100%",
    height: "100%"
  },
});

$("#croppie-toggler").on("click", function() {
  $(".thumbnail").croppie("bind", {
    url: $("#preload").attr("src")
  })
});

$("#save-button").on("click", function() {
  var image = $("#preload").attr("src");
  var format;
  if (image.startsWith("data:image/png"))
    format = "png";
  else if (image.startsWith("data:image/png"))
    format = "webp";
  else
    format = "jpeg";
  thumbnail.croppie("result", {
    type: "base64",
    size: "original",
    size: "original",
    format: format
  }).then(function(base64) {
    $("#preload").attr("src", base64);
    $("#photo_base64").val(base64);  
  });


  $("#croppie-modal").modal("hide");
})