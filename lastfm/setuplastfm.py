#!/usr/bin/python2
import time
import sys

print "This little utility will connect your last.fm account with PyMP."
print " You can quit this wizard anytime by hitting CONTROL + C."
print ""

from lastfm import LastFMHelper
lastfmhelper = LastFMHelper()

token = lastfmhelper.get_token()
uri = lastfmhelper.get_authorization_uri(token)

try:
    import webbrowser
    webbrowser.open_new(uri)
except:
    #nice try ;)
    pass

#CLI Browsers may clear the screen after closing, so
# put this message after trying to open a browser
print "The wizzard will now try to open your browser where you can grant"
print "permissions to PyMP."
print ""
print "If no web page shows up, please visit the following link to connect"
print "PyMP to your last.fm account."
print "  "+uri
print ""

while True:
    try:
        sessionkey = lastfmhelper.get_session_key(token)
        print ""
        print "Got the following SessionKey: "+sessionkey
        break
    except:
        try:
            time.sleep(5)
            print ".",
            sys.stdout.flush()        
        except:
            print ""
            print "Error: Got no sessionkey from last.fm."
            print "       Did you follow the link and granted permissions correctly?"
            print "       Please restart this wizard to try again!"
            print ""
            sys.exit(0)


import constants
f = open(constants.config_dir+"/lastfm", "w")
f.write(sessionkey)
f.close()

print ""
print "Connected succesfully."
print "Thank you for using PyMP! You can now scrobble tracks or, if you are"
print "a subscribed last.fm user, play last.fm radio."
print ""
