from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
import types, random

from .models import Words, Hangers, InterfaceMessages, Languages

debug = True

def initial_view(request, language=0):
    #global debug
    secret_word = Words.objects.get(pk=random.randint(1, Words.objects.count()))
    hanger = Hangers(request, secret_word.word, language)
    hanger.save_to_cookies()
    # request.session.flush()
    return hanger


def make_a_guess(request, new_letter):
    hanger = Hangers(request)
    if (new_letter == 'reset'):  # or(not isinstance(secret_word, TheWord)):
        return initial_view(request, hanger.language)
    current_interface = InterfaceMessages.objects.get(language=hanger.language)
    #hanger.guess(new_letter)
    if hanger.lost() or hanger.solved():
        hanger.status_message = current_interface.just_click_reset_message
    elif not new_letter.isalpha():
        hanger.status_message = current_interface.you_entered_message.format(new_letter)
    elif hanger.letter_used(new_letter[0].upper()):
        hanger.status_message = current_interface.letter_already_used_message.format(new_letter[0].upper())
    else:
        hanger.status_message = current_interface.you_entered_message.format(new_letter[0].upper())
        if hanger.check_letter(new_letter):
            hanger.status_message += ' ' + current_interface.and_hit_message
            if hanger.solved():
                hanger.status_message += ' ' + current_interface.you_won_message
        else:
            hanger.status_message += ' ' + current_interface.and_missed_message
            if hanger.lost():
                hanger.status_message += ' ' + current_interface.you_lost_message.format(hanger.secret_word)

    return hanger


def make_a_guess_sync(request):
    global debug
    new_letter = request.GET.get('guess_letter', '')  # [0].upper()
    if new_letter == '':
        hanger = initial_view(request)
    else:
        hanger = make_a_guess(request, new_letter)
    languages = Languages.objects.all()
    interface_messages = InterfaceMessages.objects.get(language__code=hanger.language.code)
    return render(request, 'hanger/guess.html', {
        'the_word': hanger,
        'debug': debug,
        'percentage_left': 100,
        'percentage_used' : 0,
        'interface_messages' : interface_messages,
        'all_languages' : languages
    })


def make_a_guess_async(request):
    new_letter = False
    if request.method == 'GET':
        new_letter = request.GET['guess_letter']
    if new_letter:
        hanger = make_a_guess(request, new_letter)
        return JsonResponse({'message': hanger.status_message,
                             'hint': hanger.hint,
                             'used': hanger.used_letters,
                             'wrong_num': hanger.attempts_left(),
                             'secret': hanger.secret_word
                             })  # , safe = False)
    else:
        return HttpResponse(0)  # None


def get_secret(request):
    hanger = Hangers(request)
    return JsonResponse({'secret': hanger.secret_word})

def change_language(request):
    new_language_code = request.GET['new_language_code']
    hanger = Hangers(request)
    hanger.set_language(new_language_code)
    interface_messages = InterfaceMessages.objects.get(language__code=new_language_code)
    return JsonResponse({'game_name': interface_messages.game_name,
                         'reset_game_prompt': interface_messages.reset_game_prompt,
                         'show_answer_prompt': interface_messages.show_answer_prompt,
                         'languages_word': interface_messages.languages_word,
                         'status_announcement': interface_messages.status_announcement,
                         'used_letters_label': interface_messages.used_letters_label,
                         'attempts_left_label': interface_messages.attempts_left_label
                         })
