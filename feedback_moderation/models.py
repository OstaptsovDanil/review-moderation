from django.db import models
from django.contrib.auth.models import User
from string import punctuation
import re


def edit_review(text):
    symbols = list(punctuation)
    new_text = text
    while '  ' in new_text:
        new_text = new_text.replace('  ', ' ')
    for symbol in symbols:
        while symbol * 2 in new_text:
            new_text = new_text.replace(symbol * 2, symbol)
        while f"{symbol} {symbol}" in new_text:
            new_text = new_text.replace(f"{symbol} {symbol}", symbol)
    upper_count = 0
    need_to_capitalize = False
    for char in new_text:
        if char.isupper():
            upper_count += 1
        else:
            upper_count = 0
        if upper_count == 6:
            need_to_capitalize = True
            break
    sentences = []
    for s in re.split(r'(?<=[.!?…])', new_text):
        s = s.strip()
        s = list(s)
        if len(s) > 1:
            while s[-2] == ' ':
                del s[-2]
        s = ''.join(map(str, s))
        if need_to_capitalize:
            sentences.append(s.capitalize())
        else:
            sentences.append(s)
    new_text = ' '.join(sentences)
    while new_text[-1] == ' ':
        new_text = new_text[:-1]
    return new_text


def trim(char_field):
    max_length = 50
    if len(str(char_field)) > max_length:
        return f"{char_field[:max_length]}..."
    return char_field


class Specialization(models.Model):
    spec_name = models.CharField(verbose_name='Название специальности', max_length=32, unique=True)

    def __str__(self):
        return self.spec_name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Doctor(models.Model):
    last_name = models.CharField(verbose_name='Фамилия', max_length=24)
    first_name = models.CharField(verbose_name='Имя', max_length=24)
    patronymic = models.CharField(verbose_name='Отчество', max_length=24, null=True, blank=True)

    specializations = models.ManyToManyField(Specialization, verbose_name='Специальности')

    @property
    def full_name(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name='ФИО врача', on_delete=models.CASCADE)
    publishing_date_time = models.DateTimeField(verbose_name='Время публикации', auto_now=True)
    original_text = models.CharField(verbose_name='Оригинальный текст', max_length=1000)
    edit_text = models.CharField(verbose_name='Отредактированный текст', max_length=1000)
    ip_address = models.GenericIPAddressField(verbose_name='IP-адрес пользователя')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)

    def edited_review(self):
        return edit_review(self.original_text)

    def original_text_trim(self):
        return trim(self.original_text)

    original_text_trim.short_description = 'Оригинальный текст'

    def edit_text_trim(self):
        return trim(self.edit_text)

    edit_text_trim.short_description = 'Отредактированный текст'

    def __str__(self):
        return f"Отзыв на {self.doctor} от {self.user}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Swearing(models.Model):
    word = models.CharField(verbose_name='Слово', max_length=32, unique=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Мат'
        verbose_name_plural = 'Маты'


class SwearingException(models.Model):
    word = models.CharField(verbose_name='Слово', max_length=32, unique=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Исключение'
        verbose_name_plural = 'Исключения'
