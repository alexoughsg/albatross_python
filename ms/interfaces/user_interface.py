#!/usr/bin/env python
#title           : user_interface.py
#description     : class to manage the 'user' resources using cloudstack API
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from cloud_interface import CloudInterface

class UserInterface(CloudInterface):
    
    def create_user(self, user_name, password, email, first_name, last_name, account_name, domain_id=None, timezone=None):

        request_type = 'POST'
        params = {
            'command':'createUser',
            'username':user_name,
            'password':password,
            'email':email,
            'firstname':first_name,
            'lastname':last_name,
            'account':account_name,
            'response':'json',
            'sessionkey':self.session_key
        }
        if domain_id:
            params['domainid'] = domain_id
        if timezone:
            params['timezone'] = timezone

        return self._request(request_type, params)


    def delete_user(self, user_id):

        request_type = 'GET'
        params = {
            'command':'deleteUser',
            'id':user_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params)


    def update_user(self, user_id, email=None, first_name=None, last_name=None, password=None, timezone=None, user_api_key=None, user_name=None, user_secret_key=None):

        request_type = 'GET'
        params = {
            'command':'updateUser',
            'id':user_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        if email:   params['email'] = email
        if first_name:  params['firstname'] = first_name
        if last_name:   params['lastname'] = last_name
        if password:    params['password'] = password
        if timezone:    params['timezone'] = timezone
        if user_api_key:    params['userapikey'] = user_api_key
        if user_name:   params['username'] = user_name
        if user_secret_key: params['usersecretkey'] = user_secret_key
        
        return self._request(request_type, params)


    def list_users(self):

        request_type = 'GET'
        params = {
            'command':'listUsers',
            'listAll':'true',
            'page':'1',
            'pagesize':'20',
            'response':'json',
            'sessionkey':self.session_key
        }
        
        """
        [{u'username': u'admin', u'account': u'admin', u'domainid': u'edda3b6c-1cac-11e3-99c0-bc173ef2043d', u'firstname': u'Admin', u'created': u'2013-09-13T09:44:40-0500', u'lastname': u'User', u'iscallerchilddomain': False, u'domain': u'ROOT', u'email': u'admin@mailprovider.com', u'secretkey': u'8I1ZAO08rsVaSOflFoPicyj3xlSwALA-DZRRrLKNLRrXeJBReXmSkn_DmNtbVOefvsmMAuHc65L8tej3GPrzDg', u'state': u'enabled', u'apikey': u'gPCacvhEZ_grKRrGfTzeXXj9q828lQVdXLypd5sr7x80M7mjg4zpoJPBfkpbKbc2kOwY7v6HH4w_8w7G-TrtWA', u'accounttype': 1, u'id': u'edda71c2-1cac-11e3-99c0-bc173ef2043d', u'isdefault': True, u'accountid': u'edda5994-1cac-11e3-99c0-bc173ef2043d'}, {u'username': u'second', u'account': u'admin', u'domainid': u'edda3b6c-1cac-11e3-99c0-bc173ef2043d', u'firstname': u'second', u'created': u'2013-09-23T15:31:19-0500', u'lastname': u'admin', u'iscallerchilddomain': False, u'domain': u'ROOT', u'email': u'a@a.com', u'state': u'enabled', u'accounttype': 1, u'id': u'4a8d80ab-b611-411d-bf0c-6276d6b2579d', u'isdefault': False, u'accountid': u'edda5994-1cac-11e3-99c0-bc173ef2043d'}, {u'username': u'alex', u'account': u'alex', u'domainid': u'edda3b6c-1cac-11e3-99c0-bc173ef2043d', u'firstname': u'alex', u'created': u'2013-09-24T13:48:07-0500', u'lastname': u'ough', u'iscallerchilddomain': False, u'domain': u'ROOT', u'email': u'alex.ough@sungard.com', u'state': u'enabled', u'accounttype': 0, u'id': u'8c015437-f341-4911-8e54-aff79dcfd649', u'isdefault': False, u'accountid': u'c56c6a4b-0c21-4c74-83ec-552f0e9133f9'}]
        """
        
        return self._request(request_type, params, 'user')


    def lock_user(self):
        pass


    def disable_user(self, user_id):

        request_type = 'GET'
        params = {
            'command':'disableUser',
            'id':user_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params)


    def enable_user(self, user_id):

        request_type = 'GET'
        params = {
            'command':'enableUser',
            'id':user_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params)


    def get_user(self):
        pass


    def register_user_keys(self):
        pass


