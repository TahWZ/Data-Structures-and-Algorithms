#!/usr/bin/python3
class ListADT:
    #--------------------------!!!Additional function!!!-------------------------
    '''
    Question states the size should be able to change, but does not state whether it
    changes automatically or manually.
    '''
    #------If auto-------#
    '''
    If the size should be changed automatically
    @Affected functions: insert, append, delete
    
    #Functions: rules
    IF REQUIRED FOR A SINGLE FUNCTION TO PERFORM BOTH THE INCREASE AND DECREASE
    The size will change automatically when any function of the affected functions is used
    through usage of the rules() function
    
    #Functions: auto_increase, auto_decrease
    IF REQUIRED FOR TWO INDIVIDUAL FUNCTIONS TO PERFORM THE INCREASE AND DECREASE
    The size will change automatically when any function of the affected functions is used.
    For insert and append, the auto_increase() function will check and perform the size increase if required
    For delete, the auto_decrease() function 
    '''
    def rules(self):
        '''
        Function:  rules(self)
        @Description    Function which changes the list size based on given conditions
        @Post           If first condition met,list size increases by 1.9
        @Post           If second condition met,list size decreases by half
        '''
        if self.length == len(self.the_array):
            self.the_array += (round(self.length*1.9)-self.length)*[None]
        elif self.length < len(self.the_array)/4 and len(self.the_array)/2 >= 40:
            temp = self.the_array
            new_size = len(self.the_array)//2
            self.the_array = [None]*new_size
            for i in range(new_size):
                self.the_array[i] = temp[i]
                
    def auto_increase(self):
        '''
        Function:  auto_increase(self)
        @Description    Function which increases the list size based on a given condition
        @Post           If condition met,list size increases by 1.9
        '''
        if self.length == len(self.the_array):
            self.the_array += (round(self.length*1.9)-len(self.the_array))*[None]

    def auto_decrease(self):
        '''
        Function:  auto_decrease(self)
        @Description    Function which decreases the list size based on a given condition
        @Post           If condition met,list size decreases by half
        '''
        if self.length < len(self.the_array)/4 and len(self.the_array)/2 >= 40:
            temp = self.the_array
            new_size = len(self.the_array)//2
            self.the_array = [None]*new_size
            for i in range(new_size):
                self.the_array[i] = temp[i]
    #--------------------#
    #-----If manual------#
    '''
    If the size should be changed manually
    @Affected functions: None
    The size will change manually by calling the increase or decrease functions,
    if the requirements are met, the size will be changed accordingly
    '''
    def increase(self):
        '''
        Function:  auto_increase(self)
        @Description    Function which increases the list size based on a given condition
        @Post           If condition met,list size increases by 1.9
        @Post           If condition not met,list remains unchanged
        '''
        if self.length == len(self.the_array):
            self.the_array += (round(self.length*1.9)-len(self.the_array))*[None]
        else:
            print("Fail to increase size")

    def decrease(self):
        '''
        Function:  auto_decrease(self)
        @Description    Function which decreases the list size based on a given condition
        @Post           If condition met,list size decreases by half
        @Post           If condition not met,list remains unchanged
        '''
        if self.length < len(self.the_array)/4 and len(self.the_array)/2 >= 40:
            temp = self.the_array
            new_size = len(self.the_array)//2
            self.the_array = [None]*new_size
            for i in range(new_size):
                self.the_array[i] = temp[i]
        else:
            print("Fail to decrease size")
    #--------------------#
    #--------------------------!!!Additional function!!!-------------------------

    def is_empty(self):
        return self.length == 0

    def is_full(self):
        return self.length == len(self.the_array)
    
    def __contains__(self, item):
        for i in range(self.length):
            if item == self.the_array[i]:
                return True
        return False
 
    def append(self, item):
        if not self.is_full():
            self.the_array[self.length] = item
            self.length +=1
        else:
            raise Exception('List is full')
        #---------------?Auto?---------------
        #self.rules()
        self.auto_increase()
        #---------------?Auto?---------------

    def unsafe_set_array(self,array,length):
        """
        UNSAFE: only to be used during testing to facilitate it!! DO NOT USE FOR ANYTHING ELSE
        """
        if 'test' not in __name__:
            raise Exception('Not runnable')
			
        self.the_array = array
        self.length = length

    #-----------------------------------TASK 2-----------------------------------
    def __init__(self, size = None):
        '''
        Function:  __init__(self, size = None)
        @Description    Creates an empty array list with a fixed capacity.
        @Parameters     The capacity of the array list or none
        @Pre            The size input must at least be 40
        @Post           If size input valid,an empty array list of given size is created
        @Post           If size input invalid or not included, an empty array list of size 40 is created
        @Complexity     Best case: O(1), Worst case: O(n) ([None]*size is O(n))
        '''
        if size is not None and size >=40:
            self.the_array = [None]*size
            self.length = 0
        else: # size is None:
            self.the_array = [None]*40
            self.length = 0
        '''else:
            raise Exception("List size must be bigger than 40")'''

    def __str__(self):
        '''
        Function:  __str__(self)
        @Description    Returns the string representation of the array list elements.
        @Return         String representation, containing the elements of the array list
        @Complexity     Best and worst case:O(n)
        '''
        ret = ""
        for i in range(self.length):
            ret += str(self.the_array[i])+"\n"
        return ret
    
    def __len__(self):
        '''
        Function:  __len__(self)
        @Description    Returns the length of the array list. (Not the capacity)
        @Return         Length of the array list
        @Complexity     Best and worst case:O(n)
        '''
        length = 0
        for i in range(self.length):
            if self.the_array[i] != [None]:
                length += 1
        return length

    def __getitem__(self,index):
        '''
        Function:  __getitem__(self,index)
        @Description    Retrieves an item from the array list in the given index.
        @Parameters     Index to retrieve item from array list
        @Return         Item contained in the array list from the given index
        @Pre            Index must be valid
        @Post           List remains unchanged
        @Complexity     Best and worst case:O(1)
        '''
        def translate(index):
            '''
            Function:  translate(index)
            @Description    Returns the index value in positive, transforms negative index inputs to positive
            @Parameters     An index value
            @Return         A positive index representation for a negative index input or the same positive index input
            @Complexity     Best and worst case: O(1)
            '''
            if index < 0:
                return self.length+index
            else:
                return index
        try:
            if index >= -self.length and index <= self.length-1:
                index = translate(index)
                return self.the_array[index]
            else:
                raise IndexError
        except IndexError:
            print("Invalid index input")

    def __setitem__(self,index,item):
        '''
        Function:  __setitem__(self,index,item)
        @Description    Changes an item in the given index to another item
        @Parameters     Item to be set to and the array index for item to be set at. 
        @Pre            index must be valid
        @Post           if index is valid, the item is successfully set into the array list
        @Post           if index is invalid, raise IndexError and list remains unchanged
        @Complexity     Best and worst case: O(1)
        '''
        def translate(index):
            '''
            Function:  translate(index)
            @Description    Returns the index value in positive, transforms negative index inputs to positive
            @Parameters     An index value
            @Return         A positive index representation for a negative index input or the same positive index input
            @Complexity     Best and worst case: O(1)
            '''
            if index < 0:
                return self.length+index
            else:
                return index
        try:
            if index >= -self.length and index <= self.length-1:
                index = translate(index)
                self.the_array[index] = item
            else:
                raise IndexError
        except IndexError:
            print("Invalid index input")

    def __eq__(self,other):
        '''
        Function:  __eq__(self,other)
        @Description    Checks if other is a ListADT object and whether it's content is the same as self
        @Parameters     other (data which should supposedly be a ListADT object)
        @Return         True or False (Based on whether self is equal to other)
        @Pre            other should be a ListADT object and have the same length as self
        @Complexity     Best and worst case: O(n)
        '''
        equal = False
        if isinstance(other, ListADT) and self.__len__() == other.__len__():
            equal = True
            for i in range(self.length):
                if self.the_array[i] != other.__getitem__(i):
                    equal = False
        return equal

    def insert(self,index,item):
        '''
        Function:  insert(self,index,item)
        @Description    Inserts a given item to the array list at a given index
        @Parameters     Item to be inserted and array index for item to be inserted to
        @Pre            Array should not be full and index must be valid
        @Post           If array is full, raise Exception and array list remains unchanged
        @Post           If index is invalid, raise IndexError and array list remains unchanged
        @Post           If array not full and index is valid, item is inserted to list at the given index
        @Post(addition) The array will change based on how 
        @Complexity     Best case: O(1), Worst case: O(n)
        '''
        def translate(index):
            '''
            Function:  translate(index)
            @Description    Returns the index value in positive, transforms negative index inputs to positive
            @Parameters     An index value
            @Return         A positive index representation for a negative index input or the same positive index input
            @Complexity     Best and worst case: O(1)
            '''
            if index < 0:
                return self.length+index
            else:
                return index
        if self.is_full():
            raise Exception("List is full")
        elif index >= -self.length-1 and index <= self.length:
            index = translate(index)
            for i in range(len(self.the_array)-1,index,-1):
                self.the_array[i] = self.the_array[i-1]
            self.the_array[index] = item
            self.length += 1
        else:
            raise IndexError("Invalid index")
        #---------------?Auto?---------------
        #self.rules()
        self.auto_increase()
        #---------------?Auto?---------------

    def delete(self,index):
        '''
        Function:  delete(self,index)
        @Description    Deletes item in array list at given index.
        @Parameters     Index of item to be removed.
        @Pre            Index must be valid.
        @Post           If index is invalid, raise IndexError and list remains unchanged
        @Post           If index is valid, item is deleted from the array list
        @Complexity     Best case: O(1), Worst case: O(n)
        '''
        def translate(index):
            '''
            Function:  translate(index)
            @Description    Returns the index value in positive, transforms negative index inputs to positive
            @Parameters     An index value
            @Return         A positive index representation for a negative index input or the same positive index input
            @Complexity     Best and worst case: O(1)
            '''
            if index < 0:
                return self.length+index
            else:
                return index
        if index >= -self.length-1 and index <= self.length:
            index = translate(index)
            for i in range(index,len(self.the_array)-1):
                self.the_array[i] = self.the_array[i+1]
            self.the_array[len(self.the_array)-1] = None
            self.length -= 1
        else:
            raise IndexError("Invalid index")
        #---------------?Auto?---------------
        #self.rules()
        self.auto_decrease()
        #---------------?Auto?---------------
    #-----------------------------------TASK 2-----------------------------------

