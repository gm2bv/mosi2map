from django.db import models

class Event(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    deadline = models.DateTimeField(auto_now = False,auto_now_add = False)
    term = models.IntegerField(null = True)
    identifier = models.CharField(max_length = 20)
    message = models.CharField(max_length = 1500, blank = True)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return str(self.lat) + ' ' + str(self.lng)


class Mlist(models.Model):
    event = models.ForeignKey('Event')
    mail = models.EmailField()
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.mail


class Chat(models.Model):
    event = models.ForeignKey('Event')
    message = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return str(self.created_at) + ':' + self.message


