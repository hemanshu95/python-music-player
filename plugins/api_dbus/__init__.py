
import dbus
import dbus.service

from dbus.mainloop.glib import DBusGMainLoop

# Data transfered over dbus is done in JSon
import simplejson

import dataobjects
import player
import music_lists.MusicList

from plugins import Plugin

from api_collections import API_Collections
from api_lazylist import API_LazyList
from api_lists import API_Lists
from api_player import API_Player


info = {
        'class': "APIDbus",
        'author': "Remco van der Zon",
        'description': "Provides access from other applications over dbus."
}


class APIDbus(Plugin):
    def __setup__(self):
        pass
    
    def start(self):
        listmanager = self.listManager
        listplayer = self.listPlayer
        collectionsmanager = self.collectionManager
        
        # initialize dbus
        DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName('org.pymp.daemon', bus=dbus.SessionBus())
 
        # Load the API classes       
        player = API_Player(listmanager, listplayer)
        player.dbus_start(bus_name)

        lists = API_Lists(listmanager)
        lists.dbus_start(bus_name)

        lazylists = API_LazyList(listmanager, listplayer)
        lazylists.dbus_start(bus_name)
        
        collections = API_Collections(collectionsmanager)
        collections.dbus_start(bus_name)


    def stop(self):
            pass