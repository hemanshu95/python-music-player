import urllib
import httplib
import simplejson

"""
1.
http://ws.audioscrobbler.com/radio/handshake.php?version=0.1&platform=linux&username=theunknowncylon&passwordmd5=xxx

session=2df8cb9f7e78fc5f9519fb7eb193268e
stream_url=http://195.24.233.49:80/last.mp3?Session=2df8cb9f7e78fc5f9519fb7eb193268e
subscriber=1
framehack=0..
base_url=ws.audioscrobbler.com
base_path=/radio
info_message=
fingerprint_upload_url=http://ws.audioscrobbler.com/fingerprint/upload.php
permit_bootstrap=0
freetrial=0




2.
http://ws.audioscrobbler.com/radio/adjust.php?session=2df8cb9f7e78fc5f9519fb7eb193268e&url=lastfm%3A%2F%2Fuser%2Ftheunknowncylon%2Fpersonal

response=OK
url=http://www.last.fm/listen/user/TheUnknownCylon/personal
stationname=TheUnknownCylon's Library Radio


3.
http://ws.audioscrobbler.com/radio/xspf.php?sk=2df8cb9f7e78fc5f9519fb7eb193268e&discovery=0&desktop=0


"""

import md5

class LastFMHelper():
    
    API_KEY = "67a78084d70872d245b466e9baced58d"
    API_SECRET = "0fab33a507343cf73697852f77d30590"
    
   
    '''Step one in the authentication process.'''
    def get_token(self):
        response = self.apicall("auth.getToken", {})
        return response['token']


    '''Step two in the authentication process.'''
    def get_authorization_uri(self, token):
        return "http://www.last.fm/api/auth/?api_key="+self.API_KEY+"&token="+token
    
    
    '''Fetch a session key for a user. The third step in the authentication process.
    @param token: Token retrieved in step one, which is authorized by the user in step two.''' 
    def get_session_key(self, token):
        response = self.apicall("auth.getSession", {'token': token})
        return response['session']['key']
    

    '''Sets the sessionkey. The sessionkey is retrieved by calling get_session_key,
    and should be stored somewhere on disk. The key has a life-time validity, but
    storing this key is not handled by this class!
    @param sessionkey: Users sessionkey'''
    def set_session_key(self, sessionkey):
        self._sessionkey = sessionkey
    
    
    
    '''Do a method call which requires no authentication to the last.fm API'''
    def apicall(self, method, methodparams):
        params = {'method' : method,
                  'api_key' : LastFMHelper.API_KEY,
                  'format'  : 'json',
                  'method'  : method}
        
        
        for paramkey in methodparams:
            params[paramkey] = methodparams[paramkey]
        
        #sign the call
        params['api_sig'] = self._calculate_sign(params)
    
        header = {"user-agent" : "pymp/1.0",
                  "Content-type": "application/x-www-form-urlencoded"}
        
        
        lastfm = httplib.HTTPConnection("ws.audioscrobbler.com")
        
        params_encoded = urllib.urlencode(params)
        lastfm.request("POST","/2.0/?", params_encoded, header)
                
        response = lastfm.getresponse()
        return simplejson.loads(response.read())
    

    '''Do a method call which requires authentication to the last.fm API'''
    def apicallauth(self, method, methodparams):
        #add the sessionkey to the method parameters
        if not self._sessionkey:
            raise Exception("Sessionkey has to be set before calling methods which require authentication.")
        
        methodparams['sk'] = self._sessionkey
        return self.apicall(method, methodparams)
        
    
    '''This function will calculate the sign value for the method call.
    This is based on the parameters'''
    def _calculate_sign(self, parameters):
        
        signature = ""
        for key in sorted(parameters):
            if key!="format" and key!="callback":
                signature = signature + key + parameters[key]
    
        signature = signature + LastFMHelper.API_SECRET
    
        return md5.md5(signature).hexdigest()


    def loadSessionKeyFromFile(self):
        import constants
        try:
            f = open(constants.config_dir+"/lastfm")
            sessionkey = f.readline()
            f.close()
        except:
            raise Exception("No sessionkey found!")
        self.set_session_key(sessionkey)


class Scrobbler():
    def __init__(self):
        lastfm = LastFMHelper()
        lastfm.loadSessionKeyFromFile()
        self._lastfm = lastfm
        
        
    def informplaying(self, track):
        info = self._scrobbleinfo(track)
        if info == None: return
        
        self._lastfm.apicallauth('track.updateNowPlaying', info)
        
        
    def scrobble(self, track, timestamp):       
        info = self._scrobbleinfo(track)
        if info == None: return
        
        info['timestamp'] = timestamp
        
        self._lastfm.apicallauth('track.scrobble', info)
        
        
    def _scrobbleinfo(self, track):
        uk = "<Unknown>"
        
        # We can only scrobble tracks with at least artist and title field set
        if not track.title or not track.artist or track.title==uk or track.artist==uk:
            return
        
        info = {'track': track.title, 'artist': track.artist}
        if track.album and track.album != uk:
            info['album'] = track.album
        if track.length:
            info['duration'] = str(int(track.length)) # in seconds!

        return info


'''Last.fm radio relies (for now) on the older last.fm API'''
class Radio():
    def __init__(self):
        lastfm = LastFMHelper()
        lastfm.loadSessionKeyFromFile()
        self._lastfm = lastfm
    
    def tune(self, stationuri):
        self._lastfm.apicallauth('radio.tune', {'station': stationuri})
    
    def getTracks(self):
        playlist = self._lastfm.apicallauth('radio.getPlaylist', {'bitrate': '128', 'speed_multiplier':'2.0' })
        tracks = self.playlist2tracks(playlist)
        return tracks
    
    def playlist2tracks(self, playlist):
        '''Parses the last.fm tracks response (json format), and returns Track-objects back.'''
        import dataobjects

        tracks = []
        for track in playlist['playlist']['trackList']['track']:
            title = track['title']
            album = track['album']
            artist = track['creator']
            uri = track['location']
            length = int(track['duration']) / 1000 # ms to seconds
            
            t = dataobjects.Track(uri)
            t.album = album
            t.artist = artist
            t.title = title
            t.length = length
            
            tracks.append(t)
            
        return tracks
