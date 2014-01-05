from django.db import models
from django.db import connection, transaction
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.conf import settings
import django
if django.VERSION[1] > 3:
    from myauth.models import UserProfile as User
else:
    from django.contrib.auth.models import User as User


# Create your models here.

class BCC_Query(models.Model):
    name = models.CharField(max_length=100, blank=True)
    sql = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id) + '_' + self.name

    def id_name(self):
        return self.__unicode__()

    def is_valid(self):
        # what makes it valid?
        return True

    @classmethod
    def factory(self, pk):
        try:
            e_bcc = BCC_Query.objects.get(pk=pk) 
        except:
            e_bcc = BCC_Query() 
            e_bcc.save()
        return e_bcc
        
    @classmethod
    def copy(self, old, new):
        old.id = new.id # old becomes new
        old.save()
        return old

    def get_bcc(self):
        cursor = connection.cursor()
        try:
            query = self.sql
            res = cursor.execute(query)
            res = cursor.fetchall()
            if len(res) > 0:
                tup = list(zip(*res)[0])
                arr = []
                for i in tup:
                    arr.append(str(i + '@umich.edu'))
                ret = arr
            else:
                ret = []
        except:
            ret = 'sql error'
        return ret

class Message(models.Model):
    user = models.ForeignKey(User, to_field='username') 
    created = models.DateTimeField(auto_now=False,blank=True, null=True)
    sender = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    bcc_query = models.ForeignKey(BCC_Query)
    bcc = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)

    def is_valid(self):
        # what makes it valid? 
        return True

    def is_query_valid(self):
        # what makes it valid? 
        if self.bcc_query == None:
            return False
        return True

    def __unicode__(self):
        return str(self.id) + '_' + self.subject + '  (' + str(self.created) + ')'

    def get_name(self):
        return self.__unicode__()

    @classmethod
    def factory(self, user, pk):
        try:
            emailer = Message.objects.get(pk=pk)
        except:  
            e_bcc = BCC_Query.factory(pk=None)
            emailer = Message(user=user, bcc_query = e_bcc)
            emailer.save()
        return emailer

    @classmethod
    def copy(self, old, new):
        old.id = new.id # old becomes new
        old.user = new.user
        old.bcc_query = BCC_Query.copy(old.bcc_query, new.bcc_query)
        old.save()
        return old

    def send(self, username, action):
        # message settings
        if username == 'jtritz' or username == 'michelot' or username == 'jbrancho' or username == 'gshultz':
            #sentfrom = 'ecoach-help@umich.edu'
            sentfrom = settings.COACH_EMAIL
            #sendto = ['jtritz@umich.edu']
            sendto = [username+'@umich.edu']
            bcc = self.bcc_query.get_bcc()
            subject = self.subject 
            bodytext = 'html message'
            html_content = self.body
            # archive settings
            if action == '1':
                self.created = datetime.now()
            elif action == '2':
                self.created = None
            self.bcc = bcc
            self.sender = sentfrom
            self.to = sendto
            self.save() 
            # use the settings
            if action == '1': # send commit
                message = EmailMultiAlternatives(
                    subject, 
                    bodytext, 
                    sentfrom,
                    sendto, 
                    bcc, 
                    #headers = {'Reply-To': 'ecoach-help@umich.edu'}
                    headers = {'Reply-To': settings.COACH_EMAIL}
                )
                message.attach_alternative(html_content, "text/html")
                #message.attach_file(self.m_attached_filepath)
                try:
                    message.send()
                except:
                    pass # in development this needs to fail
            return True
        else:
            return False


