from datetime import date, timedelta
from django.core.mail import send_mail
from .models import Motive

def notify_deadlines():
    upcoming = Motive.objects.filter(end_date=date.today() + timedelta(days=1))
    for motive in upcoming:
        send_mail(
            subject="⏰ Motivation Reminder!",
            message=f"Your motive '{motive.title}' ends tomorrow. Keep pushing!",
            from_email="noreply@selfgrowth.com",
            recipient_list=[motive.user.email],
        )
