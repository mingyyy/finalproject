from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from app_user.models import ProfileTraveler,ProfileHost, Topic, User
from .models import Trip, Available
from django.views.generic import ListView
from .utils import CalendarTrip,CalendarAvail, CalendarAvailPriv, CalendarTripPriv, CalendarTripTraveler
from django.utils.safestring import mark_safe
import calendar
from django.conf import settings
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TripForm, TripDeleteForm, AvailableForm, AvailableDeleteForm, EntryRequirementForm
import requests
import mimi


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


class CalendarViewTripPrivate(ListView):
    model = Trip
    template_name = 'app_main/calendar_trip_private.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarTripPriv(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True, user_id=self.kwargs['user_id'])
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarViewAvailablePrivate(ListView):
    model = Available
    template_name = 'app_main/calendar_available_private.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarAvailPriv(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, user_id=self.kwargs['user_id'])
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CalendarViewTripTraveler(ListView):
    model = Trip
    template_name = 'app_main/calendar_trip_traveler.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarTripTraveler(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, userid=self.kwargs['userid'])
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['traveler'] = ProfileTraveler.objects.get(user_id=self.kwargs['userid'])
        return context


class CalendarViewAvailableHost(ListView):
    model = Available
    template_name = 'app_main/calendar_available_host.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarAvailPriv(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, userid=self.kwargs['userid'])
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['host'] = ProfileHost.objects.get(user_id=self.kwargs['userid'])
        return context



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
            return HttpResponseRedirect(reverse('app_main:calendar_trip_private',args=[request.user.id]))
        trip.user = request.user
        trip.save()
        try:
            if request.POST['confirm'] == 'confirm':
                trip.delete()
                messages.warning(request, "This trip has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_trip_private',args=[request.user.id]))
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
            return HttpResponseRedirect(reverse('app_main:calendar_available_private', args=[request.user.id]))
        available.user = request.user
        available.save()
        try:
            if request.POST['confirm'] == 'confirm':
                available.delete()
                messages.warning(request, "This entry has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_available_private',args=[request.user.id]))
    context = {'form': form, "id": available_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/available.html',context)


@login_required
def available(request, available_id=None):
    instance = Available(user=request.user)
    if available_id:
        instance = get_object_or_404(Available, id=available_id)
    else:
        instance = Available(user=request.user)

    form = AvailableForm(request.POST or None, instance=instance)
    form_confirm = AvailableDeleteForm(request.POST or None)

    if request.POST and form.is_valid():
        available = form.save(commit=False)
        if available.available_duration() is False:
            messages.warning(request, "Your start and end dates are not valid!")
            return HttpResponseRedirect(reverse('app_main:calendar_available_private',args=[request.user.id]))
        available.user = request.user
        available.save()
        try:
            if request.POST['confirm'] == 'confirm':
                available.delete()
                messages.warning(request, "This trip has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('app_main:calendar_available_private',args=[request.user.id]))
    context = {'form': form, "id": available_id, 'form_confirm': form_confirm}
    return render(request, 'app_main/available.html',context)


def trip_list(request, sort_choice=None):
    '''
    1. sorting by start_date
    2. sorting by end_date
    3. sorting by destination
    4. sorting by traveler
    '''
    if request.method == "POST":
        sort_choice = request.POST['select']
        if sort_choice == '1' or None:
            trips = Trip.objects.all().order_by("start_date")
        elif sort_choice == '2':
            trips = Trip.objects.all().order_by("end_date")
        elif sort_choice == '3':
            trips = Trip.objects.all().order_by("destination")
        else:
            trips = Trip.objects.all().order_by("user")
    else:
        trips = Trip.objects.all().order_by('start_date')

    context = {'trips': trips, 'selected': sort_choice}
    return render(request, 'app_main/trip_list.html', context)


def available_list(request, sort_choice=None):
    '''
    1. sorting by start_date
    2. sorting by end_date
    3. sorting by host_id
    4. sorting by country
    '''
    if request.method == "POST":
        sort_choice = request.POST['select']
        if sort_choice == '1' or None:
            available = Available.objects.all().order_by("start_date")
        elif sort_choice == '2':
            available = Available.objects.all().order_by("end_date")
        elif sort_choice == '3':
            available = Available.objects.all().order_by("user")
        else:
            available = Available.objects.all().order_by("summary")
    else:
        available = Available.objects.all().order_by('start_date')

    context = {'available': available, 'selected': sort_choice}
    return render(request, 'app_main/available_list.html', context)


def info(request):
    # TODO: only if request.GET['get_visa_info']==['Submit']
    # print(request.GET)

    form = EntryRequirementForm(request.GET or None)
    # default requirement = Unkown, citizenship is US, destination is Vietnam
    lan = "en"
    cs = "US"
    d = "VN"
    requirement, portrestriction, allowedstay, type = "Unknown", "Unknown", "Unknown", "Unknown"
    passport_validity, password_blank_pages = "Unknown", "Unknown"
    country_name, country_call_code, country_capital, country_timezone, country_population = \
        "Unknown", "Unknown", "Unknown","Unknown","Unknown"
    weather_temp,weather_temp_min,weather_temp_max, weather_humidity="Unknown", "Unknown", "Unknown", "Unknown"
    ccy_arrival, ccy_exit = "Unknown","Unknown"
    textual=[]
    if request.GET:
        cs = request.GET["citizenship"]
        d = request.GET["destination"]
        # messages.success(request, f"You are from {cs} and going to visit {d}.")
    else:
        form = EntryRequirementForm()

    if cs == d:
        requirement = "NOT_REQUIRED"
        portrestriction = "None"
        allowedstay = "Unlimited"
        type = "Citizenship"
        passport_validity, password_blank_pages = "None", "None"
        ccy_arrival, ccy_exit = "Unlimited", "Unlimited"
        textual = ["Probably you don't need a visa to visit your country."]
    else:
        # try:
        #     if request.GET['get_visa_info'] == ['Submit']:
        url = "https://requirements-api.sandbox.joinsherpa.com/v2/entry-requirements"
        querystring = {"citizenship": cs, "destination": d, "language": lan,
                       "key": mimi.SHERPA_API_KEY}
        headers = {'accept': '*/*'}
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            visa_info=response.json()
            for k, v in visa_info.items():
                if k == "visa":
                    for key, value in v[0].items():
                        print(key)
                        if key == "requirement":
                            requirement = value
                        elif key == "allowedStay":
                            allowedstay= value
                        elif key == "portRestriction":
                            portrestriction = value
                        elif key == "type":
                            type = value
                        elif key == "textual":
                            for x in value["text"]:
                                textual.append(x)
                if k == "passport":
                    passport_validity = v["passport_validity"]
                    password_blank_pages = v["blank_pages"]
                if k == "currency":
                    ccy_exit = v["exit"]
                    ccy_arrival = v["arrival"]
                # if k == "vaccination":
        except:
            messages.warning(request, "Sorry, visa requirement to this country is not available at the moment.")
        # except:
        #     pass
    # if request.GET['get_country_info'] == ['Submit']:
    try:
        country_info = requests.get(f"https://restcountries.eu/rest/v2/alpha/{d}").json()
        for k, v in country_info.items():
            if k == "name":
                country_name = v
            elif k == "callingCodes":
                country_call_code = v[0]
            elif k == "capital":
                country_capital = v
            elif k == "population":
                country_population = v
            elif k == "timezones":
                country_timezone = v[0]
    except:
        messages.warning(request, f"Sorry, there is no country info for {d}.")
    weather_desc = []

    try:
        path = f"https://api.openweathermap.org/data/2.5/weather?q={country_capital}&units=metric&appid={mimi.OPEN_WEATHER_API}"
        weather_info = requests.get(path).json()
        for k, v in weather_info.items():
            if k == "weather":
                for x in v:
                    weather_desc.append(x["main"])
            if k == "main":
                weather_temp = v["temp"]
                weather_temp_min = v["temp_min"]
                weather_temp_max = v["temp_max"]
                weather_humidity = v["humidity"]
    except:
        messages.warning(request, "Sorry, there is no weather info for this city.")

    context = {"form": form, "requirement": requirement, "allowedstay": allowedstay,
               "portrestriction": portrestriction,"type": type, "textual": textual,
               "country_name": country_name, "country_call_code": country_call_code,
               "country_capital": country_capital, "country_population": country_population,
               "country_timezone": country_timezone, "passport_validity": passport_validity,
               "passport_blank_pages": password_blank_pages,"currency_exit": ccy_exit,
               "currency_arrival": ccy_arrival, "weather_desc": weather_desc, "weather_temp": weather_temp,
               "weather_temp_min": weather_temp_min, "weather_temp_max": weather_temp_max,
               "weather_humidity": weather_humidity}
    return render(request, "app_main/info.html", context)


def get_country_info(request, d):
    try:
        country_info = requests.get(f"https://restcountries.eu/rest/v2/alpha/{d}").json()
        for k, v in country_info.items():
            if k == "name":
                country_name = v
            elif k == "callingCodes":
                country_call_code = v[0]
            elif k == "capital":
                country_capital = v
            elif k == "population":
                country_population = v
            elif k == "timezones":
                country_timezone = v[0]
    except:
        messages.warning(request, f"Sorry, there is no country info for {d}.")
    context_country = { "country_name": country_name, "country_call_code": country_call_code,
               "country_capital": country_capital, "country_population": country_population,
               "country_timezone": country_timezone,}
    return context_country


def get_weather_info(request, country_capital):
    weather_desc = []
    try:
        path = f"https://api.openweathermap.org/data/2.5/weather?q={country_capital}&units=metric&appid={mimi.OPEN_WEATHER_API}"
        weather_info = requests.get(path).json()
        for k, v in weather_info.items():
            if k == "weather":
                for x in v:
                    weather_desc.append(x["main"])
            if k == "main":
                weather_temp = v["temp"]
                weather_temp_min = v["temp_min"]
                weather_temp_max = v["temp_max"]
                weather_humidity = v["humidity"]
    except:
        messages.warning(request, "Sorry, there is no weather info for this city.")

    context_weather = { "weather_desc": weather_desc, "weather_temp": weather_temp,
               "weather_temp_min": weather_temp_min, "weather_temp_max": weather_temp_max,
               "weather_humidity": weather_humidity}
    return context_weather


def trip_view(request, trip_id=None):
    # TODO to be continued

    trip = Trip.objects.get(id=trip_id)
    print(trip)

    profile = ProfileTraveler.objects.get(user_id=trip.user_id)

    context = {'trip': trip, "profile": profile}
    return render(request, 'app_main/trip_view.html',context)
