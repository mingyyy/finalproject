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

from django.urls import path
from .views import home, travelers, hosts, trip, CalendarView

app_name = "app_main"

urlpatterns = [
    path('', home, name='home'),
    path('travelers/', travelers, name='travelers'),
    path('hosts/', hosts, name='hosts'),

    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('trip/edit/<int:id>/', trip, name='trip_edit'),
    path('trip/new/', trip, name='trip_new'),
]