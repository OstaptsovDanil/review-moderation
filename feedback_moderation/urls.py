from django.urls import path
from . import views

app_name = 'feedback_moderation'
urlpatterns = [
    path('add-review/<int:doc_id>', views.add_review, name='add_review'),
    path('review', views.reviews, name='review')
]
