$('#reset').click(function(){
    $.get('/async', {guess_letter: 'reset'}, function(data){
        $('#status_announcement').html(data['message'])
        $('#hint').html(data['hint'])
        $('#used_ltrs').html(data['used'])
        $('#debug_txt').html('')
        wrong_num = data['wrong_num']
        $('#wrong_attempts').html(wrong_num)
        updateProgressBar(10)
        reset_keyboard()
        DrawHanger(0,'#C0C0C0',true)
    });
});

function reset_keyboard(){
    for(ch = 'A'.charCodeAt(0); ch <= 'Z'.charCodeAt(0); ch++){
        console.log(String.fromCharCode(ch));
        $('#letter_'+String.fromCharCode(ch)).html('<a href="#">' + String.fromCharCode(ch) + '</a>');
    }
}

$('#show_answer').click(function(){
   $.get('/asyncret', 0, function(data){
        $('#debug_txt').html(data['secret']);
    });
});

$(document).keypress(function(e) {
   check_letter(String.fromCharCode(e.which));
   //console.log('back')
});

$('.change_language').click(function(){
    $.get('/language', {'new_language_code': $(this).attr('id')}, function(data){
        $('#game_name').html(data['game_name']);
        $('#reset').html(data['reset_game_prompt']);
        $('#show_answer').html(data['show_answer_prompt']);
        $('#languages_word').html(data['languages_word']);
        $('#status_announcement').html(data['status_announcement']);
        $('#used_letters_label').html(data['used_letters_label']);
        $('#attempts_left_label').html(data['attempts_left_label']);
    });
});

$('.alpha').click(function(){
   //console.log($(this).attr('id').substring(7,8));
   check_letter($(this).attr('id').substring(7,8));
});

function check_letter(letter){
  //alert( "Handler for .keydown() called." );
   //if($('#hint').text().indexOf('_') ==  -1) return;
   //console.log(letter)
   $.get('/async', {guess_letter: letter}, function(data){
       $('#status_announcement').html(data['message']);
       $('#hint').html(data['hint'])
       $('#used_ltrs').html(data['used'])
        if ($('#debug_txt').html() != ''){
            $('#debug_txt').html(data['secret']);
        }
       wrong_num = data['wrong_num']
       $('#wrong_attempts').html(wrong_num)
       updateProgressBar(wrong_num)
       DrawHanger(wrong_num, "black", false)
       $('#letter_' + letter.toUpperCase()).html('&nbsp;');
   });
}