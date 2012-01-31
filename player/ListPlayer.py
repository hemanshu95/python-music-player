from patterns.Observable import Observable

import MusicPlayer
from patterns import signals


#TODO: Singleton?
#       i.e. allow the listplayer to load another list
#       instead of requiring a new listplayer for each list.
class ListPlayer(Observable):
    
    STATE_NOLIST = 01
    STATE_READY = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    
    def __init__(self):
        Observable.__init__(self)
        
        self._tracklist = None
        
        # Create a musicplayer object, which we will use
        # to actually play a track.
        self._musicplayer = None
        self._state = ListPlayer.STATE_NOLIST
        
        self._currentTrack = None
        self._currentTrackIndex = None
    
        print "Creating a new ListPlayer object"
        
    
    def set_list(self, tracklist):
        self._tracklist = tracklist
        self._musicplayer = tracklist.getPlayer()
        self._musicplayer.attach(self)

        self._state = ListPlayer.STATE_READY
    
    
    def get_list(self):
        return self._tracklist
    
    
    '''Function which is called when an observed objects sends an update.
    In this case, we only watch the self._musicplayer instance for status changes.'''
    def update(self, x, message):
        #print "GOT AN UPDATE FROM SOMETHING..."+str(x)+" | "+str(message)
        if isinstance(x, MusicPlayer.MusicPlayer):
            if message == MusicPlayer.MusicPlayer.TRACKFINISHED:

                signals.emit("player.trackfinished")
                
                try:
                    self.nextTrack()
                except:
                    self.stop()
                    
            elif message == MusicPlayer.MusicPlayer.TRACKALMOSTFINISHED:
                #print "  Track almost finished"
                pass
    
    
    '''Start playing the list from start, or from nextTrack.'''
    def play(self):
        self.playTrack(0)
    
    
    '''Start playing from a request track track.
    Stops playing the current track, if any.'''
    def playTrack(self, trackIndex):
        self._currentTrackIndex = trackIndex
        self._currentTrack = self._tracklist.getTrack(trackIndex)
        self._musicplayer.play(self._currentTrack)

        signals.emit("player.play")
    
    
    '''Pauses the current track playback'''
    def pause(self):
        self._musicplayer.pause()
    
    
    '''Stops the playback of the playlist.'''
    def stop(self):
        if self._musicplayer:
            self._musicplayer.stop()
    
    '''Iff possible, start the following track in the list.'''
    def nextTrack(self):
        nextTrackIndex = self._tracklist.getNextTrackIndex(self._currentTrackIndex)
        if nextTrackIndex != None:
            self.playTrack(nextTrackIndex)
        else:
            pass
            #TODO
    
    
    '''Iff possible, start the previous track in the list.'''
    def prevTrack(self):
        prevTrackIndex = self._tracklist.getPrevTrackIndex(self._currentTrackIndex)
        if prevTrackIndex != None:
            self.playTrack(prevTrackIndex)
        else:
            pass
            #TODO
    
    
    '''Returns True iff the listplayer supports the action pause track'''
    def supportPause(self):
        raise NotImplementedError
    
    '''Returns True iff the listplayer supports the action next-track'''
    def supportNexTrack(self):
        raise NotImplementedError
    
    '''Returns True iff the listplayer supports the action previous-track'''
    def supportPrevTrack(self):
        raise NotImplementedError
    
    '''Should be called whan a track has been changed. Any
    watchers will be notified.'''
    def _changedTrack(self):
        self.notify()
    
    
    def getCurrentTrack(self):
        return self._currentTrack
    
