
import os

import mutagen
import simplejson

from dateutil import parser as dateparser
from mutagen.easyid3 import EasyID3
from dataobjects import Track, Artist, Album
import constants

class CollectionManager():
    def __init__(self):
        self._collections = {}
        self._collectionTypes = {}
        #self._load_collections()



    def registerNewCollectionType(self, key, theClass):
        self._collectionTypes[key] = theClass
        
    def deregisterCollectionType(self, key):
        raise NotImplemented()
    
    

    def load_collections(self):
        self._loadFromConfig()
        print "Collections loaded."
        
    
    def get_collection(self, name):
        return self._collections[name]
    
    
    def get_collections(self):
        return self._collections
    
    
    def get_collection_keys(self):
        keys = self._collections.keys()
        keys.sort()
        return keys
    
    
    def _loadFromConfig(self):
        configdir = constants.config_dir_collections
                
        for filename in os.listdir(configdir):
            filenamefull = configdir + filename
            print "Loading collection "+filenamefull
            try:
                f = open(filenamefull)
                rules_raw = filter(lambda x: "=" in x, f.read().split("\n"))
                f.close()
                
                rules = {}
                for rule in rules_raw:
                    rule_parts = map(lambda x: x.strip(), rule.split("="))
                    if len(rule_parts) > 1:
                        rules[rule_parts[0]] = rule_parts[1]
                
                self._loadCollection(filename, rules['displayname'], rules['collection_type'], rules)
                    
            except Exception as e:
                print "Could not read collection config: "+filenamefull+" ("+unicode(e)+")"


    def _loadCollection(self, name, displayname, collectiontype, options):
        if collectiontype not in self._collectionTypes:
            raise Exception("Unknown collection type: "+collectiontype) 
        
        self._collections[name] = self._collectionTypes[collectiontype](name, displayname, options)
#        
#        if collection_type != "FilesSmallMedium":
#            raise Exception("Unknown collection type.")
#        
#        root = options['root']
#        
#        self._collections[name] = SmallMediumFileCollection(name, displayname, root)



