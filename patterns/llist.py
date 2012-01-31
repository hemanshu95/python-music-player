class LLNode:
    def __init__(self, uid, data):
        self.uid = uid
        self.data = data
        
        self.next = None
        self.prev = None


class LList:
    def __init__(self):
        self.firstNode = None
        self.lastNode = None
     
        #Each node gets an unique id, also keep track of all known nodes!
        self._counter = 0
        self._nodes = {}
        
        
    def _getNewNode(self, data):
        node = LLNode(self._counter, data)
        assert node.uid not in self._nodes
        self._nodes[node.uid] = node
        self._counter = self._counter + 1
        return node


    def _getNode(self, uid):
        uid = int(uid)
        return self._nodes[uid]
    
    
    '''Returns the data for the node at the given uid'''
    def getData(self, uid):
        return self._getNode(uid).data
    
    
    '''Returns the uid for the node after the node at the given uid'''
    def getNext(self, uid):
        node = self._getNode(uid)
        if node.next == None:
            return None
        return node.next.uid
    
    
    '''Returns the uid for the node before the node at the given uid'''
    def getPrev(self, uid):
        node = self._getNode(uid)
        if node.prev == None:
            return None
        return node.prev.uid
    
    
    '''Returns an ordered list of all node indeces'''
    def getNodes(self):
        l = []
        node = self.firstNode
        while node != None:
            l.append(node.uid)
            node = node.next 
        return l
    

    '''Appends a new value at the end of the list,
    returns the uid for the new node and value.'''
    def append(self, nodedata):
        node = self._getNewNode(nodedata)
        
        if self.firstNode == None:
            assert self.lastNode == None
            self.firstNode = node

        else:
            assert self.lastNode != None
            assert self.lastNode.next == None
            prevNode = self.lastNode
            prevNode.next = node
            node.prev = prevNode
            
        self.lastNode = node
        
        return node.uid
        
    
    def insert(self, uid, nodeddata):
        aNode = self._getNode(uid)
        bNode = aNode.next # aNode -X-> bNode
        
        #if the next node == None, use the append function to append the node
        if bNode == None:   
            return self.append(nodeddata)

        aNewNode = self._getNewNode(nodeddata)
        aNode.next = aNewNode
        bNode.prev = aNewNode
        
        aNewNode.next = bNode
        aNewNode.prev = aNode
        
        return aNewNode.uid
    
    
    def remove(self, uid):
        pass
        #TODO :D
        
        
    def swap(self, a, b):
        pass
    
    
    def length(self):
        return len(self._nodes)
    
        