
import dbus
from dbus_service import DBusService
from dataobjects import Track

class API_Player(DBusService):
    def __init__(self, listsmanager, player, queue):
        DBusService.__init__(self, 'player')
        
        self.player = player
        self.queue  = queue
        self.listsmanager = listsmanager
    

    @dbus.service.method('org.pymp.daemon.player')
    def set_track(self, filename):
        track = Track.loadFromFile(filename)
        self.player.changeTrack(track)
        
    
    @dbus.service.method('org.pymp.daemon.player')
    def queue_track(self, filename):
        track = Track.loadFromFile(filename)
        self.queue.addToQueue(track)
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def set_list(self, listid):
        tracklist = self.listsmanager.get_list(listid)
        self.queue.setList(tracklist)
    

    @dbus.service.method('org.pymp.daemon.player')
    def play(self):
        self.player.play()
    
    
    @dbus.service.method('org.pymp.daemon.player')
    def pause(self):
        self.player.pause() 
        

    @dbus.service.method('org.pymp.daemon.player')
    def stop(self):
        self.player.stop()


    @dbus.service.method('org.pymp.daemon.player')
    def nextTrack(self):
        self.player.nextTrack()
        
        
    @dbus.service.method('org.pymp.daemon.player')
    def prevTrack(self):
        self.player.prevTrack()
        