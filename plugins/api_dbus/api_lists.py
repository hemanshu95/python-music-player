
import dbus
from dbus_service import DBusService

from patterns import signals

import simplejson
import dataobjects
import music_lists.MusicList

class API_Lists(DBusService):
    def __init__(self, listsmanager):
        DBusService.__init__(self, 'lists')
        self._listsmanager = listsmanager
        self._connect_to_signals()

    def _connect_to_signals(self):
        signals.connect('tracklist.trackadded', self, self.signal_track_added)

    
    
    def signal_track_added(self, params):
        #params: (list_id, track_id, track)
        self.api_signal_track_added(params['list_id'], params['track_id'], simplejson.dumps(params['track'].serialize()))
    
    
    @dbus.service.signal(dbus_interface='org.pymp.daemon.lists')
    def api_signal_track_added(self, list_id, track_id, track_json):
        #if loading the track fails, the client will also fail doing so,
        # don't bother the client with it
        simplejson.loads(track_json)
        
    
    '''Create a new list of the requested type.
    It returns the id of the newly created list.'''
    @dbus.service.method('org.pymp.daemon.lists')
    def newList(self, listtype, listname):
        listtype = unicode(listtype)    #convert dbus String to python String
        
        newtracklist = self._listsmanager.get_new_list(listtype, listname)
        self._listsmanager.add_list(newtracklist)

        return

        
    '''Returns a list of all available list types'''
    @dbus.service.method('org.pymp.daemon.lists')
    def getListTypes(self):
        return simplejson.dumps(self._listsmanager.getListTypes())
        
        

    @dbus.service.method('org.pymp.daemon.lists')
    def getLists(self):
        lists = self._listsmanager.get_lists()
        lists_json = []
        
        for plist in lists:
            lists_json.append(lists[plist].serialize())
        
        
        return simplejson.dumps(lists_json)


    @dbus.service.method('org.pymp.daemon.lists')
    def getTracks(self, list_id, start=None, end=None):
        #TODO: Start and End
        tracklist = self._listsmanager.get_list(list_id)

        tracks = map(lambda x: (x[0], x[1].serialize()), tracklist.getTracks())
            
        return simplejson.dumps(tracks)

    @dbus.service.method('org.pymp.daemon.lists')
    def addFileAsTrack(self, list_id, filename):
        list_id = unicode(list_id)
        tracklist = self._listsmanager.get_list(list_id)
        tracklist.addTrack(dataobjects.Track.loadFromFile(filename))

        
        
    @dbus.service.method('org.pymp.daemon.lists')
    def addTracks(self, list_id, tracks_as_json):
        list_id = unicode(list_id)
        tracklist = self._listsmanager.get_list(list_id)
               
        tracks = simplejson.loads(tracks_as_json)
        for jtrack in tracks:
            track = dataobjects.Track(None)
            track.load(jtrack)
            tracklist.addTrack(track)
            print "* Added "+track.title+ " to playlist"
            
            