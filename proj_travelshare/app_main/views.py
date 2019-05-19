from django.shortcuts import render
from app_user.models import ProfileTraveler,ProfileHost, Topic, User
from django.views.generic import TemplateView, ListView,UpdateView


def home(request):
    profile_t = ProfileTraveler.objects.all()
    profile_h = ProfileHost.objects.all()

    context = {'profile_t': profile_t, 'profile_h': profile_h}
    return render(request,'app_main/home.html', context)


class ViewListPerson(ListView):
    model = ProfileTraveler
    template_name = 'app_main/travelers.html'
    context_object_name = 'users'
    ordering = ['-user.username']
    paginate_by = 5


def travelers(request):
    profile = ProfileTraveler.objects.all()

    for p in profile:
        if p.user.type == '0':
            expertise=p.expertise.all()
        else:
            print(p.user.type)

    context = {'profile': profile, 'expertise': expertise}
    return render(request,'app_main/travelers.html', context)


def hosts(request):
    profile = ProfileHost.objects.all()

    context = {'profile': profile}
    return render(request,'app_main/hosts.html', context)
