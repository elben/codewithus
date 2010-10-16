import git
import urllib
import urllib2
import sys
import time

from pprint import pprint

# user settings
REPO_DIR = "/Users/shira/codewithus"
USER = "jasontbradshaw@gmail.com"
SERVER_ADDRESS = "http://codewithus.heroku.com"

# internal settings
REPO = git.Repo(REPO_DIR)

class GitEvent:
    """
    Represents an event that we can push to the server.  Gets created
    and returned by the send_* functions, and sent to the actual server
    by a Sender object.
    """
    
    def __init__(self, type, timestamp, user, data):
        self.type = type
        self.timestamp = timestamp
        self.user = user
        
        # a dict of event-type specific info (gets parsed by Sender)
        self.data = data

class Sender:
    """
    Sends an event to the specified remote server.
    """
    
    def __init__(self, server_address):
        self.server_address = server_address
        
        # basic info for our sender
        self.user_agent = "CodeWithUs Client"
        self.event_post_url = "/event/"
    
    def send_event(self, event):
        """
        Sends our event to the server in a format it can understand.
        """
        
        # TODO: remove test printing
        print "Sending an event to the server..."
        print "type:", event.type
        print "user:", event.user
        print "timestamp:", event.timestamp
        print "data:"
        pprint(event.data)
        
        # create the url parameters as a dict
        values = event.data
        values["email"] = event.user
        values["time"] = event.timestamp
        values["type"] = event.type
        
        # build the http request
        url = self.server_address + self.event_post_url
        data = urllib.urlencode(values)
        headers = {"User-Agent": self.user_agent}

        # build the request object and get the response data
        request = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e
            return
        
def report_push():
    return "push!"

def report_commit():
    # get the commit we're going to operate on
    commit = REPO.head.commit # latest commit for this repository
    
    # all the data we'll need for this commit:
    #  active_branch: the current branch
    #  author_email: the email of the author of the commit
    #  hash: the sha hash (in hex) of the commit
    #  message: the commit message
    #  deletions: number of lines deleted
    #  insertions: number of lines inserted
    #  lines: net (?) total lines modified
    #  files: number of files modified
    data = {
             "active_branch": REPO.active_branch.name,
             "hash": commit.hexsha,
             "author_email": commit.author.email,
             "message": commit.message,
             "deletions": commit.stats.total["deletions"],
             "insertions": commit.stats.total["insertions"],
             "lines": commit.stats.total["lines"],
             "files": commit.stats.total["files"],
           }
    
    return GitEvent("commit", commit.committed_date, USER, data)

def report_branch():
    return "branch!"

def report_checkout():
    return "checkout!"

def main(args=sys.argv):
    """
    Parse the args, create the event object, then send it to the server.
    """
    
    if len(args) < 2:
        print "ERROR: No event type specified."
        return
    
    # the type of event we're creating
    command = args[1]
    
    # switch on command type
    event = None
    if command == "push":
        event = report_push()
    elif command == "commit":
        event = report_commit()
    elif command == "branch":
        event = report_branch()
    elif command == "checkout":
        event = report_checkout()
    else:
        print "ERROR: Failed to recognize event type '" + command + "'."
        return
    
    # send our event to the server
    sender = Sender(SERVER_ADDRESS)
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
