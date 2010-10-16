import sys
import time
import urllib
import urllib2
import json

import Growl

import config
import git_event

class Notifier:
    """
    Builds and displays a system notification.  Meant to be an
    abstraction from any platform-specific notification system (Growl,
    GNotify, Windows balloons, etc.).  This class acts as a default
    notification plugin in the case that there's no other compatible
    one installed.
    """
    
    def __init__(self, app_name):
        self.app_name = app_name
    
    def notify(self, title, message, icon_data=None):
        """
        Display a notification with the given title, message, and icon.
        """
        
        print "[" + title + "]"
        print message
        print

class GrowlNotifier(Notifier):
    """
    A notifier using Growl for OSX.
    """
    
    def __init__(self, app_name):
        
        # create and register the notification daemon
        self.growler = Growl.GrowlNotifier(app_name, ["git-event"])
        self.growler.register()
        
        Notifier.__init__(self, app_name)
    
    def notify(self, title, message, icon_data=None):
        """
        Show a Growl notification popup.
        """
        
        # get our Growl.Image if we got some icon data
        img = None
        if icon_data is not None and icon_data != "":
            img = Growl.Image.imageWithData(icon_data)
        
        self.growler.notify("git-event", title, message, icon=img)

class Poller:
    """
    Gets latest information from the specified server.
    """
    
    def __init__(self, server_name, user_email):
        self.server_name = server_name
        self.user_email = user_email
        
        self.subscription_url = "/feed"
        
    def poll(self):
        """
        Returns a list of event objects parsed from our subscriptions,
        sorted least-recent to most-recent.
        """
        
        # list of parsed events
        result = []
        
        # build the http 'get' request
        values = {
            "email": self.user_email,
            }
        
        url = self.server_name + self.subscription_url
        data = urllib.urlencode(values)
        
        # build the request object and get the response data
        request = urllib2.Request(url, data)
        
        try:
            response = urllib2.urlopen(request)
            
            # get raw JSON data
            rdata = response.read()
            
            # turn it into native data
            jdata = json.loads(rdata)
        except Exception, e:
            print e
            return
        
        # TODO: refactor this into the EventBuilder class in git_event
        for event in jdata["events"]:
            new_event = git_event.Event(event["kind"], event["time"],
                                        event["email"], event["data"],
                                        face_url=event["face_url"])
            result.append(new_event)
        
        return result

def main(args=sys.argv):
    
    # load our config file
    conf = config.load_config("~/codewithus.conf")
    
    # create our utility objects
    p = Poller(conf["server_name"], conf["user_email"])
    n = GrowlNotifier("CodeWithUs")
    
    # loop, polling for new notifications
    try:
        while 1:
            
            # ensure we get some iterable thing from the poll
            poll_data = p.poll()
            poll_data = [] if poll_data is None else poll_data
            
            # parse all the events and display them
            for event in poll_data:
                title = "Title"
                message = "Message!"
                
                if event.kind == "commit":
                    title = "Commit from %s:" % event.user_email
                    message = event.data["message"]
                elif event.kind == "push":
                    title = "Push from %s:" % event.user_email
                    message = "Pushed to a repository."
                elif event.kind == "checkout":
                    title = "Checkout from %s:" % event.user_email
                    message = "Currently in branch '%s'." % event.data["active_branch"]
                elif event.kind == "merge":
                    title = "Merge from %s:" % event.user_email
                    message = event.data["message"]
                elif event.kind == "pull":
                    title = "Pull from %s:" % event.user_email
                    message = "Pulled into branch '%s'." % event.data["active_branch"]
                
                # download the image file and save its data
                img_data = None
                try:
                    img_data = urllib.urlopen(event.face_url).read()
                except Exception, e:
                    # reset the image file if we failed somewhere
                    img_data = None
                    print e
                
                # display the notification
                n.notify(title, message, icon_data=img_data)
            
            # wait a bit before the next poll cycle
            time.sleep(conf["poll_interval"])
    
    except KeyboardInterrupt:
        print
        print "Exiting CodeWithUs daemon."
        return

if __name__ == "__main__":
    main()
