from django.shortcuts import render
#from django.http import HttpResponse
##from django.template import RequestContext, loader

def index(request):
    context = { 'hoge': 'HOGEHOGE' }
    return render(request, 'main/index.html', context);

#    template = loader.get_template('main/index.html')
#    context = RequestContext(request, {
#        'hoge' : 'HOGEHOGE'
#    })
#    return HttpResponse(template.render(context))

def confirm(request):
    return HttpResponse("Confirm")

def regist(request):
    return HttpResponse("Regist")

def event(request, event_id):
    return HttpResponse("Event %s" % event_id)

