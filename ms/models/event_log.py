#!/usr/bin/env python
#title           : event_log.py
#description     : works as a queue so that the 'event handler' just stores the event messages whenever it receives and the 'message processor' processes the stored messages sequentially.
#                  This way, both the event handler is not blocked and the messages are guaranteed to be processed in the same order compared to the messages being processed in threads, and the failed messages can be retried.
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

import datetime
from django.db import models

class EventLog(models.Model):

    # attributes    
    routing_key = models.CharField(max_length=255, blank=False)
    body = models.CharField(max_length=255, blank=False)
    created_time = models.DateTimeField(blank=True, default=datetime.datetime.now(), null=True)
    processed_time = models.DateTimeField(blank=True, null=True)
    result = models.BooleanField(default=False)
    message = models.CharField(max_length=255, blank=True, null=True)

    # this is necessary for 'syncdb' to recognize this model
    class Meta:
        app_label = 'ms'

    # string representation of this asset
    def __unicode__(self):
        return "%s [%s]" %(self.routing_key, self.body)


    @classmethod
    def Create(cls, routing_key, body):

        event_log = EventLog()
        event_log.routing_key = routing_key
        event_log.body = body
        event_log.created_time = datetime.datetime.now()
        event_log.save()

        return event_log


    def to_json(self):
        res_json = {'id':self.id}
        res_json['routing_key'] = self.routing_key
        res_json['body'] = self.body
        res_json['created_time'] = self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        if self.processed_time:
            res_json['processed_time'] = self.processed_time.strftime("%Y-%m-%d %H:%M:%S")
            res_json['result'] = self.result
        else:
            res_json['processed_time'] = ''
            res_json['result'] = ''
        
        return res_json
