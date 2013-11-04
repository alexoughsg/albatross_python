#!/usr/bin/env python
#title           : base_service.py
#description     : the base class to send job requests to appropriate interface classes
#author          : Alex Ough
#date            : 2013-11-04
#version         : 0.1
#python_version  : 2.7.1
#==============================================================================

import time

class BaseService:
    
    def __init__(self):
        self.region = None
        self.interface = None


    def _query_asynch_job(self, job_id, project_id=None):

        job_status = 0
        wait_seconds = 10
        while job_status == 0:
            time.sleep(wait_seconds)
            res = self.interface.query_asynch_job(job_id, project_id)
            print res
            job_status = res['jobstatus']
 
        job_result = res['jobresult']
        if 'errorcode' in job_result:
            raise Exception, job_result['errortext']
 
        return job_result


