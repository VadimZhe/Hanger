$('#reset').click(function(){
    $.get('/hanger/async', {guess_letter: '*'}, function(data){
        $('#status_msg').html(data['message']);
        $('#hint').html(data['hint'])
        $('#used_ltrs').html(data['used'])
        $('#debug_txt').html('')
        wrong_num = data['wrong_num']
        $('#wrong_attempts').html(wrong_num)
        DrawHanger(wrong_num)
    });
});

$('#wrong_attempts').click(function(){
   $.get('/hanger/asyncret', 0, function(data){
        $('#debug_txt').html(data['secret']);
    });
});

$(document).keypress(function(e) {
  //alert( "Handler for .keydown() called." );
   letter = String.fromCharCode(e.which)
   //console.log(letter)
   $.get('/hanger/async', {guess_letter: letter}, function(data){
       $('#status_msg').html(data['message']);
       $('#hint').html(data['hint'])
       $('#used_ltrs').html(data['used'])
        if ($('#debug_txt').html() != ''){
            $('#debug_txt').html(data['secret']);
        }
       wrong_num = data['wrong_num']
       $('#wrong_attempts').html(wrong_num)
       DrawHanger(wrong_num)
   });
});