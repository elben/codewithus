import git
import time

class Event:
    """
    Represents an event that we can push to the server.  Gets created
    and returned by the build_* functions, and sent to the actual server
    by a Sender object.
    """
    
    def __init__(self, kind, timestamp, user_email, data, face_url=None):
        self.kind = kind
        self.timestamp = timestamp
        self.user_email = user_email
        self.face_url = face_url
        
        # a dict of event-type specific info
        self.data = data

class EventBuilder:
    """
    Builds and returns correctly formatted events.
    """
    
    def __init__(self, repo_dir, user_email):
        self.repo = git.Repo(repo_dir)
        self.user_email = user_email
    
    def build_push(self):
        """
        Pushes are relatively spartan since we don't know much about
        them.
        """
        
        # TODO: get remote pushed to and send it in data
        data = {}
        
        return Event("push", int(time.time()), self.user_email, data)
    
    def build_commit(self, data=None):
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
        
        return Event("commit", commit.committed_date,
                     self.user_email, data)
    
    def build_checkout(self):
        """
        Tell what branch we're on after we checkout.
        """
        
        print type(self.repo.active_branch)
        
        data = {
            "active_branch": self.repo.active_branch,
            }
        
        return Event("checkout", int(time.time()), self.user_email, data)
