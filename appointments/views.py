from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives, send_mail  # импортируем класс для создание объекта письма с html
from datetime import datetime
from django.utils import timezone
from .models import Subscription, Category

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment
from news.models import Post


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  #  это то же, что и message
            from_email='alice-for-me@yandex.ru',
            to=['alisa.xorok@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('appointments:make_appointment')


def notify_subscribers(article):
    subscriptions = Subscription.objects.filter(category=article.category)
    for subscription in subscriptions:
        send_mail(
            subject=f'New article in {article.category.name}',
            message=f'New article: {article.title}\nRead more: {article.get_absolute_url()}',
            from_email='alice-for-me@yandex.ru',
            recipient_list=[subscription.user.email],
        )

def weekly_summary():
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    articles = Post.objects.filter(created_at__gte=one_week_ago)
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        user_articles = articles.filter(category=subscription.category)
        if user_articles.exists():
            send_mail(
                subject='Weekly article summary',
                message='\n'.join([f'{article.title}: {article.get_absolute_url()}' for article in user_articles]),
                from_email='alice-for-me@yandex.ru',
                recipient_list=[subscription.user.email],
            )
