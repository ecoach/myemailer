from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from mycoach4 import settings
from myemailer.views import *


urlpatterns = patterns('',
    url(r'^', login_required(email_bcc_view), name='email_bcc_view'),
    #url(r'^email_students/bcc/', login_required(email_bcc_view), name='email_bcc_view'),
    #url(r'^email_students/draft/', login_required(email_draft_view), name='email_draft_view'),
    #url(r'^email_students/send/', login_required(email_send_view), name='email_send_view'),
    #url(r'^email_students/archive/', login_required(email_archive_view), name='email_archive_view'),
    #url(r'^email_students/', login_required(email_bcc_view), name='email_bcc_view'),
)
