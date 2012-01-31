
## NOTE: This file is only for testing, learning and expirimenting
##       Once the PyMP daemon is more robust etc, this file will be implemented
##       in a more correct way from software design perspective :)

import urwid

import simplejson
import pprint

from music_collections.MusicCollection import FullMemoryCollection  
from curses_misc import SelText

import dataobjects

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

collecionService = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/collections')
dbusGetCollections = collecionService.get_dbus_method('getCollections', 'org.pymp.daemon.collections')
dbusCollectionGet = collecionService.get_dbus_method('getCollectionTracks', 'org.pymp.daemon.collections')


collecionService = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/lazylist')
dbusPlayListaddTracks = collecionService.get_dbus_method('addTracks', 'org.pymp.daemon.lazylist')

def api_signal_track_added(list_id, track_id, track_json):
    list_id = unicode(list_id)
    track_id = int(track_id)
    track_json = simplejson.loads(unicode(track_json))
    
    track = dataobjects.Track(None)
    track.load(track_json)
    tc.addTrack(list_id, track_id, track)

    

listsService = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/lists')
listsService.connect_to_signal('api_signal_track_added', api_signal_track_added)

name = "MultiMedia"
collectionname = "WesternDigital Disc"
x = FullMemoryCollection(name, collectionname, False)
x.load_tracks_as_json(dbusCollectionGet(name))

#Holds all collections for now :)
collections = simplejson.loads(unicode(dbusGetCollections()))

playerservice = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/player')
api_player = dbus.Interface(playerservice, dbus_interface='org.pymp.daemon.player')

#
#x = SmallMediumFileCollection("/media/MultiMedia/Music/")
def getArtistList():
    artists = x.getArtists()
    artistslist = []
    
    artistskeys = artists.keys()
    artistskeys.sort()
    
    for artist in artistskeys:
        artistslist.append(ListItem(artists[artist].getName(), artists[artist]))
    
    return artistslist

##################

"""ListItem is a special item for a urwid List.
 It allows items in the list to be selected and focussed."""
class ListItem(urwid.WidgetWrap):
    """caption: Label to be displayed,
    userobject: Optional object which can be retrieved from the item later on"""
    def __init__(self, caption, userobject=None, captionIsWidget=False):
        self.captioniswidget = captionIsWidget
        
        if not self.captioniswidget:
            caption = unicode(caption)
            self._text = SelText(caption, wrap="clip")
            self._w = urwid.AttrWrap(self._text, None, 'focus')
        else:
            self._w = urwid.AttrWrap(caption, None, 'focus')
        
        self.caption = caption
        
        self.__super.__init__(self._w)
        self.userobject = userobject        

    def selectable(self):
        return True
    
    
    def keypress(self, size, key):
        return key
    
    
class ColumedListItem(ListItem):
    def __init__(self, list_of_values, userobject):
        
        textstr = ""
        
        for item in list_of_values:
            pprint.pprint("---------------------")
            pprint.pprint(item)
            strpart = " "+item['value'].text
            textstr = textstr + strpart
        ListItem.__init__(self, textstr, userobject)
        
        #self.values = []
        
        #for item in list_of_values:
            #cell = ('fixed', item['length'], urwid.AttrWrap(item['value'], 'focus', 'focus')) 
            #self.values.append(cell)
            
        #w = urwid.Columns(self.values)
            
        #ListItem.__init__(self, w, userobject, True)


"""Extention of urwid Pile for a column, it takes one listbox
 and a callback function. It watches the given list for changes
 in focus and selected item. It will inform the callback when
 these changes occur."""
