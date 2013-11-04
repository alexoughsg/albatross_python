#!/usr/bin/env python
#title           : account_service.py
#description     : class to send 'account' related job requests to its interface class
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.interfaces.account_interface import AccountInterface
from base_service import BaseService

class AccountService(BaseService):
    
    def __init__(self, region):
        self.region = region
        self.interface = AccountInterface(region=region)


    def list(self):
        self.interface.login()
        accounts = self.interface.list_accounts()
        self.interface.logout()
        return accounts


    def find_by_id(self, id):
        self.interface.login()
        accounts = self.interface.list_accounts()
        self.interface.logout()
        for account in accounts:
            if account['id'] == id:
                return account
        return None


    def find_by_name(self, account_name, domain_name):
        self.interface.login()
        accounts = self.interface.list_accounts()
        self.interface.logout()
        for account in accounts:
            if account['name'] == account_name and account['domain'] == domain_name:
                return account
        return None


    def create(self, account_name, domain_name, user_name, password, email, first_name, last_name, account_type, domain_id, account_details, network_domain, timezone):
        
        # check if the given account already exists in the current region
        account = self.find_by_name(account_name, domain_name)
        if account:
            print 'account[%s] in domain[%s] already exists in region[%s]' % (account_name, domain_name, self.region.name)
            return

        # now create the given account in the current region
        self.interface.login()
        self.interface.create_account(user_name, password, email, first_name, last_name, account_type, domain_id, account_name, account_details, network_domain, timezone)
        self.interface.logout()
        print 'account[%s] has been successfully created in region[%s]' % (account_name, self.region.name)


    def delete(self, account_name, domain_name):

        account = self.find_by_name(account_name, domain_name)
        if account is None:
            print 'account[%s] in domain[%s] does not exist in region[%s]' % (account_name, domain_name, self.region.name)
            return

        self.interface.login()
        res = self.interface.delete_account(account['id'])

        job_id = res['jobid']
        
        try:
            job_result = self._query_asynch_job(job_id)
        except Exception, ex:
            self.interface.logout()
            raise Exception, ex

        self.interface.logout()
        print 'account[%s] has been successfully deleted in region[%s]' % (account_name, self.region.name)


    def enable(self, account_name, domain_name):
        
        # check if the given account already exists in the current region
        account = self.find_by_name(account_name, domain_name)
        if account is None:
            print 'account[%s] in domain[%s] does not exist in region[%s]' % (account_name, domain_name, self.region.name)
            return

        # now create the given account in the current region
        self.interface.login()
        self.interface.enable_account(account['id'])
        self.interface.logout()
        print 'account[%s] has been successfully enabled in region[%s]' % (account_name, self.region.name)


    def disable(self, account_name, domain_name, lock):

        account = self.find_by_name(account_name, domain_name)
        if account is None:
            print 'account[%s] in domain[%s] does not exist in region[%s]' % (account_name, domain_name, self.region.name)
            return

        self.interface.login()
        res = self.interface.disable_account(lock, account['id'])

        job_id = res['jobid']
        
        try:
            job_result = self._query_asynch_job(job_id)
        except Exception, ex:
            self.interface.logout()
            raise Exception, ex

        self.interface.logout()
        print 'account[%s] has been successfully disabled in region[%s]' % (account_name, self.region.name)


