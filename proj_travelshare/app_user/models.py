from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from .constants import CITIZENSHIP_CHOICE, GENDER_CHOICES, ORG_TYPE_CHOICE, TOPIC_CHOICE, \
    EVENT_FREQ_CHOICE, EVENT_TYPE_CHOICE, EVENT_DURATION_CHOICE, EXPERTISE_CHOICE
from django.db.models.signals import post_save
from django.dispatch import receiver
from ktag.fields import TagField


class Expertise(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Language(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    level = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Link(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    url = models.URLField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('category','name',)


class Topic(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Program(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    type = models.PositiveSmallIntegerField(choices=EVENT_TYPE_CHOICE)
    frequency = models.PositiveSmallIntegerField(choices=EVENT_FREQ_CHOICE)
    duration = models.PositiveSmallIntegerField(choices=EVENT_DURATION_CHOICE)
    topic = models.CharField(max_length=20)
    title = models.CharField(max_length=120, null=False)
    description = models.TextField()
    requirement = models.TextField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    TYPE_CHOICES = (('0', 'Traveler'), ('1', 'Local Host'))
    type = models.CharField(max_length=1, default=None, null=True, choices=TYPE_CHOICES, verbose_name='Account Type')

    REQUIRED_FIELDS = ['type', 'email']


class ProfileStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    time_updated = models.DateTimeField(auto_now_add=True)
    completed_perc = models.PositiveSmallIntegerField()


class ProfileTraveler(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1)
    nationality = models.CharField(choices=CITIZENSHIP_CHOICE, max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone = PhoneNumberField(unique=True, null=True,blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_traveler')
    experience = models.TextField(null=True, blank=True)
    expertise = models.ManyToManyField(Expertise)
    language = models.ManyToManyField(Language)
    link = models.ManyToManyField(Link)

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


class ProfileHost(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    type = models.PositiveSmallIntegerField(choices=ORG_TYPE_CHOICE, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    phone = PhoneNumberField(unique=True, null=True,blank=True)
    address = models.CharField(max_length=255)
    photo = models.ImageField(default='default.jpg', upload_to='profile_host')
    interest = models.ManyToManyField(Expertise)
    interest_details = models.TextField(blank=True)
    language = models.ManyToManyField(Language)
    link = models.ManyToManyField(Link)

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
