
import MusicList

class ListManager():
    def __init__(self):
        self._lists = {}
        self._listTypes = {}
        
        self.registerNewListType("filelist", MusicList.FileList)


    def get_new_list(self, listtype, parameter):
        '''Returns a new list. Based on the type of list and its
        parameter, the list may contain items downloaded from the web or
        other sources.'''
        if listtype not in self._listTypes:
            raise Exception("unknown listtype: "+listtype)
        
        return self._listTypes[listtype](parameter)
        
    
    def registerNewListType(self, key, theClass):
        '''Register a new type of playlist.
        Note that all supported type of playlists should be calling this method only once!'''
        self._listTypes[key] = theClass
    
    
    def deregisterNewListType(self, key):
        raise NotImplemented()
    
    
    def get_lists(self):
        return self._lists
    
    
    def get_list(self, name):
        if name in self._lists:
            return self._lists[name]
        raise Exception("No such list (did you register it with add_list?): "+name)
    
    
    def add_list(self, musiclist):
        name = musiclist.getName()
        if name in self._lists:
            raise Exception("Not a unique list-name: "+unicode(name)+".")
        
        self._lists[name] = musiclist
        
        
    