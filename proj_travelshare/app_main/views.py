from django.shortcuts import render
from app_user.models import ProfilePerson,ProfileOrganization
from django.views.generic import TemplateView, ListView,UpdateView


def home(request):
    return render(request,'app_main/home.html')


class ViewListPerson(ListView):
    model = ProfilePerson
    template_name = 'app_main/travelers.html'
    context_object_name = 'users'
    ordering = ['-user.username']
    paginate_by = 5
