
from django.urls import path
from . import views

app_name = "app_info"

urlpatterns = [
    path('visa/', views.visa_info, name='visa_info'),

]