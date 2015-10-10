from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from main.models import Event, Mlist, Chat, EventForm, MlistForm
from datetime import datetime, timedelta
from django.utils.timezone import utc
from main.webmail import webmail
from django.db import transaction
import logging

def index(request):
    form = EventForm()
    form.full_clean()
    
    targets = []
    targets.append(MlistForm(auto_id = False))

    context = {
        'targets' : targets,
        'form'    : form,
    }
    return render(request, 'main/index.html', context)

@transaction.commit_manually
def regist(request):
    logger = logging.getLogger('main.views')

    commitFlg = True
    new_event = None
    wmail     = None
    form      = EventForm(request.POST)
    if form.is_valid():
        new_event = form.save()
        wmail = webmail(new_event)
    else:
        commitFlg = False
    
    targets = []
    for (i, mail) in enumerate(request.POST.getlist('mail')):
        if len(mail) == 0:
            continue
        
        target = MlistForm({'mail':mail, 'event':new_event.pk}, auto_id = False) if new_event else MlistForm({'mail':mail, 'event': None}, auto_id = False)
        
        if target.is_valid():
            target.save()
            wmail.add_to(mail)
        else:
            commitFlg = False
        targets.append(target)
    else:
        if len(targets) == 0:
            target = MlistForm({'mail': None, 'event': None}, auto_id = False)
            targets.append(target)
            commitFlg = False
        

    if not commitFlg or len(targets) == 0:
        transaction.rollback()
        return render(request, 'main/index.html', {
            'form'   : form,
            'targets': targets
        })

    transaction.commit()
    wmail.send()
    return HttpResponseRedirect('/main/event/' + new_event.identifier)
    
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



