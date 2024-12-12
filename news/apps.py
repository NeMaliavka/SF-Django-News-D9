from django.apps import AppConfig
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from .models import send_weekly_newsletters  # Импортируйте Вашу функцию

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # Инициализация планировщика
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(send_weekly_newsletters, 'interval', weeks=1)
        scheduler.start()
