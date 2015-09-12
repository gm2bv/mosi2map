from django import forms

class ArrayField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.base_type = kwargs.pop('base_type')
        self.widget = forms.MultipleHiddenInput
        super(ArrayField, self).__init__(*args, **kwargs)
    def clean(self, value):
        for subvalue in value:
            self.base_type.validate(subvalue)

        return [self.base_type.clean(subvalue) for subvalue in value]

class EventForm(forms.Form):
    """a form to describe an event to create newly.
    """

    lat = forms.FloatField()
    lng = forms.FloatField()
    dlDate = forms.CharField(max_length=10)
    dlHour = forms.ChoiceField()
    dlMin = forms.ChoiceField()
    term = forms.ChoiceField()
#    targets = forms.EmailField()
    targets = ArrayField(base_type=forms.EmailField())
    message = forms.CharField(max_length=2048)
    
