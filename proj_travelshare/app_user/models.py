from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from .constants import CITIZENSHIP_CHOICE


class Expertise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Link(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_person = models.BooleanField(default=False)
    is_org = models.BooleanField(default=False)


class ProfilePerson(models.Model):

    # in total 222 countries

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(choices=GENDER_CHOICES)
    nationality = models.CharField(choices=CITIZENSHIP_CHOICE)
    phone = PhoneNumberField(unique=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_person')
    expertise = models.ManyToManyField(Expertise, through='')
    language = models.ManyToManyField(Language, related_name='')
    link = models.ManyToManyField(Link, related_name='')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.name)
        except FileNotFoundError as e:
                pass


class ProfileOrganization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    type = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    phone = PhoneNumberField(unique=True, blank=True)
    address = models.CharField(max_length=255)
    photo = models.ImageField(default='default.jpg', upload_to='profile_org')
    interest = models.ManyToManyField(Expertise, through='')
    interest_details = models.TextField(blank=True)
    language = models.ManyToManyField(Language, related_name='')
    link = models.ManyToManyField(Link, related_name='')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.name)
        except FileNotFoundError as e:
                pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_person:
            ProfilePerson.objects.create(user=instance)
        else:
            ProfileOrganization.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    if instance.is_person:
        instance.ProfilePerson.save()
    else:
        instance.ProfilePerson.save()




