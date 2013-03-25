#from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from mycoach3.nav import StaffNav, EmailerNav
from myemailer.models import Message, BCC_Query
from mycoach3.views import Log_Request
from myemailer.forms import (
    Emailer_Bcc_Form,
    Emailer_Draft_Form,
    Emailer_Send_Form,
    Emailer_Archive_Form
    )
from django.shortcuts import redirect

def email_bcc_view(request):
    Log_Request(request)

    # get the user's message object
    profile = request.user.get_profile()
    prefs = profile.prefs
    try:
        pk=prefs["email_message_pk"]
    except:
        pk = None
    emailer = Message.factory(user=request.user, pk=pk)
    prefs['email_message_pk'] = emailer.id
    profile.prefs = prefs
    profile.save()
    
    if request.method == 'POST':
        form = Emailer_Bcc_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_select_bcc = form.cleaned_data['select_bcc']
            f_sql = form.cleaned_data['sql']
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
            return redirect('email_bcc_view')
    else:
        form = Emailer_Bcc_Form(initial={
            'select_bcc' : emailer.bcc_query.id, 
            'query_name': emailer.bcc_query.name, 
            'sql': emailer.bcc_query.sql, 
            'commit': 0
        })

    return render(request, 'mycoach3/emailer_bcc.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_mailer": EmailerNav(request.path),
        "active_bcc_query": emailer.bcc_query.id_name(),
        "bcc_query_result": emailer.bcc_query.get_bcc()
    })

def email_draft_view(request):
    Log_Request(request)

    # get the user's message object
    profile = request.user.get_profile()
    prefs = profile.prefs
    try:
        pk=prefs["email_message_pk"]
    except:
        pk = None
    emailer = Message.factory(user=request.user, pk=pk)
    prefs['email_message_pk'] = emailer.id
    profile.prefs = prefs
    profile.save()

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
            return redirect('email_draft_view')
    else:
        form = Emailer_Draft_Form(initial={
            'subject' : emailer.subject, 
            'body': emailer.body
        })

    return render(request, 'mycoach3/emailer_draft.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_mailer": EmailerNav(request.path),
        "message_body": emailer.body,
        "message_subject": emailer.subject
    })

def email_send_view(request):
    Log_Request(request)

    # get the user's message object
    profile = request.user.get_profile()
    prefs = profile.prefs
    try:
        pk=prefs["email_message_pk"]
    except:
        pk = None
    emailer = Message.factory(user=request.user, pk=pk)
    prefs['email_message_pk'] = emailer.id
    profile.prefs = prefs
    profile.save()
 
    if request.method == 'POST':
        form = Emailer_Send_Form(
            data=request.POST
        )
        if form.is_valid():
            # process the form :)
            f_name = form.cleaned_data['message_name']
            f_commit = form.cleaned_data['commit']
            emailer.save()
            if f_commit == '1':
                # send the message
                emailer.send()
                # make new emailer and save to prefs
                profile = request.user.get_profile()
                prefs = profile.prefs
                emailer = Message.factory(user=request.user, pk=None)
                prefs['email_message_pk'] = emailer.id
                profile.prefs = prefs
                profile.save()
                return redirect('email_archive_view')
            return redirect('email_send_view')
    else:
        form = Emailer_Send_Form(initial={
        })

    return render(request, 'mycoach3/emailer_send.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_mailer": EmailerNav(request.path)
    })

def email_archive_view(request):
    Log_Request(request)

    # get the user's message object
    profile = request.user.get_profile()
    prefs = profile.prefs
    try:
        pk=prefs["email_message_pk"]
    except:
        pk = None
    emailer = Message.factory(user=request.user, pk=pk)
    prefs['email_message_pk'] = emailer.id
    profile.prefs = prefs
    profile.save()

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
            return redirect('email_archive_view')
    else:
        form = Emailer_Archive_Form()

    return render(request, 'mycoach3/emailer_archive.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_mailer": EmailerNav(request.path),
        "emailer_name": emailer.get_name(),
        "emailer": emailer
    })

