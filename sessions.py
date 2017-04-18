"""
This mod simulates the session id magangement from JSP. Everytime a new request
reaches the server, a new session id will be generated for the request handler 
to set it into cookies for future reference. 

It is basically a key-value store. 

This module will maintain the user_id, only available from successful login, 
to each session, while the authentication is done outside this module. 

The users of this module can query the following:
    * whether a specific http session exists;
    * whether there is a successful login associated with a session;
    * memo passed in at the same time of a successful login.

The users of this module can perform the following modification:
    * remove a session providing an id;
    * setting login and memo for a session;
    * clear login and memo for a session. 
"""

from uuid import uuid4

class Xavier(object):
    
    def __init__(self):
        self.rec = {}

    def generate(self):
        ret = str(uuid4())
        self.rec[ret] = (None, None)
        return ret
        
    def has_login(self, sid):
        return sid in self.rec and self.rec[sid][0]
    
    def put(self, sid, uid, memo):
        self.rec[sid] = (uid, memo)
    
    def get(self, sid):
        return self.rec[sid] if sid in self.rec else (None, None)
        
    def clear(self, sid):
        if sid in self.rec:
            self.rec[sid] = (None, None)
