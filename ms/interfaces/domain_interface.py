#!/usr/bin/env python
#title           : domain_interface.py
#description     : class to manage the 'domain' resources using cloudstack API
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from cloud_interface import CloudInterface

class DomainInterface(CloudInterface):
    
    #def __init__(self, api_host=None, api_root_url=None, logger=None, session_key=None, cookie=None):
    #    CloudInterface.__init__(self, api_host, api_root_url, logger, session_key, cookie)


    def list_domains(self, list_all=True):
        """
        command=listDomains&response=json&sessionkey=null&_=1362457544896
        """

        request_type = 'GET'
        params = {
            'command':'listDomains',
            'response':'json',
            'sessionkey':self.session_key
        }
        if list_all: params['listall'] = list_all
        
        #{ "listdomainsresponse" : { "count":2 ,"domain" : [  {"id":"45152a26-a2ce-11e2-8da9-28fb734f3313","name":"ROOT","level":0,"haschild":true,"path":"ROOT"}, {"id":"3d12e7d5-a528-4626-a423-d1e17024ff91","name":"Ough","level":1,"parentdomainid":"45152a26-a2ce-11e2-8da9-28fb734f3313","parentdomainname":"ROOT","haschild":false,"path":"ROOT/Ough"} ] } }
        return self._request(request_type, params, 'domain')


    def list_domain_children(self):
        """
        command=listDomainChildren&response=json&sessionkey=null&_=1362457544896
        """

        request_type = 'GET'
        params = {
            'command':'listDomainChildren',
            'response':'json',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params, 'domainchildren')


    def create_domain(self, name, parent_domain_id=None, domain_id=None, network_domain=None):
        """
        command=createDomain
        &response=json
        &sessionkey=WyKKl72c8fi1d6y%2Bp%2BQuDGxDnZg%3D
        &parentdomainid=b8683900-a486-11e2-8da9-28fb734f3313
        &name=Eldridge
        &_=1365892060259
        """
        
        request_type = 'GET'
        params = {
            'command':'createDomain',
            'name':name,
            'response':'json',
            'sessionkey':self.session_key
        }
        if parent_domain_id:    params['parentdomainid'] = parent_domain_id
        if domain_id:   params['domainid'] = domain_id
        if network_domain:  params['networkdomain'] = network_domain

        return self._request(request_type, params)


    def updateDomain(self):
        pass


    def delete_domain(self, domain_id, clean_up):

        request_type = 'GET'
        params = {
            'command':'deleteDomain',
            'id':domain_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        if clean_up:    params['cleanup'] = clean_up

        return self._request(request_type, params)
