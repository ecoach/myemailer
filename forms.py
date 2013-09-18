from django import forms
from django.conf import settings
from .models import Message, BCC_Query
#mydata = import_module(settings.MYDATA)
#Source1 = mydata.models.Source1

class Emailer_Bcc_Form(forms.Form):
    select_bcc = forms.ModelChoiceField(required=False, queryset=BCC_Query.objects.all().order_by('-id'))
    sql  = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'input-xxlarge'}))
    commit = forms.ChoiceField(widget=forms.RadioSelect, choices=(('0', 'Testing Query',), ('1', 'Save and Create New Query',)), initial=0)
    query_name = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))

    def __init__(self, *args, **kwargs):
        super(Emailer_Bcc_Form, self).__init__(*args, **kwargs)

class Emailer_Draft_Form(forms.Form):
    subject  = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))
    

class Emailer_Send_Form(forms.Form):
    message_name  = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    commit = forms.ChoiceField(widget=forms.RadioSelect, choices=(('0', 'Test run'), ('1', 'Send'), ('2', 'Save')), initial=0)

class Emailer_Archive_Form(forms.Form):
    email_message = forms.ModelChoiceField(required=True, queryset=Message.objects.all().order_by('-id'))
