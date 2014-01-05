from django.contrib.admin.views.decorators import staff_member_required
#from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .models import Message, BCC_Query
from .steps import steps_nav
from .forms import (
    Emailer_Bcc_Form,
    Emailer_Draft_Form,
    Emailer_Send_Form,
    Emailer_Archive_Form
    )
from django.shortcuts import redirect

import django
if django.VERSION[1] > 3:
    from mynav.mycoach_nav import main_nav, tasks_nav
else:
    from mynav.nav import main_nav, tasks_nav

@staff_member_required
def bcc_view(request):
    emailer = task_object(request.user)
    if request.method == 'POST':
        form = Emailer_Bcc_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_select_bcc = form.cleaned_data['select_bcc']
            if request.user.username == 'jtritz':
                f_sql = form.cleaned_data['sql']
            else:
                f_sql = emailer.bcc_query.sql
            f_qname = form.cleaned_data['query_name']
            f_commit = form.cleaned_data['commit']
            emailer.bcc_query.name = f_qname
            emailer.bcc_query.sql = f_sql
            emailer.bcc_query.save()
            if f_commit == '1':
                # create new bcc query
                emailer.bcc_query = BCC_Query.factory(pk=None)
            elif f_select_bcc != emailer.bcc_query:
                # copy and old bcc query
                emailer.bcc_query = BCC_Query.copy(f_select_bcc, emailer.bcc_query)
            emailer.save()
            #return redirect('email_bcc_view')
    form = Emailer_Bcc_Form(initial={
        'select_bcc' : emailer.bcc_query.id, 
        'query_name': emailer.bcc_query.name, 
        'sql': emailer.bcc_query.sql, 
        'commit': 0
    })

    return render(request, 'myemailer/bcc.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'emailer'),
        "steps_nav": steps_nav(request.user, 'bcc'),
        "form": form,
        "args": request.GET,
        "active_bcc_query": emailer.bcc_query.id_name(),
        "bcc_query_result": emailer.bcc_query.get_bcc()
    })

@staff_member_required
def draft_view(request):
    emailer = task_object(request.user)
    if request.method == 'POST':
        form = Emailer_Draft_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_subject = form.cleaned_data['subject']
            f_body = form.cleaned_data['body']
            emailer.subject = f_subject
            emailer.body = f_body 
            emailer.save()
            #return redirect('email_draft_view')
    form = Emailer_Draft_Form(initial={
        'subject' : emailer.subject, 
        'body': emailer.body
    })

    return render(request, 'myemailer/draft.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'emailer'),
        "steps_nav": steps_nav(request.user, 'draft'),
        "form": form,
        "args": request.GET,
        "message_body": emailer.body,
        "message_subject": emailer.subject
    })

@staff_member_required
def send_view(request):
    emailer = task_object(request.user)
    if request.method == 'POST':
        form = Emailer_Send_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_name = form.cleaned_data['message_name']
            f_commit = form.cleaned_data['commit']
            emailer.save()
            if f_commit == '1' or f_commit == '2': # send commit
                # send the message
                if emailer.send(username=request.user.username, action=f_commit):
                    # make new emailer and save to prefs
                    emailer = Message.factory(user=request.user, pk=None)
                    if django.VERSION[1] > 3:
                        user.set_pref('email_message_pk', emailer.id)
                    else:
                        profile = request.user.get_profile()
                        prefs = profile.prefs
                        prefs['email_message_pk'] = emailer.id
                        profile.prefs = prefs
                        profile.save()
                    return redirect(reverse('myemailer:archive'))
            #return redirect('email_send_view')
    form = Emailer_Send_Form(initial={
    })

    return render(request, 'myemailer/send.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'emailer'),
        "steps_nav": steps_nav(request.user, 'send'),
        "form": form,
        "args": request.GET,
    })

@staff_member_required
def archive_view(request):
    #Log_Request(request)
    emailer = task_object(request.user)
    if request.method == 'POST':
        form = Emailer_Archive_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_select_message = form.cleaned_data['email_message']
            # Copy the selected emailer 
            emailer = Message.copy(f_select_message, emailer)
            emailer.save()
            #return redirect('email_archive_view')
    else:
        form = Emailer_Archive_Form()

    return render(request, 'myemailer/archive.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'emailer'),
        "steps_nav": steps_nav(request.user, 'archive'),
        "form": form,
        "args": request.GET,
        "emailer_name": emailer.get_name(),
        "emailer": emailer
    })

def task_object(user):
    # get the user's message object
    if django.VERSION[1] > 3:
        pk = user.get_pref('email_message_pk')
        emailer = Message.factory(user=user, pk=pk)
        user.set_pref('email_message_pk', emailer.id)
        return emailer
    else:
        profile = user.get_profile()
        prefs = profile.prefs
        try:
            pk=prefs["email_message_pk"]
        except:
            pk = None
        emailer = Message.factory(user=user, pk=pk)
        prefs['email_message_pk'] = emailer.id
        profile.prefs = prefs
        profile.save()
        return emailer
     

