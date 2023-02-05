from django.contrib import admin
from .models import Specialization, Doctor, Feedback, Swearing, SwearingException
from django.forms import Textarea
from django.db import models


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'patronymic', 'specializations__spec_name']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    raw_id_fields = ('doctor',)
    readonly_fields = ['publishing_date_time', 'original_text']
    list_display = ('doctor', 'publishing_date_time', 'original_text_trim', 'edit_text_trim', 'ip_address', 'user')
    search_fields = ['doctor__full_name', 'publishing_date_time', 'original_text',
                     'edit_text', 'ip_address', 'user__username']
    formfield_overrides = {
        models.CharField: {'widget': Textarea}
    }


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    search_fields = ['spec_name']


@admin.register(Swearing)
class SwearingAdmin(admin.ModelAdmin):
    search_fields = ['word']


@admin.register(SwearingException)
class SwearingExceptionAdmin(admin.ModelAdmin):
    search_fields = ['word']
