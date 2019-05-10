from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,ProfileTraveler, ProfileHost, ProfileStatus, Expertise, Link, Language, Topic
from .models import User
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(ProfileTraveler)
admin.site.register(ProfileHost)
admin.site.register(ProfileStatus)

admin.site.register(Topic)
admin.site.register(Expertise)
admin.site.register(Link)
admin.site.register(Language)

