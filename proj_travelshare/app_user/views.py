from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import FormRegister, FormUserUpdate, FormProfileTravelerUpdate, FormProfileHostUpdate
from django.contrib.auth.decorators import login_required
from .decorators import traveler_required, host_required


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

    print(request.user.profiletraveler)

    if request.method == 'POST':
        u_form = FormUserUpdate(request.POST, instance=request.user)
        t_form = FormProfileTravelerUpdate(request.POST,
                           request.FILES, instance=request.user.profiletraveler)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('home')
    else:
        u_form = FormUserUpdate(instance=request.user)
        t_form = FormProfileTravelerUpdate(instance=request.user.profiletraveler)

    context = {'u_form': u_form, 't_form': t_form}
    return render(request, "app_user/profile_traveler.html", context)


@login_required()
def profile_update_host(request):
    print(request.user.profilehost)

    if request.method == 'POST':
        u_form = FormUserUpdate(request.POST, instance=request.user)
        h_form = FormProfileHostUpdate(request.POST,
                           request.FILES, instance=request.user.profilehost)
        if u_form.is_valid() and h_form.is_valid():
            u_form.save()
            h_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('home')
    else:
        u_form = FormUserUpdate(instance=request.user)
        h_form = FormProfileHostUpdate(instance=request.user.profilehost)

    context = {'u_form': u_form, 't_form': h_form}
    return render(request, "app_user/profile_host.html", context)

