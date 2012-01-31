
import os
from plugins import Plugin

from playlists import PympSpotifyPlaylists
from playlists.spotifyplaylist import SpotifyPlaylist


info = {
        'class': "SpotifyPluginn"
}

import threading
from threading import Thread

class SpotifyPlugin(Plugin, Thread):    
    
    def setup(self):
        Thread.__init__(self)
        self.pympspotify = PympSpotify("theunknowncylon", "Seven79", self.listManager)
    
    
    def start(self):
        self.listManager.registerNewListType("spotify", SpotifyPlaylist)
        self.pympspotify.connect()
    
    
    def stop(self):
        self.pympspotify.disconnect()
        self.listManager.deregisterNewListType("spotify", SpotifyPlaylist)
        
    

# --------------------------

#import spotify

from spotify.manager import SpotifySessionManager
    
    
# Should be its own Thread... somehow it blocks all te rest :(
class PympSpotify(SpotifySessionManager):
    appkey_file = os.path.join("/home/remco_lw/", 'spotify_appkey.key')
    
    def __init__(self, username, password, pymplistmanager):
        SpotifySessionManager.__init__(self, username, password, True)
        
        #Pymps ListManager
        self._pymplistManager = pymplistmanager
        
        self._session = None

    #callback from spotify
    def logged_in(self, session, error):
        if error:
            print error
            return
        self._session = session
        
        print "Logged in into Spotify"
        
        #Set up spotify managers
        self.playlists = PympSpotifyPlaylists(self._pymplistManager, session.playlist_container())
        

    #callback from spotify
    def logged_out(self, session):
        print "Logged out!"





