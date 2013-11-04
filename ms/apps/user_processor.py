#!/usr/bin/env python
#title           : user_processor.py
#description     : class to process 'user' related messages
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from albatross.ms.models import Region
from albatross.ms.services.domain_service import DomainService
from albatross.ms.services.user_service import UserService

class UserProcessor():
    
    """
    {"status":"Completed","event":"USER.CREATE","entityuuid":"221477a0-016c-4cbe-b16b-d13f2df21f33","entity":"com.cloud.user.User","account":"4f9dfb2f-81f1-4487-a0e5-3e021ef030a7","user":"edda71c2-1cac-11e3-99c0-bc173ef2043d"}
    {"status":"Completed","event":"USER.DELETE","entityuuid":"b9a894d4-a50b-4b5b-8721-10d2fc016c01","entity":"com.cloud.user.User","account":"247128a3-9574-43c6-a46d-fff47537bf3d","user":"edda71c2-1cac-11e3-99c0-bc173ef2043d"}
    """
    
    def __init__(self):
        pass


    def _create(self, user, service, domain_service):
        user_name = user['username']
        password = ''
        if 'email' in user:
            email = user['email']
        else:
            email = None
        first_name = user['firstname']
        last_name = user['lastname']
        account_name = user['account']
        domain_id = domain_service.find_by_name(user['domain'])['id']
        timezone = None
        service.create(user_name, account_name, password, email, first_name, last_name, domain_id, timezone)


    def _exist(self, user, user_list):
        for next_user in user_list:
            if user['username'] == next_user['username'] and user['account'] == next_user['account']:
                return True


    def _delete(self, user, service):
        user_name = user['username']
        account_name = user['account']
        service.delete(user_name, account_name)


    def _enable(self, user, service):
        user_name = user['username']
        account_name = user['account']
        service.enable(user_name, account_name)


    def _disable(self, user, service):
        user_name = user['username']
        account_name = user['account']
        service.disable(user_name, account_name)


    def sync(self):

        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        master_users = master_service.list()
        
        for slave_region in Region.objects.filter(is_master=False):
            
            slave_domain_service = DomainService(slave_region)
            slave_service = UserService(slave_region)
            
            # create users in the current slave
            for user in master_users:
                self._create(user, slave_service, slave_domain_service)

            # delete users not in master user list
            slave_users = slave_service.list()
            for user in slave_users:
                if self._exist(user, master_users) is None:
                    self._delete(user, slave_service)


    def create(self, message):

        user_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        user = master_service.find_by_id(user_id)

        if user is None:
            raise Exception, 'user[%s] does not exist in the master' % (user_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = UserService(slave_region)
            slave_domain_service = DomainService(slave_region)
            self._create(user, slave_service, slave_domain_service)


    def delete(self, message):

        user_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        user = master_service.find_by_id(user_id)
        self.sync()


    def enable(self, message):

        user_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        user = master_service.find_by_id(user_id)

        if user is None:
            raise Exception, 'user[%s] does not exist in the master' % (user_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = UserService(slave_region)
            self._enable(user, slave_service)


    def disable(self, message):

        user_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        user = master_service.find_by_id(user_id)

        if user is None:
            raise Exception, 'user[%s] does not exist in the master' % (user_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = UserService(slave_region)
            self._disable(user, slave_service)


    def update(self, message):

        user_id = message['entityuuid']
        master_region = Region.objects.get(is_master=True)
        master_service = UserService(master_region)
        user = master_service.find_by_id(user_id)

        if user is None:
            raise Exception, 'user[%s] does not exist in the master' % (user_id)

        # now create domain in slaves
        for slave_region in Region.objects.filter(is_master=False):
            slave_service = UserService(slave_region)
            #self._update(user, slave_service)
