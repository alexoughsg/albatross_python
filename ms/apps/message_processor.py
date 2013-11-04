#!/usr/bin/env python
#title           : message_processor.py
#description     : class to process messages given by the event handler class by invoking appropriate processors
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

import time
import datetime
from django.utils import simplejson as json
from albatross.ms.models import EventLog
from albatross.ms.apps.domain_processor import DomainProcessor
from albatross.ms.apps.account_processor import AccountProcessor
from albatross.ms.apps.user_processor import UserProcessor

class MessageProcessor:
    
    EVENTS = [
              {'key':'management-server.ActionEvent.USER-CREATE.User.*', 'processor':'UserProcessor', 'method':'create'},
              {'key':'management-server.ActionEvent.USER-DISABLE.User.*', 'processor':'UserProcessor', 'method':'disable'},
              {'key':'management-server.ActionEvent.USER-UPDATE.User.*', 'processor':'UserProcessor', 'method':'update'},
              {'key':'management-server.ActionEvent.USER-ENABLE.User.*', 'processor':'UserProcessor', 'method':'enable'},
              {'key':'management-server.ActionEvent.USER-DELETE.User.*', 'processor':'UserProcessor', 'method':'delete'},
              #{'key':'management-server.ActionEvent.REGISTER-USER-KEY.*.*', 'processor':'UserProcessor'},
              {'key':'management-server.ActionEvent.ACCOUNT-CREATE.Account.*', 'processor':'AccountProcessor', 'method':'create'},
              {'key':'management-server.ActionEvent.ACCOUNT-UPDATE.*.*', 'processor':'AccountProcessor', 'method':'update'},
              {'key':'management-server.ActionEvent.ACCOUNT-DISABLE.Account.*', 'processor':'AccountProcessor', 'method':'disable'},
              {'key':'management-server.ActionEvent.ACCOUNT-ENABLE.*.*', 'processor':'AccountProcessor', 'method':'enable'},
              {'key':'management-server.ActionEvent.ACCOUNT-DELETE.Account.*', 'processor':'AccountProcessor', 'method':'delete'},
              #{'key':'management-server.ActionEvent.CONFIGURATION-VALUE-EDIT.Configuration.*', 'processor':'AccountProcessor'},   # account settings - remote.access.vpn.client.iprange
              {'key':'management-server.ActionEvent.DOMAIN-CREATE.Domain.*', 'processor':'DomainProcessor', 'method':'create'},
              {'key':'management-server.ActionEvent.DOMAIN-DELETE.Domain.*', 'processor':'DomainProcessor', 'method':'delete'},
              {'key':'management-server.ActionEvent.DOMAIN-UPDATE.Domain.*', 'processor':'DomainProcessor', 'method':'update'},
             ]
    

    def __init__(self):
        pass


    def find(self, key):
        for event in self.EVENTS:
            if event['key'] == key:
                return event
        return None


    def process(self):
        while True:
            event_logs = EventLog.objects.filter(processed_time=None)
            if event_logs.count() == 0: break
            self.process_event_logs(event_logs)



    def process_event_logs(self, event_logs):
        print 'There are %d event logs to process' % (event_logs.count())
        for event_log in event_logs:
            try:
                self.process_event_log(event_log)
            except Exception, ex:
                print ex


    def process_event_log(self, event_log):
        for event in self.EVENTS:
            if event['key'] != event_log.routing_key:   continue
            try:
                processor = eval(event['processor'])()
                method = getattr(processor, event['method'])
                method(json.loads(event_log.body))
                event_log.processed_time = datetime.datetime.now()
                event_log.result = True
                event_log.save()
            except Exception, ex:
                print ex
                event_log.processed_time = datetime.datetime.now()
                event_log.result = False
                event_log.message = '%s' % ex
                event_log.save()


