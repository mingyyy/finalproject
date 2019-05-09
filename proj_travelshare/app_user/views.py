from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import FormRegister
from django.contrib.auth.decorators import login_required


def ViewRegister(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} your account has been created! You are now ready to log in!")
            return redirect('login')
    else:
        form = FormRegister()
    return render(request, 'app_user/register.html', {'form': form})


def ViewProfilePerson(request):
    pass


def ViewProfileOrg(request):
    pass