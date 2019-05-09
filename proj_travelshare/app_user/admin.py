from django.contrib import admin
from .models import ProfilePerson, ProfileOrganization,Topic,Expertise,Link,Language,User

# Register your models here.
admin.site.register(User)
admin.site.register(ProfilePerson)
admin.site.register(ProfileOrganization)
admin.site.register(Topic)
admin.site.register(Expertise)
admin.site.register(Link)
admin.site.register(Language)
