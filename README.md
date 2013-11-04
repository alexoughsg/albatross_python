albatross.ms
============

Domain/Account/User Sync Up Among Multiple Regions in Cloudstack.

1. The First Apporach (albatross/ms)

	Master Slave Architecture
	: The manual changes are allowed only in one master management server, and those in other servers are either prohibited or discarded.

	models
		1. region.py : table to store login information for each region because the region table of cloudstack does NOT store the user/pass.
		2. event_log.py : works as a queue so that the 'event handler' just stores the event messages whenever it receives and the 'message processor' processes the stored messages sequentially. This way, both the event handler is not blocked and the messages are guaranteed to be processed in the same order compared to the messages being processed in threads, and the failed messages can be retried.

	interfaces
		1. cloud_interface.py : the base class to provide login/logout to/from the management servers and manage cloudstack resources using cloudstack API
		2. user_interface.py : class to manage the 'user'
		3. account_interface.py : class to manage the 'account'
		4. domain_interface.py : class to manage the 'domain'
	
	services
		1. base_service.py : the base class to send job requests to above interface classes
		2. user_service.py : class to send 'user' related job requests
		3. account_service.py : class to send 'account' related job requests
		4. domain_service.py : class to send 'domain' related job requests
	
	apps
		1. event_handler.py : queue subscriber that listens to the message queue and invokes the message handler method whenever it receives an event message
		2. message_processor.py : class to process messages given by the event handler class by invoking appropriate processors
		3. user_processor.py : class to process 'user' related messages
		4. account_processor.py : class to process 'account' related messages
		5. domain_processor.py : class to process 'domain' related messages
