
import constants
from dataobjects import Track, Artist, Album
import simplejson

class Collection():
    def __init__(self, name, displayname, fullinmemory = False, searchable = False):
        self._fullinmemory = False
        self._searchable = False
        self._displayname = displayname
        
        self._name = name
        
        #Collections may be stored on disk in a cache, make sure we have one
        self._cachedir = constants.cache_dir_collections
        
    
    def getDisplayName(self):
        return self._displayname
    
    
    def search(self):
        pass


    def serialize_info(self):
        return {'name': self._name, 'displayname': self._displayname, 'searchable': self._searchable}
    
    
    
    def available(self):
        """Returns True when the collection is available.
        Non-available collections may be network-collections,
        external devices, etc."""
        return False
    
    

class FullMemoryCollection(Collection):
    
    def __init__(self, name, displayname, searchable = False):
        Collection.__init__(self, name, displayname, True, searchable)
        self._artists = {}
        self._albums  = {}
        self._tracks = []
        
        
    def getAllTracks(self):
        return self._tracks
    
    
    def dump_tracks_as_json(self):
        tracktree = []
        for track in self._tracks:
            tracktree.append(track.serialize())
        return simplejson.dumps(tracktree)
    
    
    def load_tracks_as_json(self, jsonstring):
        for trackdata in simplejson.loads(jsonstring):
            t = Track(None)
            t.load(trackdata)
            self._tracks.append(t)
        self.sortTracks()
            
            
    def writetofile(self):
        #Dump it to a file :)
        f = open(self._cachedir+self._name, 'w')
        f.write(self.dump_tracks_as_json())
        f.close()
           
            
    def loadfromfile(self):
        try:
            f = open(self._cachedir+self._name, 'r')
            self.load_tracks_as_json(f.read())
            f.close()
        except:
            self.scan()
            
            
    def sortTracks(self):
        for track in self._tracks:
            
            if track.artist == None:
                artist = "unknown"
            else:
                artist = track.artist.lower()
    
            
            if track.album == None:
                album = "unknown"
            else:
                album = track.album.lower()
    
            
            if track.year == None:
                year = 0
            else:
                year = track.year

    
            if artist not in self._artists:
                self._artists[artist] = Artist(track.artist)

            albumname = artist+"\n"+album+"\n"+str(year)
            if albumname not in self._albums:
                self._albums[albumname] = Album(track.album, artist)
                self._artists[artist].addAlbum(albumname)
            self._albums[albumname].addTrack(track)
        
        
    def buildAlbums(self):
        # Phase one: sort all tracks by albumname
        albums_by_name = {}
        for track in self._tracks:
            
            if track.album == None:
                track.album = "Unknown"
            
            if track.album.lower() not in albums_by_name:
                albums_by_name[track.album.lower()] = []
            albums_by_name[track.album.lower()].append(track)
           
        #TODO: there may be multiple albums with the same name around,
        #TODO: There may be albums with various artists, also check for this later
        #
        all_albums = []
        
        for albumname in albums_by_name:
            found_albums = {}
            for track in albums_by_name[albumname]:
                if track.artist.lower() not in found_albums:
                    found_albums[track.artist.lower()] = {}
                
                year = track.year
                if year == None:
                    year = 0
                    
                if year not in found_albums[track.artist.lower()]:
                    album = Album(track.album, track.artist)
                    found_albums[track.artist.lower()][year] = album
                    all_albums.append(album)
                
                found_albums[track.artist.lower()][year].addTrack(track)
        
        
        all_albums.append
    
    
    def getArtists(self):
        return self._artists
    
    
    