class ColumnPile(urwid.Pile):
    def __init__(self, pileitems, listbox, callback, highlight_on_focus_lose=False):
        self.__super.__init__(pileitems)
        self._listbox = listbox
        self._callback = callback
        self._has_focus = False
        self._selecteditem = None
        self._highlight_on_focus_lose = highlight_on_focus_lose
    
    def render(self, size, focus=False):
        if focus:
            if self._selecteditem != None:
                self._selecteditem._w.set_attr_map({None: None})
            
            selecteditem = self._listbox.get_focus()
            if selecteditem[0] == None:
                self._selecteditem = None
            else:
                self._selecteditem = selecteditem[0]
            self._itemchanged()
            
        if focus and not self._has_focus:
            self._has_focus = True
            self._callback.gotFocus()
        elif not focus and self._has_focus:
            self._has_focus = False
            self._callback.lostFocus()
            
        return self.__super.render(size, focus)
    
    
    '''Hack to work around Urwid-bug:
      http://excess.org/urwid/ticket/66
    '''
    def rerender(self):
        #TODO: This does not work!
        self.item_types.append(('flow', None))
        #self.keypress((1, 1), "x") 
        pass
    
    
    def keypress(self, size, key):
        if key == "enter":
            self._callback.itemSelected(self._selecteditem)
        return self.__super.keypress(size,key)

    
    def _itemchanged(self, item = None):
        if item:
            self._selecteditem = item
            
        if self._selecteditem != None:
            if self._highlight_on_focus_lose:
                self._selecteditem._w.set_attr_map({None: 'focus_selected'})
            self._callback.itemChanged(self._selecteditem)

    
class Column():
    def __init__(self, header, items, highlight_on_focus_lose=False):
        self._header = header
        self._items = items
                
        self._headertext = urwid.Text(self._header, align='left')
        self.ur_header = urwid.AttrMap(urwid.Filler(self._headertext), 'col_header')
        
        self.ur_listwalker = urwid.SimpleListWalker(items)
        self.ur_list   = urwid.ListBox(self.ur_listwalker)
        self.ur_pile   = ColumnPile([
            ('fixed', 1, self.ur_header),    #header of 1 px height
            self.ur_list                     
            ], self.ur_list, self, highlight_on_focus_lose)
    
    
    def changeListItems(self, items):
        self._items = items
        self.ur_listwalker[:] = items
        self.ur_pile._itemchanged(items[0])
        self.itemChanged(items[0])
        
    def appendItem(self, item):
        self.ur_listwalker.append(item)
        self.ur_pile.rerender() 
    
    def get_urwid_pile(self):
        return self.ur_pile
    
    def itemChanged(self, item):
        pass
    
    def itemSelected(self, item):
        pass    
    
    def gotFocus(self):
        pass
    
    def lostFocus(self):
        pass
    
    def focusChanged(self):
        pass
    
    
class ArtistColum(Column):
    def __init__(self, header, items, albumcolumn):
        self.albumcolumn = albumcolumn
        Column.__init__(self, header, items, True)
        
    """Different artist was selected, let's update
    the albums-list."""
    def itemChanged(self, item):
        artist = item.userobject
        albums = artist.getAlbums()
        
        #generate nice album displaynames
        albumnsbynameames = {}
        for albumkey in albums:
            album = x._albums[albumkey]
            #format albumname
            albumyear = album.getYear()
            if albumyear == None:
                albumyear = "    "
            albumname = unicode(albumyear) + " " + album.title
        
            albumnsbynameames[albumname] = album
        
        
        alist = []
        for albumname in sorted(albumnsbynameames, reverse=True):
            album = albumnsbynameames[albumname]
                        
            #create new listitem and append it to the list of albums
            alist.append(ListItem(albumname, album))
        
        
        self.albumcolumn.changeListItems(alist)
        return


class AlbumColumn(Column):
    def __init__(self, header, items, trackscolumn):
        self._trackscolumn = trackscolumn
        Column.__init__(self, header, items, True)
        
    def itemChanged(self, item):
        album = item.userobject
        
        tracks = album.tracks
        #generate nice track displaynames
        tracks.sort()
        
        tlist = []
        for track in sorted(tracks, key=lambda t: int(t.tracknumber)):
            trackname = track.title
            if track.tracknumber != None and track.tracknumber != 0:
                trackname = str(track.tracknumber)+". "+trackname
            tlist.append(ListItem(trackname, track))
            
        self._trackscolumn.changeListItems(tlist)
        
        
