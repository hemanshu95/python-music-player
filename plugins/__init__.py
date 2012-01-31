class Plugin():
    def __init__(self, listPlayer=None, listManager=None, collectionManager=None):
        self.listManager = listManager
        self.listPlayer = listPlayer
        self.collectionManager = collectionManager
        self.setup()
        
    def setup(self):
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass