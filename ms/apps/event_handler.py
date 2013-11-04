#!/usr/bin/env python
#title           : event_handler.py
#description     : queue subscriber that listens to the message queue and invokes the message handler method whenever it receives an event message
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

import pika
import datetime
from threading import Thread
from django.utils import simplejson as json
from albatross.ms.models import EventLog
from albatross.ms.apps.message_processor import MessageProcessor

class EventHandler():

    def __init__(self):
        
        message_processor = MessageProcessor()
        self.thread = Thread(target=message_processor.process, args=())
        self.thread.start()

        # Creates a connection to the RabbitMQ broker running on localhost
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        
        # Gets a channel to use for communicating with the broker
        channel = connection.channel()
        
        # Declares a new queue within the broker
        result = channel.queue_declare(exclusive=True)
        
        # Finds the auto-generated queue name to use when binding the queue
        # to the exchange
        queue_name = result.method.queue
        print 'Created Queue: ' + queue_name
        
        # Binds the queue to the cloudstack-events
        # exchange, with a wildcard routing key.
        # The wildcard key will cause all messages
        # sent to the exchange to be published to
        # your new queue.
        channel.queue_bind(exchange='cloudstack-events',
                           queue=queue_name,
                           #routing_key = '*.*.*.*.*')
                           routing_key = '*.ActionEvent.*.*.*')
        
        print ' [*] Waiting for logs. To exit press CTRL+C'

        # Tell the channel to use the callback
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        
        # And start consuming events!
        channel.start_consuming()


    # A simple callback method that will print
    # the routing_key and message body for any
    # message that it receives.
    def callback(self, ch, method, properties, body):
        #print ch, properties
        message_processor = MessageProcessor()
        try:
            body_json = json.loads(body)
            if message_processor.find(method.routing_key) and body_json['status'] == 'Completed':                    
                EventLog.Create(method.routing_key, body)
                print "message received => %r:%r" % (method.routing_key, body)
                # start a thread to process the event logs
                if self.thread is None or not self.thread.isAlive():
                    self.thread = Thread(target=message_processor.process, args=())
                    self.thread.start()
            else:
                print "[skipped] %r:%r" % (method.routing_key, body)
        except Exception, ex:
            print ex
            pass

    
    
if __name__ == '__main__':

    event_handler = EventHandler()
