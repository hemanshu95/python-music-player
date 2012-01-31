import os

home = os.getenv('USERPROFILE') or os.getenv('HOME')+"/"


'''Makes sure that a directory is present in the filesystem.
If it is not there, it will be created.'''
def assertDir(path):
    try:
        os.mkdir(path)
    except:
        pass

config_dir = home+".pymp/"
assertDir(config_dir)

config_dir_collections = config_dir+"collections/"
assertDir(config_dir_collections)

cache_dir = config_dir+".cache/"
assertDir(cache_dir)

cache_dir_collections = cache_dir+"collections/"
assertDir(cache_dir_collections)