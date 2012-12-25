import re
import mutagen
from mutagen.easyid3 import EasyID3
from dateutil.parser import parse as dateparser

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
        return {'uri': self.uri, 'title': self.title, 'artist': self.artist,
                'album': self.album, 'year': self.year, 'track': self.tracknumber,
                'length': self.length}
    
    
    def _load_deserialize(self, data):
        self.uri = data['uri']

        self.artist = data['artist']
        self.title = data['title']
        self.album = data['album']
        self.year  = data['year']
        self.tracknumber = data['track']
        self.length = data['length']
        
        

    @staticmethod
    def deserialize(data):
        '''
        Returns a new Track object based from the information 
        in a serialized form.
        '''
        newTrack = Track()
        newTrack._load_deserialize(data)
        return newTrack
    
    
    @staticmethod
    def loadFromUri(uri):
        if uri[7] == "file://":
            return Track.loadFromFile(uri[7:])
        
        raise Exception("Not supported!")
    
    
    @staticmethod
    def loadFromFile(filename):
        '''
        Loads a new Track object based on the contents of an (audio) file.
        '''
        try:    
            audiodata = mutagen.File(filename, easy=True)                        
        except:
            print "---- failure: %s"%filename
            raise Exception("Could not open file for EasyID3")
        t = Track("file://"+filename)
        
        if "title" in audiodata:  t.title = audiodata["title"][0]
        if "artist" in audiodata: t.artist = audiodata["artist"][0]
        if "album" in audiodata:  t.album = audiodata["album"][0]
        if "date" in audiodata:
            try:
                dt = dateparser.parse(audiodata["date"][0])
                t.year = dt.year
            except:
                t.year = audiodata["date"][0]
                    
        if "tracknumber" in audiodata: 
            t.tracknumber = int(re.findall(r'\d+', audiodata["tracknumber"][0])[0])
            
        t.length = audiodata.info.length

        return t
        