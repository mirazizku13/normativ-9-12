import os.path
import threading

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from django.core.mail import EmailMessage, EmailMultiAlternatives


def send_custom_mail(to, subject, content):
    django_send_mail(
        subject,
        content,
        # 'miraziz2008@yandex.com',
        from_email='miraziz2008@yandex.com',
        recipient_list=[to],
        fail_silently=False,
    )
def send_email_with_class(to, subject, content):
    file_path = os.path.join(settings.BASE_DIR, "file.pdf")

    email = EmailMessage(
        subject="fayl bilan email",
        body="mana biriktirilgan fayl",
        from_email="mirazizmirabdulayev11@gmail.com",
        to=["mirazizmirabdulayev11@gmail.com"],
    )

    with open(file_path, "rb") as f:
        email.attach("file.pdf", f.read(), "application/pdf")
    email.send()

def send_mail_multi_alternative():
    file_path = os.path.join(settings.BASE_DIR, "file.pdf")

    subject = "fayl bilan email"
    text_content = "mana biriktirilgan fayl"
    from_email = settings.EMAIL_HOST_USER
    to = ["mirazizmirabdulayev11@gmail.com"]

    html_content = """
        <h1 style="color:#3b82f6">Salom!</h1>
        <p>Bu <strong>HTML</strong> email.</p>
        <a href="https://example.com">Saytga o'tish</a>
    """

    email = EmailMultiAlternatives(
        subject, text_content, from_email, to
    )

    email.attach_alternative(html_content, "text/html")

    with open(file_path, "rb") as f:
        email.attach("file.pdf", f.read(), "application/pdf")
    email.send()


def thread_send_mail(to, subject, content):
    thread = threading.Thread(
        target=send_custom_mail,
        args=(to, subject, content))
    thread.start()

def thread_send_mail_multi_alternative():
    thread = threading.Thread(target=send_mail_multi_alternative)
    thread.start()

def thread_send_file_to_emil():
    pass

