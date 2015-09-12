from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from main.dlTerms import dlTerms
from main.eventForm import EventForm
from main.models import Event, Mlist, Chat
from datetime import datetime
import re
import random

def index(request):
    terms = dlTerms()

    deadline = request.POST['deadline'] if 'deadline' in request.POST else None
    dlDate = request.POST['hour'] if 'hour' in request.POST else None
    dlHour = request.POST['hour'] if 'hour' in request.POST else None
    dlMin = request.POST['min'] if 'min' in request.POST else None
    message = request.POST['message'] if 'message' in request.POST else None
    lat = request.POST['lat'] if 'lat' in request.POST else None
    lng = request.POST['lng'] if 'lng' in request.POST else None

    if 'targets' in request.POST:
        targets = request.POST.getList('targets')
    else:
        targets = None;

    if 'term' in request.POST:
        terms.selectMin(request.POST['term'])
    
    context = {
        'deadline': deadline,
        'dlDate'  : dlDate,
        'dlHour'  : dlHour,
        'dlMin'   : dlMin,
        'terms'   : terms.items,
        'message' : message,
        'lat'     : lat,
        'lng'     : lng,
        'targets' : targets,
    }
    return render(request, 'main/index.html', context)

def confirm(request):
    terms = dlTerms()
    form = EventForm(request.POST)

    lat = form['lat'].value()
    lng = form['lng'].value()
    term = form['term'].value()
    dlTerm = terms.getVal(term)
    message = form['message'].value()
    targets = form['targets'].value()
    
    date = request.POST['dlDate'] if 'dlDate' in request.POST else None
    hour = request.POST['dlHour'] if 'dlHour' in request.POST else None
    min = request.POST['dlMin'] if 'dlMin' in request.POST else None
    deadline = date + ' ' + hour + ':' + min if hour != '-1' else date


    context = {
        'deadline': deadline,
        'dlTerm'  : dlTerm,
        'term'    : term,
        'message' : message,
         'lat'     : lat,
        'lng'     : lng,
        'targets' : targets,
        'form' : form
    }
    return render(request, 'main/confirm.html', context)

def regist(request):
    form = EventForm(request.POST)
    event = Event(lat=form['lat'].value(),lng=form['lng'].value())
    event.message = form['message'].value()
    event.term = form['term'].value()
    event.deadline = form['dlDate'].value()
    event.identifier = randStr(20)    
    event.save()

    return HttpResponseRedirect('/main/event/' + event.identifier)

def randStr(size):
    seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLKMNOPQRSTUVWXYZ0123456789%#$@"
    ret = ""
    for i in range(size):
        ret += random.choice(seed)
    return ret
    
def event(request, event_id):
    event = get_object_or_404(Event, identifier = event_id)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    context = {
        'lat' : event.lat,
        'lng' :event.lng,
        'deadline': event.deadline,
        'message' : event.message
    }
    return render(request, 'main/event.html', context)