class TracksColumn(Column):
    def __init__(self, header, items):
        Column.__init__(self, header, items)
    
    
    def itemSelected(self, item):
        track = item.userobject
        
        #add the track to the playlist
        tracks_to_add = simplejson.dumps([track.serialize()])
        
        dbusPlayListaddTracks(tracks_to_add)











class lTrack:
    def __init__(self, uid, track):
        self.uid = uid
        self.track = track




class TracklistColumn(Column):
    def __init__(self, header, items):
        Column.__init__(self, header, items)

    def itemSelected(self, item):
        #item.userobject is a lTrack object
        ltrack = item.userobject
        api_player.playTrack(ltrack.uid)

        


def getCurrentPlaylist():
    list_id = api_player.get_list()
    if list_id == None:
        return []

    tracks = []

    #get tracks on the list in order
    jsontracks = listsService.get_dbus_method('getTracks', 'org.pymp.daemon.lists')(list_id, 0, 0)
    for jsontrackstruct in simplejson.loads(unicode(jsontracks)):
        #jsontrackstruct: (track_uid, track_data)
        track = dataobjects.Track(None)
        track.load(jsontrackstruct[1])
        track_uid = int(jsontrackstruct[0])
        tracks.append(lTrack(track_uid, track))
        
    return tracks


def getPlayLists():
    lists = listsService.getLists()
    return simplejson.loads(unicode(lists))











class CollectionsColumn(Column):
    def __init__(self, header, items, artistscolumn):
        self._artistscolumn = artistscolumn
        Column.__init__(self, header, items, True)
        
    def itemChanged(self, item):
        pass
#        album = item.userobject
#        
#        tracks = album.tracks
#        #generate nice track displaynames
#        tracks.sort()
#        
#        tlist = []
#        for track in sorted(tracks, key=lambda t: int(t.tracknumber)):
#            trackname = track.title
#            if track.tracknumber != None and track.tracknumber != 0:
#                trackname = str(track.tracknumber)+". "+trackname
#            tlist.append(ListItem(trackname, track))
#            
#        self._trackscolumn.changeListItems(tlist)
        
        
class CollectionsBrowser():
    def __init__(self, collections):
        self._collections = collections
    
    def getCollectionsPile(self):
        #build an array of listitems
        items = []
        items.append(ListItem("All collections", None))
        for mcollection in self._collections:
            items.append(self._collections[mcollection].name, self._collections[mcollection])
        
        #Now create a column object
        column = CollectionsColumn("Collections", items)
        return column.get_urwid_pile()


































def get_fb_collections():
    #Colums
    artistlist = getArtistList()
        
    c3        = TracksColumn("Tracks", [])
    c2        = AlbumColumn("Albums",  [], c3)
    c1        = ArtistColum("Artists", artistlist, c2)
        
    fb_collections = urwid.Columns( [c1.get_urwid_pile(), c2.get_urwid_pile(), c3.get_urwid_pile()], 3 )
    return fb_collections
    

#TODO: Support multiple tracklists :)
class TrackListsManager:
    
    def __init__(self):
        self.listsColumn = None
        self.__init__listscolumn()
        
        self.tracklistscolumn = None
        self.__init__tracklistcolumn()
   
   
    def _build_item(self, lTrack):
        track = lTrack.track
        try:
            tracklength = int(track.length) / 60
            tracklengthseconds = int(track.length % 60)
            length = "%(minutes)d:%(seconds)02d" % {'minutes': tracklength, 'seconds': tracklengthseconds}
        except:
            length = unicode(track.length)
        
        
        columns = []
        #column one: track length
        columns.append({'length': 10, 'value': urwid.Text(length)})
        
        #column two: track title
        columns.append({'length': 35, 'value': urwid.Text(track.title)})
        
        #column three: artist
        columns.append({'length': 35, 'value': urwid.Text(track.artist)})
        
        #column four: album
        columns.append({'length': 35, 'value': urwid.Text(track.album)})
        
        return ColumedListItem(columns, lTrack)


    def _build_listitem(self, serializedlist):
