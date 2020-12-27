$(function(){
    $('#carousel1').on('slide.bs.carousel', function (e) {

        if(e.direction == 'right'){
            $('#carousel2').carousel('prev');
        }
    });

    $('#carousel2').on('slide.bs.carousel', function (e) {
        if(e.direction == 'left'){
            $('#carousel1').carousel('next');
        }
    });
});