from patterns.Observable import Observable

import MusicPlayer
from music_lists.MusicList import MusicList
from patterns import signals


class QueuePlayer(Observable):
    
    STATE_READY   = 0
    STATE_PLAYING = 1
    STATE_PAUSED  = 2
    
    def __init__(self, queue):
        Observable.__init__(self)
        
        self._musicplayer = MusicPlayer.GStreamerPlayer()
        self._musicplayer.attach(self)
        
        self.queue = queue
        self.currentTrack = None
        self._track_in_musicplayer = None
        self.state = QueuePlayer.STATE_READY
        
        print "Creating a new QueuePlayer object"
        
    
    def getQueue(self):
        '''Returns the attatched queue.'''
        return self.queue


    def changeTrack(self, track):
        '''
        Change the current playing track. This will immedeatly
        stop the current running track.
        '''
        print("~~~~~~~~")
        self.currentTrack = track
        
        #TODO: Handle correctly when on pause state
        if self.currentTrack != None:
            self.play()
        else:
            print("! There are no new tracks in the queue to play!")
            raise Exception("No new tracks!")
    
    
    def play(self):
        '''
        Start playing the currentTrack from the beginning of the song.
        '''
        if self.currentTrack == None:
            try: return self.nextTrack()
            except: raise
        
        self.state = QueuePlayer.STATE_PLAYING
        if self.state == QueuePlayer.STATE_PAUSED:
            self._musicplayer.resume()
        else:
            self._musicplayer.play(self.currentTrack)
            signals.emit("player.play")
        
    
    def pause(self):
        '''
        Pauses the current track playback.
        Playback can be resumed by calling .play()
        '''
        self.state = QueuePlayer.STATE_PAUSED
        self._musicplayer.pause()
    
    
    def stop(self):
        '''
        Stops the playback of the queue.
        '''
        QueuePlayer.STATE_READY
        self._musicplayer.stop()

    
    def nextTrack(self):
        '''Iff possible, start the following track in the list.'''
        self.changeTrack(self.queue.popTrack())
        

    def prevTrack(self):
        '''Starts the previous played track.'''
        print("! Previous track is not supported yet!")
        return
    
    
    def getCurrentTrack(self):
        '''Returns the track currently playing.'''
        return self.currentTrack
    
    
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
                print "  Track almost finished"
                pass
            