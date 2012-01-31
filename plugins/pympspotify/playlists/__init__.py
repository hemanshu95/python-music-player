import spotify
from spotify.manager import SpotifyPlaylistManager, SpotifyContainerManager

from spotifyplaylist import SpotifyPlaylist 

class PympSpotifyPlaylists():
    def __init__(self, pympListManager, playlistcontainer):
        self._pympListManager = pympListManager
        
        self._playlistcontainer = playlistcontainer
        
        self.playlistcontainermanager = PympSpotifyPlaylistContainerManager(self)
        self.playlistcontainermanager.watch(self._playlistcontainer)


    def addSpotifyPlayList(self, playlist):
        newlist = SpotifyPlaylist(playlist.name())
        for track in playlist:
            newlist.addTrack(self.spotifyTrack2PympTrack(track))
        try:
            self._pympListManager.add_list(newlist)
        except:
            pass


    def spotifyTrack2PympTrack(self, sptrack):
        from dataobjects import Track
                
        uri = unicode(spotify.Link().from_track(sptrack, 0))
        
        t = Track(uri)
        t.artist = sptrack.album().artist().name()
        t.album = sptrack.album().name()
        t.title = sptrack.name()
        t.length = int(sptrack.duration()) / 1000
        t.year = sptrack.album().year()
        t.tracknumber = sptrack.index()
                
        return t
        

class PympSpotifyPlaylistContainerManager(SpotifyContainerManager):

    def __init__(self, pympspotifyplaylists):
        SpotifyContainerManager.__init__(self)
        self._pympspotifyplaylists = pympspotifyplaylists

    def container_loaded(self, c, u):
        print 'Container loaded !' #and thus all playlists!
        # The container has finished loading, we can loop over all playlists
        #  in the container now and create PyMP playlists for each Spotify
        #  playlist.
        print "Going to register all lists to pymp!"
        for playlist in c:
            self._pympspotifyplaylists.addSpotifyPlayList(playlist)
        print "Done doing the registration of lists to pymp."
        
    def playlist_added(self, c, p, i, u):
        #print "Spotify: Playlist added"
        pass
        
        
    def playlist_moved(self, c, p, oi, ni, u):
        #print 'Container: playlist "%s" moved.' % p.name()
        pass


    def playlist_removed(self, c, p, i, u):
        #print 'Container: playlist "%s" removed.' % p.name()
        pass