import git
import urllib
import urllib2
import sys
import time

from pprint import pprint

# user settings
REPO_DIR = "/Users/shira/codewithus"
USER_EMAIL = "jasontbradshaw@gmail.com"
SERVER_ADDRESS = "http://codewithus.heroku.com"

class Event:
    """
    Represents an event that we can push to the server.  Gets created
    and returned by the send_* functions, and sent to the actual server
    by a Sender object.
    """
    
    def __init__(self, type, timestamp, user_email, data):
        self.type = type
        self.timestamp = timestamp
        self.user_email = user_email
        
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
        self.event_post_url = "/event"
    
    def send_event(self, event):
        """
        Sends our event to the server in a format it can understand.
        """
        
        # TODO: remove test printing
        print "Sending an event to the server..."
        print "type:", event.type
        print "user_email:", event.user_email
        print "time:", event.timestamp
        print "data:"
        pprint(event.data)
        
        # create the url parameters as a dict
        values = event.data
        values["email"] = event.user_email
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

def build_push(repo):
    return "push!"

def build_commit(repo):
    # get the commit we're going to operate on
    commit = repo.head.commit # latest commit for this repository
    
    # all the data we'll need for this commit:
    #  active_branch: the current branch
    #  author_email: the email of the author of the commit
    #  hash: the sha hash (in hex) of the commit
    #  message: the commit message
    #  deletions: number of lines deleted
    #  insertions: number of lines inserted
    #  files: number of files modified
    data = {
             "active_branch": repo.active_branch.name,
             "hash": commit.hexsha,
             "author_email": commit.author.email,
             "message": commit.message,
             "deletions": commit.stats.total["deletions"],
             "insertions": commit.stats.total["insertions"],
             "files": commit.stats.total["files"],
           }
    
    return Event("commit", commit.committed_date, USER_EMAIL, data)

def build_branch(repo):
    return "branch!"

def build_checkout(repo):
    return "checkout!"

def main(args=sys.argv):
    """
    Parse the args, create the event object, then send it to the server.
    """
    
    repo = git.Repo(REPO_DIR)
    
    if len(args) < 2:
        print "ERROR: No event type specified."
        return
    
    # the type of event we're creating
    command = args[1]
    
    # switch on command type
    event = None
    if command == "push":
        event = build_push(repo)
    elif command == "commit":
        event = build_commit(repo)
    elif command == "branch":
        event = build_branch(repo)
    elif command == "checkout":
        event = build_checkout(repo)
    else:
        print "ERROR: Failed to recognize event type '" + command + "'."
        return
    
    # send our event to the server
    sender = Sender(SERVER_ADDRESS)
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
