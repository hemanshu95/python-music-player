#! /usr/bin/python2

import sys
import dbus
import simplejson
import dataobjects
import pprint


#get the commandline arguments
args = sys.argv[1:]

if len(args) == 0:
    print "No arguments provided.\n"
    sys.exit(0)


#Communicate to pymp daemon over dbus

bus = dbus.SessionBus()

def service_collection(methodname):
    service = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/collections')
    method = service.get_dbus_method(methodname, 'org.pymp.daemon.collections')
    return method

    
def service_lists(methodname):
    service = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/lists')
    method = service.get_dbus_method(methodname, 'org.pymp.daemon.lists')
    return method


def service_player(methodname):
    service = bus.get_object('org.pymp.daemon', '/org/pymp/daemon/player')
    method = service.get_dbus_method(methodname, 'org.pymp.daemon.player')
    return method

   
#Tune in to last.fm
if args[0] == "tune":
    station = args[1]
    
    init_list_meth = service_lists('newList')
    init_list_meth('last.fm', station)
    
    print "Tuned PyMP to "+station
    
    if not(len(args)>=3) or args[2] != "False":
        set_player_list = service_player('set_list')
        set_player_list(station)
        
        play_meth = service_player('play')
        play_meth()


if args[0] == "newlist":
    if not len(args) > 2:
        #Print all available list types
        print "Create a new list with: newlist <listtype> <name>"
        print ""
        print "Availble list types:"
        
        listtypes = service_lists('getListTypes')()
        for ltype in simplejson.loads(str(listtypes)):
            print " * "+ltype
        
    else:
        listtype = args[1]
        listname = args[2]
        
        service_lists('newList')(listtype, listname)

        
#Lists
if args[0] == "lists":
    if not len(args) > 1:
        #print a list of all collections
        lists = simplejson.loads(str(service_lists('getLists')()))
        
        print "Currently the following lists are available:"
        for playlist in lists:
            print "  * "+ playlist['name']
        print ""
        
    else:
        listname = args[1]
        getTracks = service_lists('getTracks')

        action = "tracks"
        if len(args) > 2:
            action = args[2]
        
        if action == "tracks":
            ##TODO: None, None seems not allowed with dbus... 0 999 hack instead.
            tracks = simplejson.loads(str(getTracks(listname, 0, 999)))
        
            for track in tracks:
                print track[1]['title'] + " by " + track[1]['artist']
                
        elif action == "addtrack":
            if not len(args) > 3:
                print "usage: lists <listname> addtrack <filename>"
            else:
                track = args[3]
                print "ADDING TRACK: "+track
                service_lists('addFileAsTrack')(listname, track)
        
        
        

if args[0] == "player":
    if args[1] == "play":
        method = service_player('play')
        method()
        
    elif args[1] == "stop":
        method = service_player('stop')
        method()
        
    elif args[1] == "next":
        method = service_player('nextTrack')
        method()
        
    elif args[1] == "prev":
        method = service_player('prevTrack')
        method()
   
    elif args[1] == "setlist":
        method = service_player('set_list')
        method(args[2])
        
        
if args[0] == "play":
    track = args[1]
    method = service_player('set_track')
    method(track)

    
if args[0] == "queue":
    track = args[1]
    method = service_player('queue_track')
    method(track)