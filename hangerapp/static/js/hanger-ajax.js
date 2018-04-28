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
  //alert( "Handler for .keydown() called." );
   letter = String.fromCharCode(e.which)
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
});

$('#change_language').click(function(){
    $.get('/language', 0, function(data){
        $('#status_msg').html(data['message']);
    });
});