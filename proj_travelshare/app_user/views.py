from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from .forms import FormRegister, FormUserUpdate, FormProfileTravelerUpdate, FormProfileHostUpdate, \
    FormProfileHostUpdate2, FormProfileTravelerUpdate2, FormAddress, FormProgram, FormSpace, \
    DeleteProgramForm, DeleteSpaceForm
from django.contrib.auth.decorators import login_required
from .decorators import traveler_required, host_required
from django.views.generic import DetailView
from .models import ProfileTraveler, ProfileHost, Space, Program, Language
from django.contrib.auth import logout, login, authenticate


def viewregister(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            new_user=form.save()
            username = form.cleaned_data.get('username')
            type = form.cleaned_data.get('type')
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(request, f"{username}! Thanks for signing up with us! You are now logged in.")
            return redirect('index')
    else:
        form = FormRegister()
    return render(request, 'app_user/register.html', {'form': form})


@login_required()
def viewindex(request):
    return render(request, 'app_main/index.html')


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
                return redirect('app_main:index')
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
                return HttpResponseRedirect(reverse('program_add'))
            elif request.POST['save'] == "save":
                return redirect('profile_update_traveler')
    else:
        form = FormProfileTravelerUpdate2(instance=request.user.profiletraveler)

    context = {'form': form}
    return render(request, "app_user/profile_traveler2.html", context)


@login_required()
def program_add(request):
    if request.method != 'POST':
        form = FormProgram()
    else:
        form = FormProgram(request.POST, request.user)
        if form.is_valid():
            new_program = form.save(commit=False)
            new_program.owner = request.user
            form.clean()
            new_program.save()
            form.save_m2m()
            messages.success(request, "Program has been added!")
            if request.POST['save'] == "next":
                return HttpResponseRedirect(reverse('index'))
            elif request.POST['save'] == "save":
                return redirect('profile_update_traveler2')

    context = {'form': form}
    return render(request, 'app_user/program_add.html', context)


@login_required()
def program_update(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        form = FormProgram(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program has been updated!")
            if request.POST['save'] == "next":
                return HttpResponseRedirect(reverse("program_detail", args=[program.id]))
            elif request.POST['save'] == "save":
                return redirect('program_update')
        else:
            messages.warning(request, "Form is not valid!")
    else:
        form = FormProgram(instance=program)
    context = {'form': form, 'program': program}
    return render(request, "app_user/program_update.html", context)


@login_required
def program_delete(request, program_id):
    '''delete an existng program.'''
    program = Program.objects.get(id=program_id)
    program_to_delete = get_object_or_404(Program, id=program_id)
    if request.method != 'POST':
        form = DeleteProgramForm(instance=program)
    else:
        form = DeleteProgramForm(instance=program, data=request.POST)
        if form.is_valid():
            program_to_delete.delete()
            return HttpResponseRedirect(reverse('app_main:home'))
    context = {'program': program, 'form': form}
    return render(request, 'app_user/program_delete.html', context)


@login_required
def program_detail(request, program_id):
    '''show a program'''
    program = Program.objects.filter(owner=request.user).get(id=program_id)

    lan = program.languages.all()
    context = {"program": program, "lan": lan}

    return render(request, "app_user/program_detail.html", context)


def program_list(request, userid):
    '''show a program'''
    program = Program.objects.filter(owner_id=userid)

    context = {"program": program}
    return render(request, "app_user/program_list.html", context)


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
                return redirect('space_add')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host')
    else:
        form = FormProfileHostUpdate2(instance=request.user.profilehost)
    context = {'form': form}
    return render(request, "app_user/profile_host2.html", context)


@login_required()
def space_add(request):
    if request.method == 'POST':
        form = FormSpace(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            messages.success(request, "Availability has been added!")
            if request.POST['save'] == "next":
                return redirect('app_main:home')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host2')
    else:
        form = FormSpace()
    context = {'form': form}
    return render(request, "app_user/space_add.html", context)


@login_required()
def space_update(request, space_id):
    space = Space.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = FormSpace(request.POST, instance=space)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            messages.success(request, "Availability has been updated!")
            if request.POST['save'] == "next":
                return redirect('app_main:home')
            elif request.POST['save'] == "save":
                return redirect('profile_update_host2')
    else:
        form = FormSpace(instance=space)
    context = {'form': form}
    return render(request, "app_user/space_update.html", context)


@login_required
def space_detail(request, space_id):
    '''show a program'''
    space = Space.objects.filter(owner=request.user).get(id=space_id)
    context = {"space": space}
    return render(request, "app_user/space_detail.html", context)


def space_list(request, userid):
    '''show a program'''
    space = Space.objects.filter(owner_id=userid)
    context = {"space": space}
    return render(request, "app_user/space_list.html", context)


@login_required
def space_delete(request, space_id):
    '''delete an existng program.'''
    space = Space.objects.get(id=space_id)
    space_to_delete = get_object_or_404(Program, id=space_id)
    if request.method != 'POST':
        form = DeleteSpaceForm(instance=space)
    else:
        form = DeleteSpaceForm(instance=space, data=request.POST)
        if form.is_valid():
            space_to_delete.delete()
            return HttpResponseRedirect(reverse('app_main:home'))
    context = {'space': space, 'form': form}
    return render(request, 'app_user/space_delete.html', context)

@login_required
def links(request):
    return render(request, '')


def profile_traveler(request, userid):
    profile = ProfileTraveler.objects.get(user_id=userid)
    lan = profile.languages.all()
    context = {"profile": profile, 'lan': lan, }

    return render(request, 'app_user/preview_traveler.html', context)


def profile_host(request, userid):
    profile = ProfileHost.objects.get(id=userid)
    lan = profile.languages.all()
    interest = profile.interests.all()
    lat, lon = profile.geolocation.lat, profile.geolocation.lon

    context = {"profile": profile, 'lan': lan, 'interest': interest, 'lat': lat, 'lon': lon}

    return render(request, 'app_user/preview_host.html', context)


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
