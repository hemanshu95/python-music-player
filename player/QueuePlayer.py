from patterns.Observable import Observable

import MusicPlayer
from patterns import signals
from states import PlayerStates
from queue import NoTracksException

class QueuePlayer(Observable):
    
    def __init__(self, queue):
        Observable.__init__(self)
        
        self._musicplayer = MusicPlayer.GStreamerPlayer()
        self._musicplayer.attach(self)
        
        self.queue = queue
        self._currentTrack = None
        
        self.state = PlayerStates.STOPPED
        
        print("Creating a new QueuePlayer object")
        
    
    def getQueue(self):
        '''Returns the attatched queue.'''
        return self.queue


    def setTrackFromQueue(self):
        '''
        Sets the current track from the top track of the queue.
        '''
        self._currentTrack = self.queue.popTrack()


    def play(self):
        '''
        Start playing the currentTrack from the beginning of the song.
        If the player is already playing, calling this effect will have no effect.
        '''
        if self.state == PlayerStates.PLAYING:
            return
        
        if self._currentTrack == None:
            try:
                self.setTrackFromQueue()
            except:
                return
        
        if self.state == PlayerStates.PAUSED:
            self._musicplayer.resume()
        else:
            print(">>>>")
            self._musicplayer.play(self._currentTrack)
            signals.emit("player.play")

        self.state = PlayerStates.PLAYING
        
    
    def pause(self):
        '''
        Pauses the current track playback.
        Playback can be resumed by calling .play()
        '''
        self.state = PlayerStates.PAUSED
        self._musicplayer.pause()
        
        
    def playpause(self):
        '''
        If playback is paused, resume playback, otherwise start playback.
        '''
        if self.state == PlayerStates.PLAYING:
            self.pause()
        else:
            self.play()
    
    
    def stop(self):
        '''
        Stops the playback of the queue.
        '''
        self.state = PlayerStates.STOPPED
        self._musicplayer.stop()


    def getState(self):
        '''
        Returns the current player state, which can be one of 
        QueuePlayerStates.
        '''
        return self.state

    
    def nextTrack(self):
        '''
        Iff possible, start the following track in the list.
        If not possible, playback is ended.
        '''
        try:
            self.setTrackFromQueue()
            self.stop()
            self.play()
        except NoTracksException as _:
            print("No new track to play: stopping playback.")
            self.stop()
        

    def prevTrack(self):
        '''Starts the previous played track.'''
        print("! Previous track is not supported yet!")
        return
    
    
    def getCurrentTrack(self):
        '''Returns the track currently playing.'''
        return self._currentTrack
    
    
    def _changedTrack(self):
        '''Should be called whan a track has been changed. Any
        watchers will be notified.'''
        self.notify()
        
    
    def update(self, x, message):
        '''Function which is called when an observed objects sends an update.
        In this case, we only watch the self._musicplayer instance for status changes.'''

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
            
            