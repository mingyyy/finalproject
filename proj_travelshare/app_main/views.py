from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from app_user.models import ProfileTraveler,ProfileHost, Topic, User
from .models import Trip, Available
from django.views.generic import ListView
from .utils import CalendarTrip,CalendarAvail
from django.utils.safestring import mark_safe
import calendar
from django.conf import settings
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TripForm, TripDeleteForm, AvailableForm, AvailableDeleteForm


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
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarAvail(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    # def get_queryset(self):
    #     return Trip.objects.filter(user_id=self.kwargs['userid'])


class CalendarViewTrip(ListView):
    model = Trip
    template_name = 'app_main/calendar_trip.html'

    # def get_queryset(self):
    #     return Trip.objects.filter(user_id=self.kwargs['userid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarTrip(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarViewAvailable(ListView):
    model = Available
    template_name = 'app_main/calendar_available.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarAvail(d.year, d.month)

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
            return HttpResponseRedirect(reverse('app_main:calendar_trip',args=[request.user.id]))
        trip.user = request.user
        trip.save()
        try:
            if request.POST['confirm'] == 'confirm':
                trip.delete()
                messages.warning(request, "This trip has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_trip',args=[request.user.id]))
    context = {'form': form, "id": trip_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/trip.html',context)


@login_required
def available_new(request, available_id=None):
    instance = Available(user=request.user)
    form = AvailableForm(request.POST or None, instance=instance)
    form_confirm = AvailableDeleteForm(request.POST or None)

    if request.POST and form.is_valid():
        available = form.save(commit=False)
        if available.available_duration() is False:
            messages.warning(request, "Your start and end dates are not valid!")
            return HttpResponseRedirect(reverse('app_main:calendar_available', args=[request.user.id]))
        available.user = request.user
        available.save()
        try:
            if request.POST['confirm'] == 'confirm':
                available.delete()
                messages.warning(request, "This entry has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_available',args=[request.user.id]))
    context = {'form': form, "id": available_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/available.html',context)


@login_required
def available(request, available_id):
    instance = Available(user=request.user, id=available_id)
    # if available_id:
    #     instance = get_object_or_404(Trip, id=available_id)
    # else:
    #     instance = Available(user=request.user)
    form = AvailableForm(request.POST or None, instance=instance)
    form_confirm = AvailableDeleteForm(request.POST or None)

    if request.POST and form.is_valid():
        available = form.save(commit=False)
        if available.available_duration() is False:
            messages.warning(request, "Your start and end dates are not valid!")
            return HttpResponseRedirect(reverse('app_main:calendar_available', args=[request.user.id]))
        available.user = request.user
        available.save()
        try:
            if request.POST['confirm'] == 'confirm':
                available.delete()
                messages.warning(request, "This entry has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_available', args=[request.user.id]))
    context = {'form': form, "id": available_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/available.html', context)


def trip_list(request):
    trips = Trip.objects.all()
    context = {'trips': trips}

    return render(request, 'app_main/trip_list.html', context)


def available_list(request, sort_choice=None):
    '''
    1. sorting by start_date
    2. sorting by end_date
    3. sorting by host_id
    4. sorting by country

    '''
    if sort_choice == 1:
        available = Available.objects.all().order_by("start_date")
    elif sort_choice == 2:
        available = Available.objects.all().order_by("end_date")
    elif sort_choice == 3:
        available = Available.objects.all().order_by("user")
    else:
        available = Available.objects.all().order_by("start_date")

    context = {'available': available}

    return render(request, 'app_main/available_list.html', context)
