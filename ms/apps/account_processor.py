#!/usr/bin/env python
#title           : account_processor.py
#description     : class to process 'account' related messages
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.models import Region
from albatross.ms.services.domain_service import DomainService
from albatross.ms.services.account_service import AccountService

class AccountProcessor():
    
    def __init__(self):
        pass


    def _create(self, account, service, domain_service):
        user_name = account['user'][0]['username']
        password = ''
        if 'email' in account['user'][0]:
            email = account['user'][0]['email']
        else:
            email = None
        first_name = account['user'][0]['firstname']
        last_name = account['user'][0]['lastname']
        account_type = account['accounttype']
        domain_name = account['domain']
        domain_id = domain_service.find_by_name(account['domain'])['id']
        account_name = account['name']
        account_details = None
        network_domain = None
        timezone = None
        service.create(account_name, domain_name, user_name, password, email, first_name, last_name, account_type, domain_id, account_details, network_domain, timezone)


    def _exist(self, account, account_list):
        for next_account in account_list:
            if account['name'] == next_account['name'] and account['domain'] == next_account['domain']:
                return True


    def _delete(self, account, service):
        account_name = account['name']
        domain_name = account['domain']
        service.delete(account_name, domain_name)


    def _enable(self, account, service):
        account_name = account['name']
        domain_name = account['domain']
        service.enable(account_name, domain_name)


    def _disable(self, account, service):
        account_name = account['name']
        domain_name = account['domain']
        service.disable(account_name, domain_name, False)


    def sync(self):

        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        master_accounts = master_service.list()
        
        for slave_region in Region.objects.filter(is_master=False):

            slave_domain_service = DomainService(slave_region)
            slave_service = AccountService(slave_region)

            # create accounts in the current slave
            for account in master_accounts:
                self._create(account, slave_service, slave_domain_service)

            # delete accounts not in master account list
            slave_accounts = slave_service.list()
            for account in slave_accounts:
                if self._exist(account, master_accounts) is None:
                    self._delete(account, slave_service)


    def create(self, message):

        account_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        account = master_service.find_by_id(account_id)

        if account is None:
            raise Exception, 'account[%s] does not exist in the master' % (account_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = AccountService(slave_region)
            slave_domain_service = DomainService(slave_region)
            self._create(account, slave_service, slave_domain_service)


    def delete(self, message):

        account_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        account = master_service.find_by_id(account_id)
        self.sync()


    def enable(self, message):

        account_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        account = master_service.find_by_id(account_id)

        if account is None:
            raise Exception, 'account[%s] does not exist in the master' % (account_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = AccountService(slave_region)
            self._enable(account, slave_service)


    def disable(self, message):

        account_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        account = master_service.find_by_id(account_id)

        if account is None:
            raise Exception, 'account[%s] does not exist in the master' % (account_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = AccountService(slave_region)
            self._disable(account, slave_service)


    def update(self, message):

        account_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = AccountService(master_region)
        account = master_service.find_by_id(account_id)

        if account is None:
            raise Exception, 'account[%s] does not exist in the master' % (account_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = AccountService(slave_region)
            #self._create(account, slave_service)

