$('#reset').click(function(){
    $.get('/async', {guess_letter: 'reset'}, function(data){
        $('#status_msg').html(data['message'])
        $('#hint').html(data['hint'])
        $('#used_ltrs').html(data['used'])
        $('#debug_txt').html('')
        wrong_num = data['wrong_num']
        $('#wrong_attempts').html(wrong_num)
        updateProgressBar(10)
        DrawHanger(0,'#C0C0C0',true)
    });
});

$('#show_answer').click(function(){
   $.get('/asyncret', 0, function(data){
        $('#debug_txt').html(data['secret']);
    });
});

$(document).keypress(function(e) {
   check_letter(String.fromCharCode(e.which));
});

$('#change_language').click(function(){
    $.get('/language', 0, function(data){
        $('#status_msg').html(data['message']);
    });
});

$('.alpha').click(function(){
   //console.log($(this).attr('id').substring(7,8));
   check_letter($(this).attr('id').substring(7,8));
   $(this).html('&nbsp;');
});

function check_letter(letter){
  //alert( "Handler for .keydown() called." );
   if($('#hint').text().indexOf('_') ==  -1) return;
   //console.log(letter)
   $.get('/async', {guess_letter: letter}, function(data){
       $('#status_msg').html(data['message']);
       $('#hint').html(data['hint'])
       $('#used_ltrs').html(data['used'])
        if ($('#debug_txt').html() != ''){
            $('#debug_txt').html(data['secret']);
        }
       wrong_num = data['wrong_num']
       $('#wrong_attempts').html(wrong_num)
       updateProgressBar(wrong_num)
       DrawHanger(wrong_num, "black", false)
   });
}