from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
import types, random

from .models import Words, Hangers

debug = True


def initial_view(request):
    global debug
    secret_word = Words.objects.get(pk=random.randint(1, Words.objects.count()))
    hanger = Hangers(request, secret_word.word)
    hanger.save_to_cookies()
    # request.session.flush()
    return hanger


def make_a_guess(request, new_letter):
    if (new_letter == '*'):  # or(not isinstance(secret_word, TheWord)):
        return initial_view(request)
    hanger = Hangers(request)
    hanger.guess(new_letter)
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