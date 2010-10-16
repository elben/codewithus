import urllib
import urllib2
import sys
import time

from pprint import pprint

import git_event
import config

# user settings
REPO_DIR = "/Users/shira/codewithus"
USER_EMAIL = "jasontbradshaw@gmail.com"
SERVER_ADDRESS = "http://codewithus.heroku.com"

class Sender:
    """
    Sends an event to the specified remote server.
    """
    
    def __init__(self, server_name):
        self.server_name = server_name
        
        # basic info for our sender
        self.user_agent = "CodeWithUs Client"
        self.event_post_url = "/event"
    
    def send_event(self, event):
        """
        Sends our event to the server in a format it can understand.
        """
        
        # TODO: remove test printing
        print "Sending an event to the server..."
        print "kind:", event.kind
        print "user_email:", event.user_email
        print "time:", event.timestamp
        print "data:"
        pprint(event.data)
        
        # create the url parameters as a dict
        values = event.data
        values["email"] = event.user_email
        values["time"] = event.timestamp
        values["kind"] = event.kind
        
        # build the http request
        url = self.server_name + self.event_post_url
        data = urllib.urlencode(values)
            
        # build the request object and get the response data
        request = urllib2.Request(url, data)
        
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e
            return

def main(args=sys.argv):
    """
    Parse the args, create the event object, then send it to the server.
    """
    
    if len(args) < 2:
        print "ERROR: No event type specified."
        return
    
    # build events from the specified repository
    builder = git_event.EventBuilder(config.REPO_DIR, config.USER_EMAIL)
    
    # the type of event we're creating
    command = args[1]
    
    # switch on command type
    event = None
    if command == "push":
        event = builder.build_push()
    elif command == "commit":
        event = builder.build_commit()
    elif command == "branch":
        event = builder.build_branch()
    elif command == "checkout":
        event = builder.build_checkout()
    else:
        print "ERROR: Failed to recognize event type '" + command + "'."
        return
    
    # send our event to the server
    sender = Sender(config.SERVER_NAME)
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
