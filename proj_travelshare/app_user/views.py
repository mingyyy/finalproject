from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import FormRegister
from django.contrib.auth.decorators import login_required
from .decorators import org_required,person_required


def viewregister(request):
    print(request.POST)
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
@person_required()
def ViewProfilePersonUpdate(request):
    pass


@login_required()
@org_required()
def ViewProfileOrgUpdate(request):
    pass


