import os
import time
from patterns import signals
from dataobjects import Track
from plugins import Plugin
import simplejson

import lastfm

info = {'class': "LastFMScrobbler", 'author': "Remco van der Zon"}


#TODO: Make scrobblequeue file static field
#TODO: Scrobble on 60% (?) of track

 
class LastFMScrobbler(Plugin):    
    
    queuefile = 'lastfm-scrobble-cache' 
    
    def setup(self):
        self._scrobbler = lastfm.Scrobbler()
        self._nowplaying = None
    
    
    def start(self):
        signals.connect("player.trackfinished", self, self.lastfmscrobble)
        signals.connect("player.play", self, self.lastfmnewsong)
        self.scrobble_cueue()

    
    def stop(self):
        signals.disconnect("player.trackfinished", self, self.lastfmscrobble)
        signals.disconnect("player.play", self, self.lastfmnewsong)
        self.hideCurrentMessage()
    
    
    def scrobble(self, track, timestamp):
        """Scrobbles a track to last.fm, if scrobbling the track fails 
        it will be scrobbled later (when it possible again to scrobble)"""
        try:
            self._scrobbler.scrobble(track, timestamp)
        except:
            self.add_to_scrobble_cueue(track, timestamp)
    
    
    def lastfmnewsong(self):
        """Notifies last.fm that the user is now listening... to another track."""        
        current_track = self.queueplayer.getCurrentTrack()
        self._nowplaying = current_track
        try:
            self._scrobbler.informplaying(current_track)
        except:
            pass
        

    def lastfmscrobble(self):
        """Scrobbles the current track to last.fm. If this fails the track is added
        to the scrobble queue."""
        if self._nowplaying != None:
            timestamp = str(int(time.time()))
            self.scrobble(self._nowplaying, timestamp)
        
    
    
    ######
    ## Methods for queue below.
    ## Note: The queue is a repeatment of timestamp and tracks:
    ##
    ##  Timestamp\n
    ##  Serialized Track data\n
    ## 
    
    
    def add_to_scrobble_cueue(self, track, timestamp):
        """Adds a track to the tracks-to-be-scrobbled queue"""
        f = open(self.queuefile, 'a')
        f.write(timestamp+"\n")
        f.write(simplejson.dumps(track.serialize())+"\n")
        f.close()
    
    
    def scrobble_cueue(self):
        """Tries to scrobble all tracks in the queue to last.fm.
        When tracks fail to scrobble, they will be re-added tot he queue."""
        if not os.path.isfile(self.queuefile):
            return
        
        #get all scrobbles from the cache file,
        # then purge it and parse it. When tracks
        # can not be scrobbled, they will be re-added
        # to the file later
        f = open(self.queuefile, 'r')
        lines = f.readlines()
        f.close()
        
        f = open(self.queuefile, 'w')
        f.write("")
        f.close()
        
        timestamp = None
        for line in lines:
            line = line.rstrip()
            if not timestamp:
                #Try some sort of error recovery, when timestamp is expected,
                # but a nontimestamp has been read, break and the current line is ignored
                try: 
                    int(line)
                    timestamp = line
                except:
                    pass
                
                
            else:
                track = Track.deserialize(simplejson.loads(line))
                self.scrobble(track, timestamp)
                timestamp = None

        