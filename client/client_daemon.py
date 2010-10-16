import sys
import time
import urllib
import urllib2

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
        
        result = []
        
        # build the http 'get' request
        url = self.server_name + self.subscription_url
        data = urllib.urlencode({"email": self.user_email})
        
        # how we'll turn our data into events once again
        eb = git_event.EventBuilder(config.REPO_NAME, config.USER_EMAIL)
        
        # build the request object and get the response data
        request = urllib2.Request(url, data)
        
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e
            return
        
        return result

def main(args=sys.argv):
    
    # create our utility objects
    p = Poller(config.SERVER_NAME)
    n = GrowlNotifier("CodeWithUs")
    
    # loop, polling for new notifications
    try:
        while 1:
            
            # show notifications for latest events
            for event in p.poll():
                if event.type == "commit":
                    title = "Commit from " + event.user + ":"
                    message = event.data["message"]
            
            # wait a bit before the next poll cycle
            time.sleep(config.POLL_INTERVAL)
    
    except KeyboardInterrupt:
        print
        print "Exiting CodeWithUs daemon."
        return

if __name__ == "__main__":
    main()
