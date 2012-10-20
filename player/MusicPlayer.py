from patterns.Observable import Observable

import gst # gstreamer
import sys

'''
PlayBin2: 
  http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-playbin2.html
'''
class Playbin2:
    '''Initilaizes a Gstreamer Playbin2 object,
    which will handle the actual audio playing for use.
    http://ubuntuforums.org/showthread.php?t=1579725
    
    As an argument it takes any (PyMP) MusicPlayer object.
    '''  
    def __init__(self, musicplayer):
        self.idle = True # not playing at the moment
        
        #Store the musicplayer element, so we can inform
        # it later when certain events occur.
        self._musicplayer = musicplayer
        
        # create a playbin2 pipe
        self.player = gst.element_factory_make("playbin2", "player")

        # we are interested in some signals which are not send over the bus
        self.player.connect('about-to-finish', self.about_to_finish) #~ 1 sec. for EOS 
        

        # connect a signal handler to it's bus
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.idle = True
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print >> sys.stderr, "Error: {0} {1}".format(err, debug)
            self.player.set_state(gst.STATE_NULL)
            self.idle = True
        
            
        if self.idle == True:
            self._musicplayer._trackfinished()
            
        return self.idle


    def about_to_finish(self, signal=None, bla = None):
        self._musicplayer._trackAlmostFinished()
        

    def play(self, stream):
        # abort previous play if still busy
        if not self.idle:
            print >> sys.stderr, 'audio truncated'
            self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", stream)
        self.player.set_state(gst.STATE_PLAYING)
        self.idle = False # now playing
    
    
    def resume(self):
        self.player.set_state(gst.STATE_PLAYING)
    
    
    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.idle = True
        
        
    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.idle = True
















#abstract
class MusicPlayer(Observable):
    TRACKFINISHED = 0
    TRACKALMOSTFINISHED = 1
    
    def __init__(self):
        Observable.__init__(self)
    
    
    def play(self, track):
        raise NotImplementedError
    
    def pause(self):
        raise NotImplementedError
    
    def resume(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    

    
    
    '''Returns True iff we are playing (or pausing) a track...'''
    def isPlaying(self):
        return False
    
    
    '''Should be called when a MusicPlayer has finished playing
    the current track. It will notify any observer, so they can undertake
    some action, such as starting a new track.'''
    def _trackfinished(self):
        self.notify(message=MusicPlayer.TRACKFINISHED)
    
    
    '''Should be called by a MusicPlayer implementation when
    a track is almost finished, so other instances can prepare
    the next one.'''
    def _trackAlmostFinished(self):
        #TODO: Move to QueuePlayer signals.emit("player.trackalmostfinished")
        self.notify(message=MusicPlayer.TRACKALMOSTFINISHED)

    
    '''Should be called by a MusicPlayer implementation when
    a new track has been detected. This is usually the case within
    a music stream, when one song has stopped and the next one has been
    started.'''
    def _newTrackDetected(self):
        self.notify()


class GStreamerPlayer(MusicPlayer):
    def __init__(self):
        MusicPlayer.__init__(self)
        self._player = None
        self._paused = False
        
    def play(self, track):
        #Try to stop the current player
        try:
            self._player.stop()
        except:
            pass
        
        assert track != None
        
        #Print a nice line of the current playing song
        playstr = "Playing: "
        if track.title != None and track.artist != None and track.artist != "<Unknown>":
            playstr = playstr+track.title + " by " + track.artist 
        else:
            playstr = playstr + track.uri
        print playstr
        
        
        #create a playbin2 (gstreamer) player, with us as
        # parameter, so it can inform us on certain events.
        self._player = Playbin2(self)
        
        self._player.play(track.uri)
    
    
    def pause(self):
        if self._player:
            self._player.pause()
            self._paused = True
    
    
    def resume(self):
        if self._player:
            self._paused = False
            self._player.resume()
    
    
    def stop(self):
        if self._player: 
            self._player.stop()  
    
    