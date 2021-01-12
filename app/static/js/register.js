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
});
