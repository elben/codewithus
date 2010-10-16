import urllib
import urllib2
import sys
import time

import git_event
import config

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
        
        # create the url parameters as a dict starting with the data
        # it already contains.
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
    
    # load our config file
    conf = config.load_config("~/codewithus.conf")
    
    # build events from the specified repository
    builder = git_event.EventBuilder(conf["repo_dir"], conf["user_email"])
    
    # the type of event we're creating
    command = args[1]
    
    # switch on command type
    event = None
    if command == "push":
        event = builder.build_push()
    elif command == "commit":
        event = builder.build_commit()
    elif command == "checkout":
        event = builder.build_checkout()
    elif command == "merge":
        event = builder.build_merge()
    elif command == "pull":
        event = builder.build_pull()
    else:
        print "ERROR: Failed to recognize event type '" + command + "'."
        return
    
    # send our event to the server
    sender = Sender(conf["server_name"])
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