#        serializedlist["value"] = serializedlist['name']
#        pprint.pprint(serializedlist)
#        return ColumedListItem(serializedlist['name'], serializedlist)
        return ColumedListItem([{'value': urwid.Text(serializedlist['name'])}], serializedlist)
        
        

    def _track_to_string(self, track):
        tracklength = int(track.length) / 60
        tracklengthseconds = int(track.length) % 60
        length = " %(minutes)d:%(seconds)02d" % {'minutes': tracklength, 'seconds': tracklengthseconds}
        return length+" "+track.title


    
    def __init__tracklistcolumn(self):
        #textBody = urwid.Text("Lorem ipsum dolor...\n\nHier moet een lange lijst van muziek komen :)")
        #fill = urwid.Filler(textBody, 'top')
        
        listitems = []
        tracks = getCurrentPlaylist()   #object is a tracks = lTrack
        for i in range(0, len(tracks)):
            listitem = self._build_item(tracks[i])
            listitems.append(listitem)
        
        tracklistcolumn = TracklistColumn("Track", listitems)

        self.tracklistcolumn = tracklistcolumn


    def __init__listscolumn(self):
        listitems = []
        alllists = getPlayLists()

        pprint.pprint(alllists)
        for i in range(0, len(alllists)):
            listitem = self._build_listitem(alllists[i])
            listitems.append(listitem)
        
        thecolumn = Column("PlayLists", listitems)
        self.listsColumn = thecolumn
        



    ### Frame body: tracklistbrowser 
    def get_fb_tracklist(self):
        return self.tracklistcolumn.get_urwid_pile()


    def addTrack(self, tracklist, track_id, track):
        ltrack = lTrack(track_id, track)
        listItem = self._build_item(ltrack)
        self.tracklistcolumn.appendItem(listItem)
        

    


tc = TrackListsManager()

#Init framebodies
fb_collections = get_fb_collections()
fb_tracklist = tc.get_fb_tracklist()


#Define main Frame
textHeader = urwid.Text(('frame_header', "PyMP -- Python Music Player"), align='right')
textFooter = urwid.Text(('frame_footer' ,"You can not quit yet!"))
footerMap = urwid.AttrMap(textFooter, 'frame_footer')
footer = urwid.Pile([footerMap])

frame = urwid.Frame(fb_collections,header=urwid.Pile([textHeader]),footer=footer)


palette = [ 
    ('frame_header'   , 'light blue'  , 'default'),
    ('frame_footer'   , 'light gray'  , 'dark blue'),
    ('body'           , 'default'     , 'default'),
    ('focus'          , 'black'       , 'light gray'),
    ('focus_selected' , 'default'     , 'dark gray'),
    ('col_header'     , 'black'       , 'dark green'),
]

def global_key_press(key):
    try: key = key.lower()
    except: pass    #mouse click
    
    if key=="p":
        api_player.play()
                
    if key=="o":
        api_player.pause()

    if key=="i":
        api_player.stop()

    if key=="n":
        api_player.nextTrack()

    if key=="b":
        api_player.prevTrack()
        
    if key=="1":
        frame.set_body(fb_collections)
        
    if key=="2":
        frame.set_body(fb_tracklist)

    if key=="esc":
        raise urwid.ExitMainLoop()


#loop = urwid.MainLoop(frame, palette, unhandled_input=global_key_press)
#loop.run()
urwid_loop = urwid.MainLoop(frame, palette, screen=urwid.raw_display.Screen(),  unhandled_input=global_key_press, event_loop=urwid.GLibEventLoop())


#import gobject
#loop = gobject.MainLoop()
urwid_loop.run()

print "Thank you for using PyMP!\n"

