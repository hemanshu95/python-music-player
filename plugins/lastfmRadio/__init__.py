import os
import time
from patterns import signals
from dataobjects import Track
from plugins import Plugin
import simplejson

from music_lists.MusicList import MusicList

import lastfm

info = {'class': "lastfmRadio", 'author': "Remco van der Zon"}

class lastfmRadio(Plugin):    
    def setup(self):
        lastfm.Radio()
    
    def start(self):
        self.listManager.registerNewListType("last.fm", LastFMList)

    def stop(self):
        self.listManager.deregisterNewListType("last.fm")
        


class LastFMList(MusicList):
    '''Special playlist for Last.fm radio stations
    
    Last.fm radio streams will provide you with MP3s which needs to be download
    in a specific order. Skipping is allowd, but seeking, storing and go to
    previous tracks is not by the last.fm licence.'''
    def __init__(self, station):
        name = station
        
        self._lastfmradio = lastfm.Radio() 
        
        MusicList.__init__(self, name)
        
        self._tuned = False
        self._radiouri = station
        self._lastfmqueue = []
        self._fill_lastfm_queue()
    
    
    def addTrack(self):
        raise Exception("Can not add manually tracks to last.fm list.")
        
    
    def getTrack(self, index):
        if index == 0 and self._tracks.length() == 0:  #If no track has been loaded, bootstrap the list
            self.getNextTrackIndex()
        
        return MusicList.getTrack(self, index)
    
    
    '''Special implementation, we can assume that we are
    always listening the latest track, so index doesn't matter.
    Fetch a new track from the last.fm queue and add it to the playlist.'''
    def getNextTrackIndex(self, index=None):
        assert len(self._lastfmqueue) > 0
        
        #don't care for the current track, just get the next one
        track = self._lastfmqueue.pop(0)
        
        #TODO: Make sure that the given track is still valid
        # i.e. we are still allowed to download it, given its validty timestamp
        
        #Make sure we add tracks to the last-fm queue in time
        if len(self._lastfmqueue) < 2:
            self._fill_lastfm_queue()
        
        #Play the new track: add it to the playlist
        track_id = MusicList.addTrack(self, track) #Bypass our own addTrack impl, use supers impl. instead!
        
        return track_id


    def _fill_lastfm_queue(self):
        # Make sure we are tuned to the radio station!        
        if self._tuned == False:
            self._lastfmradio.tune(self._radiouri)
            self._tuned = True
            
        # get some (5) tracks from last.fm and append them to the queue
        tracks = self._lastfmradio.getTracks()
        for track in tracks:
            self._lastfmqueue.append(track)
            
            
            
#    '''Addtrack with a track. Tuning to anohter radio station
#    can be done by calling this method with a last-fm 'track',
#    i.e. a valid last.fm uri should be in the uri-field of the track.''' 
#    def addTrack(self, track):
#        #Tuning to a(nother) radio station...
#        if track.uri[0:9].lower() == "lastfm://":
#            self._radiouri = track.uri
#            self._lastfmqueue = []
#            self._tuned = False
#            
#            self._fill_lastfm_queue()
#            
#            pass
#        else:
#            #Only lastfm radio's supported
#            #TODO: Support for adding tracks to the radio
#            #      But... these tracks will not be able to be skipped
#            raise Exception("Last.fm list only supports last.fm radio streams.")

