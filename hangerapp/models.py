from django.db import models

class Languages(models.Model):
    code = models.CharField(max_length=3)
    full_name = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Words(models.Model):
    word = models.CharField(max_length=50)
    #language = models.ForeignKey('Languages', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.word# + '(' + str(self.language) + ')'

class InterfaceMessages(models.Model):
    language = models.ForeignKey('Languages', on_delete=models.PROTECT)
    status_announcement = models.CharField(max_length=200, null=True)
    game_name = models.CharField(max_length=20, null=True)
    reset_game_prompt = models.CharField(max_length=50, null=True)
    show_answer_prompt = models.CharField(max_length=50, null=True)
    languages_word = models.CharField(max_length=20, null=True)
    used_letters_label = models.CharField(max_length=50, null=True)
    attempts_left_label = models.CharField(max_length=50, null=True)
    just_click_reset_message = models.CharField(max_length=100, null=True)
    type_a_letter_message = models.CharField(max_length=100, null=True)
    letter_already_used_message = models.CharField(max_length=100, null=True)
    you_entered_message = models.CharField(max_length=50, null=True)
    and_hit_message = models.CharField(max_length=20, null=True)
    and_missed_message = models.CharField(max_length=20, null=True)
    you_won_message = models.CharField(max_length=100, null=True)
    you_lost_message = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.language.full_name + ': ' + self.status_announcement + '...'

class Hangers:
    max_wrong_attempts = 10

    def __init__(self, request, word='', language=0):
        self.request = request
        if word == '':
            self.secret_word = request.session['word']
            self.hint = request.session['hint']
            self.used_letters = request.session['used']
            self.wrong_attempts = request.session['failures']
            #self.status_message = '?--'
            self.language = Languages.objects.get(code=request.session['language'])
        else:
            self.secret_word = word
            self.hint = "_" * len(self.secret_word)
            self.used_letters = ''
            self.wrong_attempts = 0
            #self.status_message = '--?'
            if language==0:
                self.language = Languages.objects.get(pk=1)
            else:
                self.language = language
        current_interface = InterfaceMessages.objects.get(language=self.language)
        self.status_message = current_interface.status_announcement

    def save_to_cookies(self):
        self.request.session['word'] = self.secret_word
        self.request.session['hint'] = self.hint
        self.request.session['used'] = self.used_letters
        self.request.session['failures'] = self.wrong_attempts
        self.request.session['language'] = self.language.code

    def check_letter(self, letter):
        letter = letter[0].upper()
        self.add_used(letter)
        retvalue = letter in self.secret_word.upper()
        if retvalue:
            for i in filter(lambda c: c[1].upper() == letter, enumerate(self.secret_word.upper())):
                self.hint = self.hint[:i[0]] + letter + self.hint[i[0] + 1:]
            self.save_hint()
        else:
            self.add_miss(letter)
        return retvalue

    def save_hint(self):
        self.request.session['hint'] = self.hint

    def add_miss(self, letter):
        self.wrong_attempts += 1
        self.request.session['failures'] = self.wrong_attempts

    def solved(self):
        return not "_" in self.hint

    def lost(self):
        return self.wrong_attempts >= 10

    def finished(self):
        return self.solved() or self.lost()

    def attempts_left(self):
        return self.max_wrong_attempts - self.wrong_attempts

    def add_used(self, letter):
        if letter in self.used_letters:
            return False
        self.used_letters = ''.join(sorted(self.used_letters + letter))
        self.request.session['used'] = self.used_letters
        return True

    def letter_used(self, letter):
        return letter.upper() in self.used_letters

    def get_answer(self):
        return self.secret_word

    def set_language(self, new_language_code):
        self.language = Languages.objects.get(code=new_language_code)
        self.save_to_cookies()

    # def __str__(self):
    #    return self.secret_word + ' (' + '_'*len(self.secret_word)+ ')' #guessed

    #def guess(self, new_letter):
