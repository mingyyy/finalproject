from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from app_user.models import ProfileTraveler,ProfileHost, Topic, User
from .models import Trip
from django.views.generic import TemplateView, ListView,UpdateView
from .utils import Calendar
from django.utils.safestring import mark_safe
import calendar
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TripForm, TripDeleteForm


def home(request):
    profile_t = ProfileTraveler.objects.all()
    profile_h = ProfileHost.objects.all()

    context = {'profile_t': profile_t, 'profile_h': profile_h}
    return render(request,'app_main/home.html', context)



def travelers(request):
    profile = ProfileTraveler.objects.all()

    # for p in profile:
    #     if p.user.type == '0':
    #         expertise = p.expertise.all()
    #         lan = p.languages.all()
    #     else:
    #         expertise = []
    #         lan = []
    context = {'profile': profile}
    return render(request,'app_main/travelers.html', context)


def hosts(request):
    profile = ProfileHost.objects.all()

    context = {'profile': profile}
    return render(request,'app_main/hosts.html', context)


class CalendarView(ListView):
    model = Trip
    template_name = 'app_main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(m):
    first = m.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(m):
    days_in_month = calendar.monthrange(m.year, m.month)[1]
    last = m.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()


@login_required
def trip(request, trip_id=None):
    instance = Trip(user=request.user)
    if trip_id:
        instance = get_object_or_404(Trip, id=trip_id)
    else:
        instance = Trip(user=request.user)

    form = TripForm(request.POST or None, instance=instance)
    form_confirm = TripDeleteForm(request.POST or None)

    if request.POST and form.is_valid():
        trip = form.save(commit=False)
        if trip.trip_duration() is False:
            messages.warning(request, "Your start and end dates are not valid!")
            return redirect('app_main:calendar')
        trip.user = request.user
        trip.save()
        try:
            if request.POST['confirm'] == 'confirm':
                trip.delete()
                messages.warning(request, "This trip has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar'))
    context = {'form': form, "id": trip_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/trip.html',context)


