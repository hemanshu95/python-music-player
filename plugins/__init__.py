class Plugin():
    def __init__(self, queueplayer=None, queue=None, listManager=None, collectionManager=None):
        self.listManager = listManager
        self.queueplayer = queueplayer
        self.queue = queue
        self.collectionManager = collectionManager
        self.setup()
        
    def setup(self):
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass