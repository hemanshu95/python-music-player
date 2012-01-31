import os
import mutagen
import magic
import dateutil

class TagDefinitions:
    artist = ["artist"]
    album = ["album"]
    title = ["title"]
    year = ['date']
    track = ['tracknumber']
    

class Collection:
    def __init__(self):
        self.collection = {}
        
    def addArtist(self, artist):
        if artist.name.lower() in self.collection:
            raise
        self.collection[artist.name.lower()] = artist
    
    def getArtist(self, artistname):
        if artistname.lower() in self.collection:
            return self.collection[artistname.lower()]
        return None


class Artist:
    def __init__(self, name):
        self.name = name
        self.albums = {}
    
    def addAlbum(self, album):
        if album.name in self.albums:
            raise
        self.albums[album.name] = album
        
    def getAlbum(self, albumname):
        if albumname in self.albums:
            return self.albums[albumname]
        return None
        
        
class Album:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        
    def addTrack(self, track):
        self.tracks.append(track)
        
    def getYear(self):
        highest = 0
        for track in self.tracks:
            try:
                if track.year != None and int(track.year) > highest:
                    highest = track.year
            except:
                pass
            
        return highest

class Track:
    def __init__(self, filename):
        self.filename = filename
        
        self.artist = None
        self.album = None
        self.title = None
        
        self.year = None
        self.track = None
        
        self._loaddata()
        
    def _loaddata(self):
        trackdata = mutagen.File(self.filename, easy=True)
        
        if TagDefinitions.artist[0] in trackdata:
            self.artist = trackdata[TagDefinitions.artist[0]][0]
        
        if TagDefinitions.album[0] in trackdata:
            self.album = trackdata[TagDefinitions.album[0]][0]
            
        if TagDefinitions.title[0] in trackdata:
            self.title = trackdata[TagDefinitions.title[0]][0]
            
        if TagDefinitions.year[0] in trackdata:
            self.year = trackdata[TagDefinitions.year[0]][0]
            
        if TagDefinitions.track[0] in trackdata:
            self.track = trackdata[TagDefinitions.track[0]][0]
            

class CollectionParser:
    def __init__(self, root):
        self.root = root
        self.artistscollection = Collection()
        
        #m is used for mime type reading
        m = magic.open(magic.MAGIC_MIME)
        m.load()
        self.m = m
    
    def parse(self):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                self.addFile(root+"/"+file)

    def addFile(self, filename):
        mimetype = self.m.file(filename)
        
        mimesplit = None
        try:
            mimesplit =  mimetype.split(" ")[0].split("/")
        except:
            print "Detecting of MimeType failed for file", filename
            print "  the mimetype reported is:", mimetype
            return
        
        if mimesplit[0] == "audio":
            try:
                self.addTrack(filename)
            except:
                #print "COULD NOT ADD FILE", filename, "AS TRACK !"
                pass
                
        elif mimesplit[0] == "image":
            #print "IMAGEFILE"
            pass
            
        else:
            #print "UNKNOWN MIMETYPE", mimetype, filename
            pass
    
    
    def addTrack(self, filename):
        trackdata = Track(filename)
        if self.artistscollection.getArtist(trackdata.artist) == None:
            self.artistscollection.addArtist(Artist(trackdata.artist))
        artist = self.artistscollection.getArtist(trackdata.artist)
        
        if artist.getAlbum(trackdata.album) == None:
            artist.addAlbum(Album(trackdata.album))
        album = artist.getAlbum(trackdata.album)
        
        album.addTrack(trackdata)
        
    
x = CollectionParser("/media/MultiMedia/Music/zooi")
x.parse()
print "PRINTING A LIST OF ARTISTS AND THEIR ALBUMS: "
for artist in x.artistscollection.collection:
    try:
        print "* "+x.artistscollection.collection[artist].name+" "
    except:
        print "* ??? **UNICODE ERROR**"
    for albumkey in x.artistscollection.collection[artist].albums:
        album = x.artistscollection.collection[artist].albums[albumkey]
        print "  - ["+str(album.getYear())+"] "+unicode(album.name)
        #try:
        #    print "  - ["+str(album.getYear())+"]"+unicode(album.name)
        #except:
        #    print "  - ??? **UNICODE ERROR**"