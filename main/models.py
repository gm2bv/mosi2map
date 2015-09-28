from django.db import models
from django import forms
from django.forms import ModelForm
from swampdragon.models import SelfPublishModel
from main.serializers import ChatSerializer

HOUR_CHOICES = (
    ('-1', '--'),
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
    ('0', "--"),
    ('15', "15分"),
    ('30', '30分'),
    ('60', '1時間'),
    ('120', '2時間'),
    ('240', '4時間'),
    ('720', '半日'),
    ('1440', '終日')
)

class Event(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    deadline = models.DateTimeField(auto_now = False,auto_now_add = False,blank=True)
    term = models.IntegerField(blank = True)
    identifier = models.CharField(max_length = 20, blank=True)
    message = models.TextField(max_length = 1500, blank = True)
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
    event = models.ForeignKey('Event')
    mail = models.EmailField()
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.mail

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['lat','lng','deadline','term','identifier','message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'Message'}),
        }
    dlDate = forms.CharField(max_length=10)
    dlHour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    dlMin = forms.ChoiceField(choices=MIN_CHOICES, required=False)
    terms = forms.ChoiceField(choices=TERMS_CHOICES)

    def getTermStr(self):
        selectedTerm = self['terms'].value()
        for term in TERMS_CHOICES:
            if term[0] == selectedTerm:
                return term[1] 
        return None

    def getDeadline(self):
        if self['dlHour'].value() and self['dlMin'].value():
            return self['dlDate'].value() + ' ' + self['dlHour'].value() + ':' + self['dlMin'].value()
        else:
            return self['dlDate'].value()
        
class MlistForm(ModelForm):
    class Meta:
        model = Mlist
        fields = ['event', 'mail']

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
    
