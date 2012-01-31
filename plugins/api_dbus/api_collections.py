import dbus
from dbus_service import DBusService

import simplejson

class API_Collections(DBusService):
    def __init__(self, collectionsmanager):
        DBusService.__init__(self, 'collections')
        self._collectionsmanager= collectionsmanager
        
        
    @dbus.service.method('org.pymp.daemon.collections') 
    def getCollection(self, name):
        name = unicode(name)
        collection = self._collectionsmanager.get_collection(name)
        return simplejson.dumps(collection.serialize_info())


    @dbus.service.method('org.pymp.daemon.collections') 
    def getCollectionTracks(self, name):
        name = unicode(name)
        collection = self._collectionsmanager.get_collection(name)
        return collection.dump_tracks_as_json()


    @dbus.service.method('org.pymp.daemon.collections') 
    def getCollections(self):
        collections_serialized = []
        collections = self._collectionsmanager.get_collections()
        for collection in collections:
            collections_serialized.append(collections[collection].serialize_info())
        
        return simplejson.dumps(collections_serialized)
