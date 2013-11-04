#!/usr/bin/env python
#title           : user_service.py
#description     : class to send 'user' related job requests to its interface class
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.interfaces.user_interface import UserInterface
from base_service import BaseService

class UserService(BaseService):
    
    def __init__(self, region):
        self.region = region
        self.interface = UserInterface(region=region)


    def list(self):
        self.interface.login()
        users = self.interface.list_users()
        self.interface.logout()
        return users


    def find_by_id(self, id):
        self.interface.login()
        users = self.interface.list_users()
        self.interface.logout()
        for user in users:
            if user['id'] == id:
                return user
        return None


    def find_by_name(self, user_name, account_name):
        self.interface.login()
        users = self.interface.list_users()
        self.interface.logout()
        for user in users:
            if user['username'] == user_name and user['account'] == account_name:
                return user
        return None


    def create(self, user_name, account_name, password, email, first_name, last_name, domain_id, timezone):
        
        # check if the user already exists
        user = self.find_by_name(user_name, account_name)
        if user:
            print 'user[%s] in account[%s] already exists in region[%s]' % (user_name, account_name, self.region.name)
            return

        # now create the given user in the current region
        self.interface.login()
        self.interface.create_user(user_name, password, email, first_name, last_name, account_name, domain_id, timezone)
        self.interface.logout()
        print 'user[%s] has been successfully created in region[%s]' % (user_name, self.region.name)


    def delete(self, user_name, account_name):

        user = self.find_by_name(user_name, account_name)
        if user is None:
            print 'user[%s] in account[%s] does not exist in region[%s]' % (user_name, account_name, self.region.name)
            return

        self.interface.login()
        self.interface.delete_user(user['id'])
        self.interface.logout()
        print 'user[%s] has been successfully deleted in region[%s]' % (user_name, self.region.name)


    def enable(self, user_name, account_name):

        user = self.find_by_name(user_name, account_name)
        if user is None:
            print 'user[%s] in account[%s] does not exist in region[%s]' % (user_name, account_name, self.region.name)
            return

        self.interface.login()
        self.interface.enable_user(user['id'])
        self.interface.logout()
        print 'user[%s] has been successfully enabled in region[%s]' % (user_name, self.region.name)


    def disable(self, user_name, account_name):

        user = self.find_by_name(user_name, account_name)
        if user is None:
            print 'user[%s] in account[%s] does not exist in region[%s]' % (user_name, account_name, self.region.name)
            return

        self.interface.login()
        res = self.interface.disable_user(user['id'])

        job_id = res['jobid']
        
        try:
            job_result = self._query_asynch_job(job_id)
        except Exception, ex:
            self.interface.logout()
            raise Exception, ex

        self.interface.logout()
        print 'user[%s] has been successfully disabled in region[%s]' % (user_name, self.region.name)
