from django.shortcuts import render

def index(request):
    context = { }
    return render(request, 'main/index.html', context);

def confirm(request):
    context = { }
    return render(request, 'main/confirm.html', context);

def regist(request):
    return HttpResponse("Regist")

def event(request, event_id):
    return HttpResponse("Event %s" % event_id)

