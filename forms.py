from django import forms
from mydata3.models import W_13Data
from myemailer.models import Message, BCC_Query
from datetime import datetime

class Emailer_Bcc_Form(forms.Form):
    select_bcc = forms.ModelChoiceField(required=False, queryset=BCC_Query.objects.all().order_by('-id'))
    sql  = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 70, 'rows': 25}))
    commit = forms.ChoiceField(widget=forms.RadioSelect, choices=(('0', 'Testing Query',), ('1', 'Save and Create New Query',)), initial=0)
    query_name = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))

    def __init__(self, *args, **kwargs):
        super(Emailer_Bcc_Form, self).__init__(*args, **kwargs)

class Emailer_Draft_Form(forms.Form):
    subject  = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 1}))
    body = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 25}))
    

class Emailer_Send_Form(forms.Form):
    message_name  = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    commit = forms.ChoiceField(widget=forms.RadioSelect, choices=(('0', 'Test run',), ('1', 'Commit',)), initial=0)

class Emailer_Archive_Form(forms.Form):
    email_message = forms.ModelChoiceField(required=True, queryset=Message.objects.all().order_by('-id'))
