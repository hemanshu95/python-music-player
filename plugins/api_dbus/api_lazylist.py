
#load-list lastfm lasftm://xxxxx


import dbus
from dbus_service import DBusService

import simplejson
import dataobjects
import music_lists.MusicList

class API_LazyList(DBusService):
    def __init__(self, listsmanager, listplayer):
        DBusService.__init__(self, 'lazylist')
        self._listsmanager = listsmanager
        self._listplayer = listplayer


    @dbus.service.method('org.pymp.daemon.lazylist')
    def addTracks(self, tracks_as_json):
        tracklist = self._listplayer.get_list()
        
        if tracklist == None:
            newtracklist = music_lists.MusicList.FileList("List 1")
            self._listsmanager.add_list(newtracklist)
            self._listplayer.set_list(newtracklist)
            tracklist = newtracklist
        
        tracks = simplejson.loads(tracks_as_json)
        for jtrack in tracks:
            track = dataobjects.Track(None)
            track.load(jtrack)
            tracklist.addTrack(track)
            print "* Added "+track.title+ " to current playlist"
            
            