
import dbus
from dbus_service import DBusService

class API_Player(DBusService):
    def __init__(self, listsmanager, listplayer):
        DBusService.__init__(self, 'player')
        
        self._listplayer = listplayer
        self._listsmanager = listsmanager
        self._list = None
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def set_list(self, listid):
        tracklist = self._listsmanager.get_list(listid)

        #Make sure that we stop the current listplayer!
        if self._listplayer != None:
            self._listplayer.stop()
        self._listplayer.set_list(tracklist)
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def get_list(self):
        tracklist = self._listplayer.get_list()
        
        if tracklist != None:
            list_id = tracklist.getName()
            return list_id
        else:
            return None
    
    
    #Burp, TODO! playTrackByIndex.. rethink the idea here
    @dbus.service.method('org.pymp.daemon.player')
    def playTrack(self, trackuid):
        trackuid = int(trackuid)
        self._listplayer.playTrack(trackuid)
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def play(self):
        self._listplayer.play()
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def pause(self):
        self._listplayer.pause() 
        

    @dbus.service.method('org.pymp.daemon.player')
    def stop(self):
        self._listplayer.stop()


    @dbus.service.method('org.pymp.daemon.player')
    def nextTrack(self):
        self._listplayer.nextTrack()
        
        
    @dbus.service.method('org.pymp.daemon.player')
    def prevTrack(self):
        self._listplayer.prevTrack()
        