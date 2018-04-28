from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
import types, random

from .models import Words, Hangers, InterfaceMessages, Languages

debug = True

def initial_view(request):
    #global debug
    secret_word = Words.objects.get(pk=random.randint(1, Words.objects.count()))
    hanger = Hangers(request, secret_word.word)
    hanger.save_to_cookies()
    # request.session.flush()
    return hanger


def make_a_guess(request, new_letter):
    if (new_letter == 'reset'):  # or(not isinstance(secret_word, TheWord)):
        return initial_view(request)
    hanger = Hangers(request)
    current_interface = InterfaceMessages.objects.filter(language=hanger.language)
    #hanger.guess(new_letter)
    if hanger.lost() or hanger.solved():
        hanger.status_message = 'Just click "Restart", OK?'
    elif not new_letter.isalpha():
        hanger.status_message = 'You typed "' + new_letter + '". Type a letter, please'
    elif hanger.letter_used(new_letter[0].upper()):
        hanger.status_message = '"' + new_letter[0].upper() + '" has already been used'
    else:
        hanger.status_message = 'You entered "' + new_letter[0].upper() + '"'
        if hanger.check_letter(new_letter):
            hanger.status_message += ' and hit!'
            if hanger.solved():
                hanger.status_message += ' You won! Click <a onClick="window.location.reload()">Reset game</a>'
        else:
            hanger.status_message += ' and missed.'
            if hanger.lost():
                hanger.status_message += ' You lost! The word was "' + hanger.secret_word + '". Click <a onClick="window.location.reload()">Reset game</a>'

    return hanger


def make_a_guess_sync(request):
    global debug
    new_letter = request.GET.get('guess_letter', '')  # [0].upper()
    # print('Left: ', hanger.attempts_left())
    if new_letter == '':
        hanger = initial_view(request)
    else:
        hanger = make_a_guess(request, new_letter)
    return render(request, 'hanger/guess.html', {
        'the_word': hanger,
        'debug': debug,
        'percentage_left': 100,
        'percentage_used' : 0,
        'language' : 'rus'
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