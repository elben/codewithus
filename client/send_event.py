import git
import urllib2
import sys

# user settings
REPO_DIR = "/Users/shira/codewithus"
USER = "jasontbradshaw"

# internal settings
REPO = git.Repo(REPO_DIR)

class GitEvent:
    """
    Represents an event that we can push to the server.  Gets created
    and returned by the send_* functions, and send to the actual server
    by the Sender object.
    """
    
    def __init__(self, user, branch, type, data):
        self.user = user
        self.branch = branch
        self.type = type
        self.data = data

class Sender:
    """
    Sends an event to the specified remote server.
    """
    
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
    
    def send_event(self, event):
        pass

def report_push():
    return "push!"

def report_pull():
    return "pull!"

def report_commit():
    return REPO.head.commit.message.strip()

def report_branch():
    return "branch!"

def report_checkout():
    return "checkout!"

def main(args=sys.argv):
    print "args:", args
    
    if len(args) < 2:
        print "ERROR: No event type specified."
        return
    
    command = args[1]
    
    # switch on command type
    if command == "push":
        print report_push()
    elif command == "pull":
        print report_pull()
    elif command == "commit":
        print report_commit()
    elif command == "branch":
        print report_branch()
    elif command == "checkout":
        print report_checkout()
    else:
        print "ERROR: Failed to recognize event type '" + command + "'."
    
if __name__ == "__main__":
    main()
