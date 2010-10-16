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
    
    def notify(self, title, message, icon=None):
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
    
    def notify(self, title, message, icon=None):
        """
        Show a Growl notification popup.
        """
        
        self.growler.notify("git-event", title, message, icon=icon)

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
            "showall": True, # debug for always getting data
            }
        
        url = self.server_name + self.subscription_url
        data = urllib.urlencode(values)
        
        # build the request object and get the response data
        request = urllib2.Request(url, data)
        
        try:
            response = urllib2.urlopen(request)
            
            # get raw JSON data
            rdata = response.read()
            print rdata
            
            # turn it into native data
            jdata = json.loads(rdata)
        except Exception, e:
            print e
            return
        
        # TODO: refactor this into the EventBuilder class in git_event
        for event in jdata["events"]:
            new_event = git_event.Event(event["kind"], event["time"],
                                        event["email"], event["data"])
            result.append(new_event)
        
        return result

def main(args=sys.argv):
    
    # create our utility objects
    p = Poller(config.SERVER_NAME, config.USER_EMAIL)
    n = GrowlNotifier("CodeWithUs")
    
    # loop, polling for new notifications
    try:
        while 1:
            
            # show notifications for latest events
            print "poll"
            for event in p.poll():
                title = "Commit from %s:" % event.user_email
                message = event.data["message"]
                
                n.notify(title, message)
            
            # wait a bit before the next poll cycle
            time.sleep(config.POLL_INTERVAL)
    
    except KeyboardInterrupt:
        print
        print "Exiting CodeWithUs daemon."
        return

if __name__ == "__main__":
    main()
