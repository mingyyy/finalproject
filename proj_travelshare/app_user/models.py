from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from .constants import CITIZENSHIP_CHOICE, GENDER_CHOICES, ORG_TYPE_CHOICE, SUBJECT_CHOICE, \
    EVENT_FREQ_CHOICE, EVENT_TYPE_CHOICE, EVENT_DURATION_CHOICE, EXPERTISE_CHOICE, LANGUAGE_CHOICE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_google_maps.fields import AddressField, GeoLocationField


class User(AbstractUser):
    TYPE_CHOICES = (('0', 'Traveler'), ('1', 'Local Host'))
    type = models.CharField(max_length=1, default=None, null=True, choices=TYPE_CHOICES, verbose_name='Account Type')

    REQUIRED_FIELDS = ['type', 'email']


class ProfileStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_updated = models.DateTimeField(auto_now_add=True)
    completed_perc = models.PositiveSmallIntegerField()


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language

    class Meta:
        ordering = ('language',)


class Link(models.Model):
    category = models.CharField(max_length=50) # social
    name = models.CharField(max_length=100) # instagram
    url = models.URLField() # www.instagram.com/xxxx/

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('category','name',)


class Topic(models.Model):
    category = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ('topic',)


class ProfileTraveler(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    nationality = models.CharField(choices=CITIZENSHIP_CHOICE, max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_traveler')
    bio = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    languages = models.ManyToManyField(Language)
    # contact info
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    links = models.ManyToManyField(Link)

    def __str__(self):
        return self.user.username

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


class Program(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    subject = models.ForeignKey(Topic, on_delete=models.CASCADE)

    type = models.PositiveSmallIntegerField(choices=EVENT_TYPE_CHOICE)
    frequency = models.PositiveSmallIntegerField(choices=EVENT_FREQ_CHOICE)
    duration = models.PositiveSmallIntegerField(choices=EVENT_DURATION_CHOICE)

    title = models.CharField(max_length=120, null=False)
    description = models.TextField()
    requirement = models.TextField()

    def __str__(self):
        return self.name


class ProfileHost(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    type = models.PositiveSmallIntegerField(choices=ORG_TYPE_CHOICE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    address = AddressField(max_length=200)
    geolocation = GeoLocationField(blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_host')
    interests = models.ManyToManyField(Topic)
    interest_details = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)
    links = models.ManyToManyField(Link)

    def __str__(self):
        return self.user.username

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == '0':
            ProfileTraveler.objects.create(user=instance)
        elif instance.type == '1':
            ProfileHost.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if instance.type == '0':
        instance.profiletraveler.save()
    elif instance.type == '1':
        instance.profilehost.save()