#---------------------------------------TEST-------------------------------------
def test_init():
    lst = ListADT(20)
    test1 = len(lst.the_array) == 40 and len(lst) == 0
    lst.append(1)
    test2 = len(lst.the_array) == 40 and len(lst) == 1
    lst2 = ListADT()
    test3 = len(lst2.the_array) == 40 and len(lst2) == 0
    return test1 and test2 and test3

def test_str():
    lst = ListADT()
    test1 = str(lst).strip("\n") == ("")
    lst.append(1)
    test2 = str(lst).strip("\n") == ("1")
    lst.append(2)
    test3 = str(lst).strip("\n") == ("1\n2").strip("\n")
    return test1 and test2 and test3

def test_len():
    lst = ListADT()
    test1 = len(lst) == 0
    lst.append(1)
    test2 = len(lst) == 1
    lst.append(2)
    test3 = len(lst) == 2
    return test1 and test2 and test3

def test_getitem():
    lst = ListADT()
    for i in range(1,41):
        lst.append(i)
    test1 = lst.__getitem__(0) == 1
    test2 = lst.__getitem__(1) == 2
    test3 = lst.__getitem__(-2)== 39
    return test1 and test2 and test3

def test_setitem():
    lst = ListADT()
    for i in range(1,41):
        lst.append(i)
    lst.__setitem__(0,500)
    test1 = lst.__getitem__(0) == 500
    lst.__setitem__(-2,500)
    test2 = lst.__getitem__(-2) == 500
    test3 = lst.__getitem__(1) == 2 and lst.__getitem__(-3) == 38
    return test1 and test2 and test3
    
