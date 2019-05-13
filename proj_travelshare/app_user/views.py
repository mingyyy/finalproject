from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import FormRegister, FormUserUpdate, FormProfileTravelerUpdate, FormProfileHostUpdate, \
    FormProfileHostUpdate2, FormProfileTravelerUpdate2, FormLanguage, FormAddress, FormProgram, FormSpace
from django.contrib.auth.decorators import login_required
from .decorators import traveler_required, host_required
from django.views.generic import DetailView
from .models import ProfileTraveler, ProfileHost, Space, Program
from django.contrib.auth import logout, login, authenticate


def viewregister(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            new_user=form.save()
            username = form.cleaned_data.get('username')
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(request, f"{username}! Thanks for signing up with us! You are now logged in.")
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
        form = FormProfileTravelerUpdate2(request.POST, instance=request.user.profiletraveler)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            messages.success(request, "Expertise section has been updated")
            if request.POST['save'] == "next":
                return redirect('profile_update_traveler3')
            elif request.POST['save'] == "save":
                return redirect('profile_update_traveler')
    else:
        form = FormProfileTravelerUpdate2(instance=request.user.profiletraveler)

    context = {'form': form }
    return render(request, "app_user/profile_traveler2.html", context)


@login_required()
def profile_update_traveler3(request):

    if request.method == 'POST':
        form = FormProgram(request.POST, instance=request.user)
        form.clean()
        if form.is_valid():
            form.save()
            messages.success(request, "Programs section has been updated")
            if request.POST['save'] == "next":
                return redirect('app_main:home')
            elif request.POST['save'] == "save":
                return redirect('profile_update_traveler2')
        else:
            messages.warning(request, "Form is not valid!")
    else:

        form = FormProgram(instance=request.user)
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
            messages.success(request, "Basic section has been updated!")
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
        form = FormProfileHostUpdate2(request.POST, instance=request.user.profilehost)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            messages.success(request, "Interest section has been updated!")
            if request.POST['save'] == "next":
                return redirect('app_main:home')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host')
    else:
        form = FormProfileHostUpdate2(instance=request.user.profilehost)

    context = {'form': form}
    return render(request, "app_user/profile_host2.html", context)


@login_required()
def space_update_host(request, space_id):

    space = Space.objects.get(owner_id=space_id)
    if request.method == 'POST':
        form = FormSpace(request.POST, instance=space)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            messages.success(request, "Availability section has been updated!")
            if request.POST['save'] == "next":
                return redirect('app_main:home')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host2')
    else:
        form = FormSpace(instance=space)

    context = {'form': form}
    return render(request, "app_user/space_update_host.html", context)


class TravelerDetailView(DetailView):
    model = ProfileTraveler
    # context_object_name = 'Preview Profile'
    # queryset = ProfileTraveler.objects.all()


class HostDetailView(DetailView):
    model = ProfileHost
