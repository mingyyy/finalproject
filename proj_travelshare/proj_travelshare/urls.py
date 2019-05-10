"""proj_travelshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_user import views as user_views
from django.contrib.auth.views import (LogoutView, LoginView,
    PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),
    path('register/', user_views.viewregister, name='register'),
    path('profile_person/',user_views.ViewProfilePersonUpdate, name='profile_person'),
    path('profile_org/',user_views.ViewProfileOrgUpdate, name='profile_org'),
    path('login/', LoginView.as_view(template_name="app_user/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="app_user/logout.html"), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

