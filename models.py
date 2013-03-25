from django.db import models
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

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
            # update myemailer_bcc_query set myemailer_bcc_query.sql = concat("select user_id from mydata3_w_13data where ", myemailer_bcc_query.sql);
            # query = "select user_id from mydata3_w_13data where " + self.sql
            query = self.sql
            res = cursor.execute(query)
            res = cursor.fetchall()
            tup = list(zip(*res)[0])
            arr = []
            for i in tup:
                arr.append(str(i + '@umich.edu'))
            ret = arr
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
        if username == 'jtritz':
            sentfrom = 'ecoach-help@umich.edu'
            sendto = ['jtritz@umich.edu']
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
                    headers = {'Reply-To': 'ecoach-help@umich.edu'}
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


