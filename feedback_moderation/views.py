from django.shortcuts import render
from .models import Doctor, Feedback, Swearing, SwearingException
from django.http import HttpResponse, HttpResponseNotFound
from .forms import AddReviewForm


def get_ip(meta):
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = meta.get('REMOTE_ADDR')
    return ip_address


def add_review(request, doc_id):
    doctor = Doctor.objects.prefetch_related('specializations').get(id=doc_id)
    if request.user.is_anonymous:
        user = None
    else:
        user = request.user

    ip_address = get_ip(request.META)

    form = AddReviewForm()

    if request.method == 'GET':
        return render(request, 'feedback_moderation/add_review.html', context={
            'doctor': doctor,
            'form': form,
        })

    if request.method == 'POST':
        r = request.POST
        print(r)
        form = AddReviewForm(r)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor = doctor
            review.user = user
            review.ip_address = ip_address
            review.edit_text = review.edited_review()
            review.save()
            return HttpResponse('Отзыв успешно отправлен')
        else:
            return render(request, 'feedback_moderation/add_review.html', context={
                'doctor': doctor,
                'form': form,
            })


def reviews(request):
    if request.user.is_superuser:
        feedbacks = Feedback.objects.select_related('doctor').select_related('user').all()
        feedbacks = feedbacks.prefetch_related('doctor__specializations')
        feedbacks = feedbacks.order_by('publishing_date_time')

        swearing = list(Swearing.objects.values_list('word', flat=True))
        swearing_exceptions = list(SwearingException.objects.values_list('word', flat=True))

        return render(request, 'feedback_moderation/reviews.html', context={
            'feedbacks': feedbacks,
            'swearing': swearing,
            'swearing_exceptions': swearing_exceptions
        })
    else:
        return HttpResponseNotFound()
