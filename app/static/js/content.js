$(function(){
    $('#content').on('input', function(){
        var converter = new showdown.Converter();
        text = this.value;
        html = converter.makeHtml(text);
        $('#preview').html(html);
    })
})