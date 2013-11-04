#!/usr/bin/env python
#title           : domain_service.py
#description     : class to send 'domain' related job requests to its interface class
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.interfaces.domain_interface import DomainInterface
from base_service import BaseService

class DomainService(BaseService):
    
    def __init__(self, region):
        self.region = region
        self.interface = DomainInterface(region=region)


    def list(self):
        self.interface.login()
        domains = self.interface.list_domains()
        self.interface.logout()
        return domains


    def find_by_id(self, id):
        self.interface.login()
        domains = self.interface.list_domains()
        self.interface.logout()
        for domain in domains:
            if domain['id'] == id:
                return domain
        return None


    def find_by_name(self, name):
        self.interface.login()
        domains = self.interface.list_domains()
        self.interface.logout()
        for domain in domains:
            if domain['name'] == name:
                return domain
        return None


    def create(self, domain_name, domain_id, parent_domain_id, network_domain):
        
        # check if the given domain already exists in the current region
        domain = self.find_by_name(domain_name)
        if domain:
            print 'domain[%s] already exists in region[%s]' % (domain_name, self.region.name)
            return

        # now create the given domain in the current region
        self.interface.login()
        self.interface.create_domain(domain_name, parent_domain_id, domain_id, network_domain)
        self.interface.logout()
        print 'domain[%s] has been successfully created in region[%s]' % (domain_name, self.region.name)


    def delete(self, domain_name, clean_up):

        domain = self.find_by_name(domain_name)
        if domain is None:
            print 'domain[%s] does not exist in region[%s]' % (domain_name, self.region.name)
            return

        self.interface.login()
        res = self.interface.delete_domain(domain['id'], clean_up)

        job_id = res['jobid']
        
        try:
            job_result = self._query_asynch_job(job_id)
        except Exception, ex:
            self.interface.logout()
            raise Exception, ex

        self.interface.logout()
        print 'domain[%s] has been successfully deleted in region[%s]' % (domain_name, self.region.name)


