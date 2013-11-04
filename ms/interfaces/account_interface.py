#!/usr/bin/env python
#title           : account_interface.py
#description     : class to manage the 'account' resources using cloudstack API
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

from cloud_interface import CloudInterface

class AccountInterface(CloudInterface):
    
    def list_accounts(self, domain_id=None):
        """
        command=listAccounts&response=json&sessionkey=XxjzeJWHV3S%2Brwq2m2EsYTSIYNE%3D&listAll=true&page=1&pagesize=20&_=1362457447296
        """

        request_type = 'GET'
        params = {
            'command':'listAccounts',
            'listAll':'true',
            'page':'1',
            'pagesize':'20',
            'response':'json',
            'sessionkey':self.session_key
        }
        if domain_id: params['domainId'] = domain_id
        
        res = self._request(request_type, params, 'account')
        if len(res) == 0:   return res

        if not domain_id:   return res
        
        #print res
        accounts = []
        for account in res:
            if account['domainid'] != domain_id:    continue
            accounts.append(account)
        return accounts


    def create_account(self, user_name, password, email, first_name, last_name, account_type, domain_id=None, account_name=None, account_details=None, network_domain=None, timezone=None):
        """
        command=createAccount&response=json&sessionkey=WyKKl72c8fi1d6y%2Bp%2BQuDGxDnZg%3D
            response
            sessionkey
            username
            email
            command
            account
            lastname
            accounttype    # User : "0"
            domainid
            firstname
            password
        """
        
        request_type = 'POST'
        params = {
            'command':'createAccount',
            'username':user_name,
            'password':password,
            'email':email,
            'accounttype':account_type,
            'firstname':first_name,
            'lastname':last_name,
            'response':'json',
            'sessionkey':self.session_key
        }
        
        if account_name: params['account'] = account_name
        if domain_id:   params['domainid'] = domain_id
        if account_details: params['accountdetails'] = account_details
        if network_domain:  params['networkdomain'] = network_domain
        if timezone:    params['timezone'] = timezone

        return self._request(request_type, params)


    def updateAccount(self):
        pass


    def delete_account(self, account_id):

        request_type = 'GET'
        params = {
            'command':'deleteAccount',
            'id':account_id,
            'response':'json',
            'sessionkey':self.session_key
        }
        
        return self._request(request_type, params)


    def disable_account(self, lock, account_id=None, account_name=None, domain_id=None):

        request_type = 'GET'
        params = {
            'command':'disableAccount',
            'lock':lock,
            'response':'json',
            'sessionkey':self.session_key
        }
        if account_id:  params['id'] = account_id
        if account_name:  params['name'] = account_name
        if domain_id:  params['domainid'] = domain_id
        
        return self._request(request_type, params)


    def enable_account(self, account_id=None, account_name=None, domain_id=None):

        request_type = 'GET'
        params = {
            'command':'enableAccount',
            'response':'json',
            'sessionkey':self.session_key
        }
        if account_id:  params['id'] = account_id
        if account_name:  params['name'] = account_name
        if domain_id:  params['domainid'] = domain_id
        
        return self._request(request_type, params)


    def lockAccount(self):
        pass


    def markDefaultZoneForAccount(self):
        pass


    def addAccountToProject(self):
        pass


    def deleteAccountFromProject(self):
        pass


    def listProjectAccounts(self):
        pass


