from django.shortcuts import render,redirect,HttpResponseRedirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import FormRegisterPerson,FormRegisterOrg
from django.contrib.auth.decorators import login_required
from .decorators import org_required,person_required



def ViewRegister(request):
    if request.method == 'POST':
        try:
            if request.POST.getlist('type') == ['person']:
                request.user.is_person = True
                # print(request.user.is_person)
                HttpResponseRedirect(reverse('register_person'))
            elif request.POST.getlist['type'] == ['org']:
                print(request.POST['type'])
                request.user.is_org = True
                HttpResponseRedirect(reverse('register_org'))
        except KeyError:
            messages.warning(request, "Please select one of types!")
        except TypeError:
            messages.warning(request, "Wrong type!")

    return render(request, 'app_user/register.html')


def ViewRegisterPerson(request):
    if request.method == 'POST':
        form = FormRegisterPerson(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} your account has been created! You are now ready to log in!")
            return redirect('login')
    else:
        form = FormRegisterPerson()
    return render(request, 'app_user/register_type.html', {'form': form})

def ViewRegisterOrg(request):
    if request.method == 'POST':
        form = FormRegisterOrg(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} your account has been created! You are now ready to log in!")
            return redirect('login')
    else:
        form = FormRegisterOrg()
    return render(request, 'app_user/register_type.html', {'form': form})

@login_required()
@person_required()
def ViewProfilePersonUpdate(request):
    pass


@login_required()
@org_required()
def ViewProfileOrgUpdate(request):
    pass


