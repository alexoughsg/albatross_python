#!/usr/bin/env python
#title           : user_interface.py
#description     : the base class to provide login/logout to/from the management servers and manage cloudstack resources using cloudstack API
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

import httplib, urllib
from django.conf import settings
from django.utils import simplejson as json
from albatross.ms.models import Region

class CloudInterface:
    
    def __init__(self, api_host=None, api_root_url=None, region=None, logger=None, session_key=None, cookie=None):
        if region:
            self.server = region.host
            self.root_url = region.root_url
            self.user_name = region.user_name
            self.password = region.password
        else:
            self.server = api_host
            self.root_url = api_root_url
            self.user_name = None
            self.password = None
        self.logger = logger
        self.conn = httplib.HTTPConnection(self.server)
        self.session_key = session_key
        self.cookie = cookie
        self.account = None
        self.domain_id = None


    def login(self, user_name=None, password=None):
        """
        '{ "loginresponse" : { "timeout" : "1800", "sessionkey" : "GNUfHusIyEOsqpgFp/Q9O2zaRFQ=", "username" : "admin", "registered" : "false", "userid" : "813253a8-7c63-11e2-a26f-c9595fd30292", "lastname" : "User", "account" : "admin", "domainid" : "813221a8-7c63-11e2-a26f-c9595fd30292", "firstname" : "Admin", "type" : "1" } }'
        """

        if user_name is None:   user_name = self.user_name
        if password is None:    password = self.password

        request_type = 'POST'
        params = {
            'command':'login',
            #'domain':'/',
            'username':user_name,
            'password':password,
            'response':'json'
        }
        
        task_url = '%s?%s' % (self.root_url, urllib.urlencode(params))
        self.conn.request(request_type, task_url)
        response = self.conn.getresponse()
        content = response.read()
        #print content
        res = json.loads(content)['loginresponse']
        res['cookie'] = response.getheader('Set-Cookie')

        self.session_key = res['sessionkey']
        self.cookie = response.getheader('Set-Cookie')
        self.account = res['account']
        self.domain_id = res['domainid']
        
        user_details = {}
        user_details['user_name'] = res['username']
        user_details['user_id'] = res['userid']
        user_details['domain_id'] = self.domain_id
        user_details['type'] = res['type']
        user_details['first_name'] = res['firstname']
        user_details['last_name'] = res['lastname']
        user_details['session_key'] = self.session_key
        user_details['session_id'] = self.cookie
        user_details['admin_role'] = True
        user_details['manager_role'] = True
        user_details['developer_role'] = True
        user_details['auditor_role'] = False
        user_details['snt_code'] = 'sgns'
        
        return {'user_details':user_details}


    def _get_headers(self):
        if self.cookie is None:    raise Exception, "no cookie available"
        headers = {'content-type':'text/plain'}
        headers['cookie'] = self.cookie
        return headers


    def _request(self, request_type, params, ret_attr_name=None):
        headers = self._get_headers()
        task_url = '%s?%s' % (self.root_url, urllib.urlencode(params))
        self.conn.request(request_type, task_url, headers=headers)
        response = self.conn.getresponse()
        content = response.read()
        #print "######"
        #print content
        res_json = json.loads(content).values()[0]
        if 'errorcode' in res_json:
            raise Exception, res_json['errortext']
        if ret_attr_name:
            if ret_attr_name in res_json:
                return res_json[ret_attr_name]
            else:
                return []
        return res_json


    def logout(self):
        """
        '{ "logoutresponse" : { "description" : "success" } }'
        """
        
        request_type = 'GET'
        params = {
            'response':'json',
            'command':'logout',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params)


    def query_asynch_job(self, job_id, project_id=None):
        """
        command=queryAsyncJobResult
        &jobId=2888ed5d-a42f-49df-9297-a4945e46d3c8
        &response=json
        &sessionkey=KPqcTgDRRT9rNMJeH%2FUc2OdBhGQ%3D
        &projectid=dd19bac8-38a7-43ca-af9c-eca4f9e97e13&_=1365832471891
        """

        request_type = 'GET'
        params = {
            'command':'queryAsyncJobResult',
            'jobId':job_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        if project_id:  params['projectid'] = project_id

        return self._request(request_type, params)
