signals = {}

def emit(signalname, param = None):
    #print "Emitting signal: "+signalname
    
    if not signalname in signals:
        return
    
    for ob in signals[signalname]:
        for singalmethod in signals[signalname][ob]:
            try:
                if param:
                    singalmethod(param)
                else:
                    singalmethod()
            except Exception as e:
                print "Exception during signal call: "+unicode(e)
        


def connect(signalname, ob, method_to_call):
    if signalname not in signals:
        signals[signalname] = {}
    
    if ob not in signals[signalname]:
        signals[signalname][ob] = []
    signals[signalname][ob].append(method_to_call)
    #else:
    #    raise Exception(ob+" is already connected to signal "+signalname)    
        
        
        
def disconnect(signalname, ob):
    #TODO
    pass
    