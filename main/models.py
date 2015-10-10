from django.db import models
from django import forms
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from swampdragon.models import SelfPublishModel
from main.serializers import ChatSerializer
from django.forms.utils import ErrorList
from django.http.request import QueryDict
import random
import logging

HOUR_CHOICES = (
    ('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),
    ('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),
    ('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),
    ('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),
    ('20','20'),('21','21'),('22','22'),('23','23')
)
MIN_CHOICES = (
    ('00','00'),('05','05'),('10','10'),('15','15'),
    ('20','20'),('25','25'),('30','30'),('35','35'),
    ('40','40'),('45','45'),('50','50'),('55','55')
)
TERMS_CHOICES = (
    ('0', "ちょうど"),
    ('15', "15分"),
    ('30', '30分'),
    ('60', '1時間'),
    ('120', '2時間'),
    ('240', '4時間'),
    ('720', '半日'),
    ('1440', '終日')
)

class Event(models.Model):
    lat        = models.FloatField()
    lng        = models.FloatField()
    deadline   = models.DateTimeField(auto_now = False,auto_now_add = False)
    term       = models.IntegerField()
    identifier = models.CharField(max_length = 20)
    message    = models.TextField(max_length = 1500, blank = True)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.identifier;


    def getTermStr(self):
        selectedTerm = self.term
        for t in TERMS_CHOICES:
            if int(t[0]) == selectedTerm:
                return t[1] 
        return None
    

class Mlist(models.Model):
    event      = models.ForeignKey('Event')
    mail       = models.EmailField()
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.mail

class EventForm(ModelForm):
    class Meta:
        model   = Event
        fields  = ['lat','lng','identifier','message','deadline', 'term']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'Message'}),
        }

    validDate = {
        'required': u'日付を指定してください',
        'invalid': u'不正な入力されました'
    }
    
    dlDate = forms.CharField(max_length=10, required=True, error_messages=validDate)
    dlHour = forms.ChoiceField(choices=HOUR_CHOICES)
    dlMin  = forms.ChoiceField(choices=MIN_CHOICES)
    terms  = forms.ChoiceField(choices=TERMS_CHOICES)

    def __init__(self, *args, **kwargs):
        newPosts = QueryDict('', True)
        if len(args) > 0:
            posts = dict(args[0].items())

            if posts['dlDate'] and posts['dlHour'] and posts['dlMin']:
                posts['deadline'] = self.getDeadline(posts['dlDate'],posts['dlHour'], posts['dlMin'])

            if posts['terms']:
                posts['term'] = posts['terms']

            posts['identifier'] = self.randStr(20)

            newPosts.update(posts)
            super(EventForm, self).__init__((newPosts))
        else:
            super(EventForm, self).__init__(*args, **kwargs)
        
    def getTermStr(self):
        selectedTerm = self['terms'].value()
        for term in TERMS_CHOICES:
            if term[0] == selectedTerm:
                return term[1] 
        return None

    def getDeadline(self, fldDate, fldHour, fldMin):
        if fldHour and fldMin:
            return "{date} {hour}:{min}".format(**{
                'date': fldDate,
                'hour': fldHour,
                'min': fldMin
            })
        else:
            return fldDate.value()

    def formatDeadline(self, date, hour, min):
        return "{date} {hour}:{min}:00".format(
            **{
                'date': date,
                'hour': hour,
                'min' : min
            }
        )
        
    def randStr(self, size):
        seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLKMNOPQRSTUVWXYZ0123456789"
        ret = ""
        for i in range(size):
            ret += random.choice(seed)
        return ret
        
class MlistForm(ModelForm):
    class Meta:
        model = Mlist
        fields = ['event', 'mail']

    def __init__(self, *args, **kwargs):
        super(MlistForm, self).__init__(*args, **kwargs)
        self.fields['mail'].error_messages = {'required': u"通知先のメールアドレスを入力してください"}

class Chat(models.Model, SelfPublishModel):
    event = models.ForeignKey('Event')
    message = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)
    serializer_class = ChatSerializer

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at) + ':' + self.message

class Marker(SelfPublishModel):
    lat = models.FloatField
    lng = models.FloatField
    
