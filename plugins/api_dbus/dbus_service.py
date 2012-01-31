import dbus

class DBusService(dbus.service.Object):
    def __init__(self, buskey):
        self._buskey = buskey
    
    def dbus_start(self, bus_name):
        dbus.service.Object.__init__(self, bus_name, '/org/pymp/daemon/'+self._buskey)
