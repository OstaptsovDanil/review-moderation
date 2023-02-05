import datetime

import django.conf.global_settings
import factory

import feedback_moderation.models


class SpecializationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = feedback_moderation.models.Specialization

    spec_name = factory.Sequence(lambda s: '%s' % s)


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = feedback_moderation.models.Doctor

    last_name = factory.Sequence(lambda ln: '%s' % ln)
    first_name = factory.Sequence(lambda fn: '%s' % fn)
    patronymic = factory.Sequence(lambda p: '%s' % p)
    specializations = factory.RelatedFactory(SpecializationFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = django.conf.global_settings.AUTH_USER_MODEL


class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = feedback_moderation.models.Feedback
        django_get_or_create = ('original_text',)

    doctor = factory.SubFactory(DoctorFactory)
    publishing_date_time = factory.LazyFunction(datetime.datetime.now)
    original_text = 'блять оскорблять просто текст'
    ip_address = factory.Sequence(lambda num: '%s.0.0.0' % num)
    user = factory.SubFactory(UserFactory)


class SwearingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = feedback_moderation.models.Swearing
        django_get_or_create = ('word',)

    word = 'блять'


class SwearingExceptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = feedback_moderation.models.SwearingException
        django_get_or_create = ('word',)

    word = 'оскорблять'
