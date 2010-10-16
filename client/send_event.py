import git
import urllib2
import sys
import time

from pprint import pprint

# user settings
REPO_DIR = "/Users/shira/codewithus"
USER = "jasontbradshaw@gmail.com"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

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
    
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
    
    def send_event(self, event):
        """
        Sends our event to the server in a format it can understand.
        """
        
        print "Sending an event to the server..."
        print "type:", event.type
        print "user:", event.user
        print "timestamp:", event.timestamp
        print "data:"
        pprint(event.data)

def report_push():
    return "push!"

def report_commit():
    # get the commit we're going to operate on
    commit = REPO.head.commit # latest commit for this repository
    
    # all the data we'll need for this commit:
    #  active_branch: the current branch
    #  author_email: the email of the author of the commit
    #  files_modified: a list of the full path name of modified file
    #    for the commit
    #  hash: the hex sha hash of the commit
    #  message: the commit message
    data = {
             "active_branch": REPO.active_branch.name,
             "author_email": commit.author.email,
             "files_modified": [f for f in commit.stats.files],
             "hash": commit.hexsha,
             "message": commit.message,
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
    
    # send our event to the server
    sender = Sender(SERVER_IP, SERVER_PORT)
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
