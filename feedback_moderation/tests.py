from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import edit_review, Feedback
from django.urls import reverse
from . import factories


class FeedbackEditReviewTest(TestCase):

    def test_punctuation(self):
        some_text = 'fsdgsdf. gf  . .  gdf .fds , gdf ,fdsf , , gdfg... dfg.. fg dfs.'
        some_text = edit_review(some_text)

        complete = True
        for i in range(1, len(some_text)+1):
            if some_text[i] in ',.!?' and (some_text[i - 1] == ' ' or some_text[i + 1] != ' '):
                complete = False
                break
        self.assertEqual(complete, False, 'Ошибка в пробелах возле знаков')

    def test_last_symbol_is_space(self):
        some_text = 'sometext.    '
        some_text = edit_review(some_text)
        self.assertNotEqual(some_text[-1], ' ', 'Последний символ - пробел')

    def test_six_upper_chars(self):
        some_text = 'soMETEXT. tEXT. TEXT. Text'
        some_text = edit_review(some_text)
        self.assertEquals(some_text, 'Sometext. Text. Text. Text',
                          'Не преобразуется текст при 6 заглавных буквах подряд')

    def test_multiple_characters_in_one(self):
        some_text = 'Мегахарош!!!!!!!!'
        some_text = edit_review(some_text)
        self.assertEquals(some_text, 'Мегахарош!', 'Не удаляются множественные знаки')

    def test_max_functional(self):
        some_text = 'soMETEXT. tEXT. TEXT. Text... text . . text  '
        some_text = edit_review(some_text)
        self.assertEquals(some_text, 'Sometext. Text. Text. Text. Text. Text', 'Полный функционал')


class DemonstrateReviewTest(TestCase):

    def test_review_no_moderator(self):
        client = Client()
        response = client.get(reverse('feedback_moderation:review'))
        self.assertEquals(response.status_code, 404, 'Страница не должа быть доступна обычным пользователям')

    def test_review_moderator(self):
        User.objects.create_superuser(username='admin', password='admin')
        client = Client()
        client.login(username='admin', password='admin')
        response = client.get(reverse('feedback_moderation:review'))
        self.assertEqual(response.status_code, 200, 'Страница должа быть доступна модераторам')

    def test_swear_is_red(self):
        factories.FeedbackFactory()
        factories.SwearingFactory()
        User.objects.create_superuser(username='admin', password='admin')
        client = Client()
        client.login(username='admin', password='admin')
        response = client.get(reverse('feedback_moderation:review'))
        is_red = False
        if '<span style="color:red">блять' in str(response.content.decode('utf8')):
            is_red = True
        self.assertTrue(is_red, 'Слово "блять" должно быть красным')

    def test_swear_exceptions_is_not_red(self):
        factories.FeedbackFactory()
        factories.SwearingFactory()
        User.objects.create_superuser(username='admin', password='admin')
        client = Client()
        client.login(username='admin', password='admin')
        response = client.get(reverse('feedback_moderation:review'))
        is_red = False
        if '<span style="color:red>оскорблять' in str(response.content.decode('utf8')):
            is_red = True
        self.assertFalse(is_red, 'Слово "оскорблять" не должно быть красным')


class AddReviewTest(TestCase):

    def test_open_page(self):
        factories.DoctorFactory.create()
        client = Client()
        response = client.get('/add-review/1')
        self.assertEquals(response.status_code, 200, 'Ошибка при входе на страницу')

    def test_create_review(self):
        factories.DoctorFactory.create()
        client = Client()
        len_100_text = 'some text len 100some text len 100some text len 100some text len 100some text len 100some ' \
                       'text len 100some text len 100some text len 100some text len 100some text len 100some text len ' \
                       '100some text len 100some text len 100some text len 100some text len 100some text len 100some ' \
                       'text len 100some text len 100some text len 100some text len 100some text len 100some text len ' \
                       '100some text len 100some text len 100some text len 100'
        client.post('/add-review/1', {'original_text': len_100_text})
        self.assertEquals(Feedback.objects.get(id=1).original_text, len_100_text, 'Отзыв не отправляется')