def test_eq():
    lstA = ListADT()
    lstB = ListADT()
    lstC = ListADT()
    lstD = [1,2,3,4,5,6,7,8,9,10]
    for i in range(1,11):
        lstA.append(i)
        lstB.append(i)
        lstC.insert(-1,i)
    test1 = lstA.__eq__(lstB)
    test2 = lstA.__eq__(lstC) == False
    test3 = lstA.__eq__(lstD) == False
    return test1 and test2 and test3

def test_insert():
    lst = ListADT()
    for i in range(1,6):
        lst.insert(0,i)
    test1 = lst.the_array == [5,4,3,2,1] + [None]*35
    for i in range(1,3):
        lst.insert(3,i)
    test2 = lst.the_array == [5,4,3,2,1,2,1] + [None]*33
    for i in range(1,6):
        lst.insert(-3,i)
    test3 = lst.the_array == [5,4,3,2,1,2,3,4,5,1,2,1] + [None]*28
    return test1 and test2 and test3

def test_delete():
    lst = ListADT()
    for i in range(1,11):
        lst.append(i)
    lst.delete(0)
    test1 = lst.the_array == [2,3,4,5,6,7,8,9,10] + [None]*31
    lst.delete(-1)
    test2 = lst.the_array == [2,3,4,5,6,7,8,9] + [None]*32
    lst.delete(1)
    lst.delete(1)
    lst.delete(1)
    test3 = lst.the_array == [2,6,7,8,9] + [None]*35
    return test1 and test2 and test3

if __name__ == "__main__":
    tests = [test_init(),test_str(),test_len(),test_getitem(),test_setitem(),test_eq(),test_insert(),test_delete()]
    test_count = 0
    successes = 0
    failures = 0
    for test in tests:
        test_count += 1
        if test == True:
            successes += 1
        elif test == False:
            failures += 1
    print("Test results:" + "\nSuccesses=" + str(successes) + "\nFailures=" + str(failures))

def self_test():
    tests = [test_init(),test_str(),test_len(),test_getitem(),test_setitem(),test_eq(),test_insert(),test_delete()]
    test_count = 0
    successes = 0
    failures = 0
    for test in tests:
        test_count += 1
        if test == True:
            successes += 1
        elif test == False:
            failures += 1
    print("Test results (Self-made testing):" + "\nSuccesses=" + str(successes) + "\nFailures=" + str(failures))
#---------------------------------------TEST-------------------------------------

