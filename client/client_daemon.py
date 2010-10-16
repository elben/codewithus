import sys
import time
import urllib
import urllib2

import Growl

POLL_INTERVAL = 1

class Notifier:
    """
    Builds and displays a system notification.  Meant to be an
    abstraction from any platform-specific notification system (Growl,
    GNotify, Windows baloons, etc.).
    """
    
    def __init__(self, app_name):
        self.app_name = app_name
    
    def notify(self, title, message, icon=None):
        """
        Display a notification with the given title, message, and icon.
        """
        
        pass

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
        
        self.growler.notify("git-event", title, message)

def main(args=sys.argv):
    
    # loop, polling for new notifications
    try:
        while 1:
            print "Polling..."
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print
        print "Exiting CodeWithUs daemon."
        return

if __name__ == "__main__":
    main()
