from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

ADMINISTRATOR = 'AD'
AUTOR_NEWS = 'AN'
NORMAL_USER = 'NU'

roles = [
    (ADMINISTRATOR, 'Администратор'),
    (AUTOR_NEWS, 'Автор статей'),
    (NORMAL_USER, 'Пользователь')
]

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} subscribed to {self.category.name}'

def send_weekly_newsletters():
    one_week_ago = timezone.now() - timedelta(days=7)
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        new_posts = Post.objects.filter(categories=subscription.category, created_at__gte=one_week_ago)
        if new_posts.exists():
            message = "New articles in your subscribed category:\n"
            for post in new_posts:
                message += f"{post.title}: {post.get_absolute_url()}\n"
            send_mail(
                subject='Weekly Newsletter',
                message=message,
                from_email='alice-for-me@yandex.ru',
                recipient_list=[subscription.user.email],
            )
            
class User(models.Model):
    user_name = models.CharField(max_length=255)
    role = models.CharField(max_length=2,
                            choices=roles,
                            default=NORMAL_USER)
