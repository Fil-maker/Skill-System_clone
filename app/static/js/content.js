$(function(){
    $('#content').on('input', function(){
        var converter = new showdown.Converter();
        text = this.value;
        if (text != ''){
            html = converter.makeHtml(text);
            $('#preview').html(html);
        } else{
            $('#preview').html('<p style="color: gray;">Nothing there!</p>');
        }
    })
})