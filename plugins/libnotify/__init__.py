
from patterns import signals
import pynotify

from plugins import Plugin


info = {'class': "LibNotify"}

class LibNotify(Plugin):    
    
    def setup(self):
        self._currentMessage = None
    
    def start(self):
        signals.connect("player.play", self, self.notifyNewSong)       
        self._currentMessage = None

    
    def stop(self):
        signals.disconnect("player.play", self)
        self.hideCurrentMessage()
    
    
    def showMessage(self, title, message):
        if pynotify.init("PyMP"):
            n = pynotify.Notification(title, message)
            n.show()
            self._currentMessage = n
            
    def hideCurrentMessage(self):
        if self._currentMessage != None:
            self._currentMessage.close()

    def notifyNewSong(self):
        current_track = self.listPlayer.getCurrentTrack()

        self.hideCurrentMessage()
        self.showMessage("Now playing", current_track.title + " - " + current_track.artist)

