from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import FormRegister, FormUserUpdate, FormProfileTravelerUpdate, FormProfileHostUpdate, \
    FormProfileHostUpdate2, FormProfileTravelerUpdate2, FormLanguage, FormAddress
from django.contrib.auth.decorators import login_required
from .decorators import traveler_required, host_required
from django.views.generic import DetailView
from .models import ProfileTraveler, ProfileHost


def viewregister(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}! You are now ready to log in!")
            return redirect('login')
    else:
        form = FormRegister()
    return render(request, 'app_user/register.html', {'form': form})


@login_required()
def profile_update_traveler(request):
    if request.method == 'POST':
        u_form = FormUserUpdate(request.POST, instance=request.user)
        t_form = FormProfileTravelerUpdate(request.POST, request.FILES, instance=request.user.profiletraveler)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request, "Personal section has been updated")
            if request.POST['save'] == "next":
                return redirect('profile_update_traveler2')
            elif request.POST['save'] == "save":
                return redirect('app_main:home')
    else:
        u_form = FormUserUpdate(instance=request.user)
        t_form = FormProfileTravelerUpdate(instance=request.user.profiletraveler)

    context = {'u_form': u_form, 't_form': t_form}
    return render(request, "app_user/profile_traveler.html", context)


@login_required()
def profile_update_traveler2(request):

    if request.method == 'POST':
        # form_lan = FormLanguage(request.POST)
        form = FormProfileTravelerUpdate2(request.POST, instance=request.user.profiletraveler)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, "Expertise section has been updated")
            return redirect('app_main:home')
    else:
        form = FormProfileTravelerUpdate2()
        # form_lan = FormLanguage(instance=request.user.profiletraveler.objects.language_set.all())

    context = {'form': form }
    return render(request, "app_user/profile_traveler2.html", context)


@login_required()
def profile_update_traveler3(request):
    if request.method == 'POST':
        form = FormProfileTravelerUpdate(request.POST,
                           request.FILES, instance=request.user.profiletraveler)
        if form.is_valid():
            form.save()
            messages.success(request, "Professional section has been updated")
            return redirect('app_main:home')
    else:
        form = FormUserUpdate(instance=request.user.profiletraveler)

    context = {'form': form}
    return render(request, "app_user/profile_traveler3.html", context)


@login_required()
def address_update(request):
    if request.method == 'POST':
        form = FormAddress(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            geolocation = form.cleaned_data.get('geolocation')
            form.save()
        return HttpResponseRedirect(reverse('profile_update_host'))
    else:
        form = FormAddress()
    return render(request, "app_user/profile_address.html", {'form': form})


@login_required()
def profile_update_host(request):
    if request.method == 'POST':
        h_form = FormProfileHostUpdate(request.POST,
                           request.FILES, instance=request.user.profilehost)
        if h_form.is_valid():
            h_form.save()
            messages.success(request, "Local host profile has been updated!")
            if request.POST['save'] == "next":
                return redirect('profile_update_host2')
            elif request.POST['save'] == "save":
                return redirect('app_main:home')
    else:
        h_form = FormProfileHostUpdate(instance=request.user.profilehost)

    context = {'h_form': h_form}
    return render(request, "app_user/profile_host.html", context)


@login_required()
def profile_update_host2(request):
    if request.method == 'POST':
        form = FormUserUpdate(request.POST, instance=request.user.profilehost)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, "Section 2 of the profile has been updated!")
            return redirect('home.html')
    else:
        form = FormProfileHostUpdate(instance=request.user.profilehost)

    context = {'form': form}
    return render(request, "app_user/profile_host2.html", context)


@login_required()
def profile_update_host3(request):
    if request.method == 'POST':
        form = FormUserUpdate(request.POST, instance=request.user.profilehost)

        if form.is_valid():
            form.save()
            messages.success(request, "Section 3 of the profile has been updated!")
            return redirect('home.html')
    else:
        form = FormProfileHostUpdate(instance=request.user.profilehost)

    context = {'form': form}
    return render(request, "app_user/profile_host3.html", context)


class TravelerDetailView(DetailView):
    model = ProfileTraveler
    # context_object_name = 'Preview Profile'
    # queryset = ProfileTraveler.objects.all()


class HostDetailView(DetailView):
    model = ProfileHost
