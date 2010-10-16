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
    and returned by the build_* functions, and sent to the actual server
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

class EventBuilder:
    """
    Builds and returns correctly formatted events.
    """
    
    def __init__(self, repo):
        self.repo = repo
    
    def build_push(self):
        raise NotImplementedException("Must implement push!")

    def build_commit(self):
        # get the commit we're going to operate on
        commit = self.repo.head.commit # latest commit for this repository
        
        # all the data we'll need for this commit:
        #  active_branch: the current branch
        #  author_email: the email of the author of the commit
        #  hash: the sha hash (in hex) of the commit
        #  message: the commit message
        #  deletions: number of lines deleted
        #  insertions: number of lines inserted
        #  files: number of files modified
        data = {
            "active_branch": self.repo.active_branch.name,
            "commit_hash": commit.hexsha,
            "author_email": commit.author.email,
            "message": commit.message,
            "deletions": commit.stats.total["deletions"],
            "insertions": commit.stats.total["insertions"],
            "files": commit.stats.total["files"],
            }
        
        return Event("commit", commit.committed_date, USER_EMAIL, data)

    def build_branch(self):
        raise NotImplementedException("Must implement branch!")

    def build_checkout(self):
        raise NotImplementedException("Must implement checkout!")

def main(args=sys.argv):
    """
    Parse the args, create the event object, then send it to the server.
    """
    
    if len(args) < 2:
        print "ERROR: No event type specified."
        return
    
    # build events from the specified repository
    builder = EventBuilder(git.Repo(REPO_DIR))
    
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
    sender = Sender(SERVER_ADDRESS)
    if event is not None:
        sender.send_event(event)

if __name__ == "__main__":
    main()
