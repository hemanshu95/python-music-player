
class Artist():
    def __init__(self, name):
        self._albums = []
        self._name = name
        
    def addAlbum(self, albumname):
        self._albums.append(albumname)
    
    def getName(self):
        return self._name
    
    def getAlbums(self):
        return self._albums
    

class Album():
    def __init__(self, title, artist):
        self.tracks = []
        
        self.title = title
        self.artist = artist
        
    def addTrack(self, track):
        self.tracks.append(track)
        
    def getYear(self):
        year = None
        for track in self.tracks:
            tyear = track.year
            if tyear == None:
                year = tyear
            elif tyear > year:
                year = tyear
                 
        return year

        
class Track():
    def __init__(self, uri=None):
        self.uri = uri
        
        self.title = "<Unknown>"
        self.artist = "<Unknown>"
        self.album = "<Unknown>"
        self.tracknumber = 0
        self.year = None
        self.length = None
        

    def serialize(self):
        return {'uri': self.uri, 'title': self.title, 'artist': self.artist, 'album': self.album, 'year': self.year, 'track': self.tracknumber, 'length': self.length}
    
    
    def load(self, data):
        self.uri = data['uri']

        self.artist = data['artist']
        self.title = data['title']
        self.album = data['album']
        self.year  = data['year']
        self.tracknumber = data['track']
        self.length = data['length']
        
    @staticmethod
    def fromData(data):
        x = Track()
        x.load(data)
        return x
    