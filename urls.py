from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
    #url(r'^admin/', include(admin.site.urls)),

    # app urls
    url(r'^bcc/', login_required(bcc_view), name='bcc'),
    url(r'^draft/', login_required(draft_view), name='draft'),
    url(r'^send/', login_required(send_view), name='send'),
    url(r'^archive/', login_required(archive_view), name='archive'),
    url(r'^', login_required(archive_view), name='default'),

)


