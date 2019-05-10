from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,ProfilePerson, ProfileOrganization,Topic,Expertise,Link,Language

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ProfilePerson)
admin.site.register(ProfileOrganization)
admin.site.register(Topic)
admin.site.register(Expertise)
admin.site.register(Link)
admin.site.register(Language)
