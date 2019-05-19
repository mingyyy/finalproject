from django.db import models
from django.conf import settings
from app_user.constants import CITIZENSHIP_CHOICE, GENDER_CHOICES, ORG_TYPE_CHOICE, SUBJECT_CHOICE, \
    EVENT_FREQ_CHOICE, EVENT_TYPE_CHOICE, EVENT_DURATION_CHOICE, EXPERTISE_CHOICE, LANGUAGE_CHOICE


class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    destination = models.CharField(choices=CITIZENSHIP_CHOICE, max_length=30)
    details = models.TextField()

    def __str__(self):
        return self.destination

    class Meta:
        ordering = ('start_date',)


class Available(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    summary = models.CharField(max_length=100)
    extra_info=models.TextField()

    def __str__(self):
        return self.summary

    class Meta:
        ordering = ('start_date',)
