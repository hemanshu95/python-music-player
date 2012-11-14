from patterns.Observable import Observable

from patterns.llist import LList

from patterns import signals

#abstract
class MusicList(Observable):
    '''Super Class for music lists.'''
    
    def __init__(self, name):
        Observable.__init__(self)
        self._tracks = LList()
        self._name = name
    
    
    def getName(self):
        return self._name
    
    def getAllTracks(self):
        raise NotImplementedError

    def getPlayerType(self):
        raise NotImplementedError
    
    def addTrack(self, track):
        '''Adds a track to the list, the assigned index is returned.'''
        track_id = self._tracks.append(track)
        signals.emit('tracklist.trackadded', {'list_id': self._name, 'track_id': track_id, 'track': track})
        return track_id

    def getTrack(self, index):
        '''Returns a track for the given index.'''
        return self._tracks.getData(index)

    def getTracks(self):
        '''Returns all tracks in order in the following format:
        (index, Track)'''
        tracks = map(lambda index: (index, self._tracks.getData(index)), self._tracks.getNodes())
        return tracks

    def getPrevTrackIndex(self, index):
        '''Returns the index for the previous track.'''
        return self._tracks.getPrev(index)

    def getNextTrackIndex(self, index):
        '''Returns the index for the next track.'''
        return self._tracks.getNext(index)
    
    def _trackadded(self):
        self.notify()
    
    
    def serialize(self):
        return { 'name': self._name }
    

class FileList(MusicList):
    def __init__(self, name):
        MusicList.__init__(self, name)
        
class StreamList(MusicList):
    def __init__(self, name):
        MusicList.__init__(self, name)
        
