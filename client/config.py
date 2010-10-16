import json

def load_config(fname):
    """
    Loads the config file into a config object and returns it as a dict.
    Returns 'None' if the file couldn't be loaded.
    """
    
    try:
        with open(fname, 'r') as f:
            return json.loads(f.read())
    except Exception, e:
        print e
        return None
