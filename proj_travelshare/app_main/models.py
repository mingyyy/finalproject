from django.db import models
from django.conf import settings
from app_user.constants import CITIZENSHIP_CHOICE
from django.shortcuts import reverse
from PIL import Image

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

    @property
    def get_html_url(self):
        url = reverse('app_main:trip_edit', args=(self.id,))
        return f'<a href="{url}">{self.user} in {self.destination}</a>'

    @property
    def get_detail_url(self):
        url = reverse('app_main:trip_detail', args=(self.id,))
        return f'<a href="{url}">{self.user} in {self.destination}</a>'

    def trip_duration(self):
        delta = self.end_date - self.start_date
        if delta.days >= 0:
            return delta.days
        else:
            return False


class Available(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    summary = models.CharField(max_length=100)
    extra_info = models.TextField()
    photo = models.ImageField(default='default.jpg', upload_to='space_host')

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.photo.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.name)
        except FileNotFoundError as e:
                pass

    def __str__(self):
        return self.user + " has " + self.summary

    class Meta:
        ordering = ('start_date',)

    @property
    def get_html_url(self):
        url = reverse('app_main:available_edit', args=(self.id,))
        return f'<a href="{url}">{self.summary}</a>'

    @property
    def get_detail_url(self):
        url = reverse('app_main:available_detail', args=(self.id,))
        return f'<a href="{url}">{self.summary}</a>'

    def available_duration(self):
        delta = self.end_date - self.start_date
        if delta.days >= 0:
            return delta.days
        else:
            return False
