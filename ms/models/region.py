#!/usr/bin/env python
#title           : region.py
#description     : table to store login information for each region because the region table of cloudstack does NOT store the user/pass.
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from django.db import models

class Region(models.Model):

    # attributes    
    name = models.CharField(max_length=255, blank=False)
    host = models.CharField(max_length=255, blank=False)
    root_url = models.CharField(max_length=255, blank=False)
    user_name = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)
    is_master = models.BooleanField(default=False)

    # this is necessary for 'syncdb' to recognize this model
    class Meta:
        app_label = 'ms'

    # string representation of this asset
    def __unicode__(self):
        return "%s [%s]" %(self.name, self.host)


    @classmethod
    def Create(cls, name, end_point, user_name, password, is_master):

        region = Region()
        region.name = name
        region.host = host
        region.root_url = root_url
        region.user_name = user_name
        region.password = password
        region.is_master = is_master
        region.save()

        return region


    def to_json(self):
        res_json = {'id':self.id}
        res_json['name'] = self.name
        res_json['host'] = self.host
        res_json['root_url'] = self.root_url
        res_json['user_name'] = self.user_name
        res_json['password'] = self.password
        res_json['is_master'] = self.is_master
        
        return res_json
