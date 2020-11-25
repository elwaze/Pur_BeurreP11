# import uuid
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import send_mail

# Create your models here.
#
#
# class PBUser(AbstractUser):
#     token = models.UUIDField(default=uuid.uuid4, editable=False)
#
#     def save(self, **options):
#         super().save(**options)
#         context = {
#             'user': self,
#             'link': settings.SITE_LINK
#         }
#         email_content = render_to_string('confirmation_email.html', context)
#         send_mail(
#             settings.EMAIL_MAIL_SUBJECT,
#             email_content,
#             settings.EMAIL_FROM_ADDRESS,
#             [self.email])
