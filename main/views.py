from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from main.models import Event, Mlist, Chat, EventForm, MlistForm
from datetime import datetime, timedelta
from django.utils.timezone import utc
import re
import random

def index(request):
    form = EventForm()
    targets = []
    targets.append(MlistForm(auto_id = False))

    context = {
        'targets' : targets,
        'form'    : form,
    }
    return render(request, 'main/index.html', context)

def confirm(request):
    form = EventForm(request.POST)

    targets = []
    for mail in request.POST.getlist('mail'):
        targets.append(MlistForm({'mail':mail}, auto_id = False))
        
    context = {
        'form' : form,
        'targets': targets,
    }
    return render(request, 'main/confirm.html', context)

def regist(request):
    if 'cancel' in request.POST:        
        return HttpResponseRedirect('/main/')
    
    form = EventForm(request.POST)
    if not form.is_valid():
        print(form.errors)

    targets = []
    for mail in request.POST.getlist('mail'):
        target = MlistForm({'mail':mail}, auto_id = False)
        if not target.is_valid():
            print(target.errors)
        targets.append(target)
            
    new_event = form.save(commit=False)
    new_event.deadline = form.getDeadline()
    new_event.identifier = randStr(20)
    new_event.term = form['terms'].value()
    new_event.save()

    for mail in request.POST.getlist('mail'):
        target = MlistForm({'mail':mail, 'event':new_event.pk}, auto_id = False)
        target.save()
                    
    return HttpResponseRedirect('/main/event/' + new_event.identifier)

def randStr(size):
    seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLKMNOPQRSTUVWXYZ0123456789"
    ret = ""
    for i in range(size):
        ret += random.choice(seed)
    return ret
    
def event(request, event_id):
    try:
        event = get_object_or_404(Event, identifier = event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    targets = Mlist.objects.filter(event = event.pk)
    now = datetime.utcnow().replace(tzinfo=utc)
    is_live = True if event.deadline + timedelta(minutes = event.term) > now else False
    chats = Chat.objects.filter(event = event.pk) if not is_live else None

    context = {
        'event': event,
        'targets': targets,
        'is_live': is_live,
        'chats': chats,
    }
    return render(request, 'main/event.html', context)



