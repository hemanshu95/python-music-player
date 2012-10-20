
from Queue import Queue as pyQueue

class TrackQueue:
    '''
    Object that orchastrates the tracks to be played.
    New tracks can be appended to the queue. Also a playlist
    can be set as a list of tracks to be played by the queue.
    
    A music player can take new tracks from the queue by
    simply invoking .popTrack()
    
    If there no tracks explicitly added to to the queue, the
    queue will take tracks from the playlist.
    '''
    
    def __init__(self):
        self.queue = pyQueue()
        self.tracklist = None
        self.tracklistpointer = 0


    def addToQueue(self, track):
        '''Add a track to the end of the queue.'''
        self.queue.put(track)


    def popTrack(self):
        '''
        Pops a track from the queue. This track can be used
        as the new track to be played after a song has ended.
        
        If there are no new tracks, the first upcoming track from
        the music list is returned, and the list-index is incremented
        by one.
        '''
        nextTrack = None
        if self.queue.qsize() > 0:
            nextTrack = self.queue.get()
            
        elif self.tracklist != None:
            self.tracklistpointer = self.tracklist.getNextTrackIndex(self.tracklistpointer)
            if self.tracklistpointer != None:
                nextTrack = self.tracklist.getTrack(self.tracklistpointer)
        
        if nextTrack == None:
            raise NoTracksException()
        return nextTrack


    def setList(self, tracklist):
        '''
        Set a playlist where tracks should be loaded from
        if the queue is empty. Also resets the tracklist pointer.
        '''
        self.tracklist = tracklist
        self.tracklistpointer = 0
        
        
    def getList(self):
        '''
        Returns the list of tracks to be played after the
        queue is empty.
        '''
        return self.tracklist
