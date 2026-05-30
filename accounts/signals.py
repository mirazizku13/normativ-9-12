from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from common.service import thread_send_mail
from accounts.models import User

# u1 = User.objects.create_user(username='user', email='', password='')


@receiver(post_save, sender=User)
def register_new_user(sender, instance, created, **kwargs):
    if created:
        # send_mail(
        #     subject='New User',
        #     from_email=settings.EMAIL_HOST_USER,
        #     message=f'Welcome {instance.username}!',
        #     recipient_list=[instance.email],
        #     fail_silently=False,
        # )
        thread_send_mail(
            to=instance.email,
            subject='New user created',
            content='New user created Welcome!',
        )