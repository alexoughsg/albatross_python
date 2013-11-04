#!/usr/bin/env python
#title           : domain_processor.py
#description     : class to process 'domain' related messages
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.models import Region
from albatross.ms.services.domain_service import DomainService

class DomainProcessor():

    def __init__(self):
        pass


    def _create(self, domain, service):
        domain_id = domain['id']
        domain_name = domain['name']
        if 'parentdomainname' in domain:
            parent_name = domain['parentdomainname']
            parent_domain_id = service.find_by_name(parent_name)['id']
        else:
            parent_domain_id = None
        if 'networkdomain' in domain:
            network_domain = domain['networkdomain']
        else:
            network_domain = None
        service.create(domain_name, domain_id, parent_domain_id, network_domain)


    def _exist(self, domain, domain_list):
        for next_domain in domain_list:
            if domain['name'] == next_domain['name']:
                return True


    def _delete(self, domain, service):
        domain_name = domain['name']
        service.delete(domain_name, None)


    def sync(self):

        master_region = Region.objects.get(is_master=True)
        master_service = DomainService(master_region)
        master_domains = master_service.list()
        
        for slave_region in Region.objects.filter(is_master=False):

            slave_service = DomainService(slave_region)

            # create domains in the current slave
            for domain in master_domains:
                self._create(domain, slave_service)

            # delete domains not in master domain list
            slave_domains = slave_service.list()
            for domain in slave_domains:
                if self._exist(domain, master_domains) is None:
                    self._delete(domain, slave_service)


    def create(self, message):

        domain_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = DomainService(master_region)
        domain = master_service.find_by_id(domain_id)

        if domain is None:
            raise Exception, 'domain[%s] does not exist in the master' % (domain_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = DomainService(slave_region)
            self._create(domain, slave_service)


    def delete(self, message):

        domain_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = DomainService(master_region)
        domain = master_service.find_by_id(domain_id)
        self.sync()


    def update(self, message):

        domain_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = DomainService(master_region)
        domain = master_service.find_by_id(domain_id)

        if domain is None:
            raise Exception, 'domain[%s] does not exist in the master' % (domain_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = DomainService(slave_region)
            #self._update(domain, slave_service)

