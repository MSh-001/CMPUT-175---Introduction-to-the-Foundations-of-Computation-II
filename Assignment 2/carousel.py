class DLinkedListNode:
    '''An object in this class represents a single node in a doubly linked list'''
    def __init__(self,initData,initNext,initPrevious):
        '''
        Parameters:
            - self: the node to initialize
            - initData: stores the employee record as a string 
            - initNext: points to the next node, type DLinkedListNode
            - initPrevious: points to the previous node, type DLinkedListNode
        Initializes the values of the attributes of a doubly linked list node object
        '''
        self.data = initData
        self.next = initNext
        self.previous = initPrevious

        if initNext is not None:
            self.next.previous = self

        if initPrevious is not None:
            self.previous.next = self

    def getData(self):
        '''
        Parameter:
            - self: the node object
        Returns the data attribute
        '''
        return self.data
    
    def getNext(self):
        '''
        Parameter:
            - self: the node object
        Returns the next attribute
        '''
        return self.next
    
    def getPrevious(self):
        '''
        Parameter:
            - self: the node object
        Returns the previous attribute
        '''
        return self.previous
    
    def setData(self, newData):
        '''
        Parameter:
            - self: the node object
            - newData: the new data to assign to the node, any type
        Sets the data attribute to a new value
        '''
        self.data = newData

    def setNext(self, newNext):
        '''
        Parameter:
            - self: the node object
            - newNext: the new reference to the next node, type DLinkedListNode
        Sets the next attribute to a new value
        '''
        self.next = newNext

    def setPrevious(self, newPrevious):
        '''
        Parameter:
            - self: the node object
            - newPrevious: the new reference to the previous node, type DLinkedListNode
        Sets the previous attribute to a new value
        '''
        self.previous = newPrevious

class Carousel:
    '''An object in this class represents a single circular doubly linked list (carousel)'''
    def __init__(self):
        '''
        Parameter:
            - self: the carousel object
        Initializes the head and current attributes to None
        '''
        self.head = None
        self.current = None
    
    def add(self, data):
        '''
        Parameters:
            - self: the carousel object
            - data: the employee record str to add
        - creates a new node, and inserts it into the carousel
        - if the list is empty, sets head and current to new node and links it to itself
        - otherwise, inserts new node after current and updates current to equal the new node 
        '''
        if self.head is None:
            newNode = DLinkedListNode(data, None, None)
            self.head = newNode
            self.current = newNode
            newNode.setNext(self.head)
            newNode.setPrevious(self.head)
        else:
            newNode = DLinkedListNode(data, self.current.getNext(), self.current)
            self.current = newNode

    def getCurrentData(self):
        '''
        Parameter:
            - self: the carousel object
        Returns the data of the current node, or a message if the carousel is empty
        '''
        try:
            return self.current.getData()
        except: return 'The carousel is empty!'

    def moveNext(self):
        '''
        Parameter:
            - self: the carousel object
        Updates current to point to the next node in the carousel, or prints a message if the carousel is empty
        '''
        try:
            self.current = self.current.getNext()
        except: print("Can't move current to next node! The carousel is empty!")

    def movePrevious(self):
        '''
        Parameter:
            - self: the carousel object
        Updates current to point to the previous node in the carousel, or prints a message if the carousel is empty
        '''
        try:
            self.current = self.current.getPrevious()
        except: print("Can't move current to previous node! The carousel is empty!")

    def __str__(self):
        '''
        Parameter:
            - self: the carousel object
        Returns a string representation of the carousel object
        '''
        values = []
        if self.head != None:
            current = self.head.getNext()
            values.append(self.head.getData())
            while current != self.head:
                values.append(str(current.getData()))
                current = current.getNext()
        return str(values)

def main():
    # Create a carousel
    carousel = Carousel()

    # Add some employees as strings
    carousel.add("Alice, HR, ID:101")
    carousel.add("Bob, Sales, ID:102")
    carousel.add("Charlie, IT, ID:103")
    carousel.add("Diana, Marketing, ID:104")

    # Print the carousel
    print("Full Carousel:")
    print(carousel)

    # Show the current employee
    print("\nCurrent Employee:")
    print(carousel.getCurrentData())

    # Move forward through the carousel
    carousel.moveNext()
    print("\nAfter moving next:")
    print(carousel.getCurrentData())

    # Move backward using movePrevious()
    carousel.movePrevious()
    print("Previous:", carousel.getCurrentData())

if __name__ == "__main__":
    main()