class Node():
    def __init__(self, item=None, link=None):
        self.item = item
        self.next = link

class StackADT:
    def __init__(self):
        self.head = None
    
    def size(self):
        count = 0
        node = self.head
        while node is not None:
          count += 1
          node = node.next
        return count
    
    def is_empty(self):
        return self.head is None
        
    def is_full(self):
        return False
         
    def push(self, item):
        new_node = Node(item, self.head)
        self.head = new_node

        
    def pop(self):
        if self.is_empty():
          raise IndexException("Attempted to pop empty stack.")
        item = self.head.item
        self.head = self.head.next
        return item
   
    def reset(self):
        self.head = None
