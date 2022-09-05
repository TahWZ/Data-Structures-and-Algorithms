#!/usr/bin/env python3
"""
:author: Tah Wen Zhong
"""

class HashTable: #Linear probing
    def __init__(self, table_capacity = 101, hash_base=31):
        '''
        #Function: __intit__
        Creates an empty object of the class

        @Parameter: table_capacity, the size of the table
        @Parameter: hash_base, the hash base value
        @Pre-condition: None
        @Post-condition: None
        @Return: a table with size table_capacity, two variables which holds the hash_base and the count
        @Complexity: Best case and worst case: O(1)
        '''
        #Creates a table of None values
        self.table = [None] * table_capacity
        #Creates a variable to hold the hash base value
        self.base = hash_base
        #Counter which counts the number of items being set in the table
        self.count = 0
    
    def __getitem__(self, key):
        '''
        #Function: __getitem__
        Search for the given key value within the tuples in self.table and returns the item associated to the given key value
        (Uses self.hash(key) to gain the hash value which is the index of self.table which should contain a tuple)

        @Parameter: key, the key value to be searched in the lists in self.table
        @Pre-condition: None
        @Post-condition: Raises an exception if the key value is not within self.table
        @Return: The value associated with the given key value
        @Complexity: Best case: O(1) and worst case: O(N)
        '''
        hash_val = self.hash(key)
        #The loop iterates to search for the key value
        for _ in range(len(self.table)):
            if self.table[hash_val] is None:    #If the key value is not in table
                raise KeyError("Key does not exist")
            elif self.table[hash_val][0] == key:    #If the key value is found
                return self.table[hash_val][1]  #Returns the item associated to the key value
            else:
                hash_val = (hash_val + 1) % len(self.table) #Recalculate the hash_val
        #If key value not found, raise KeyError
        raise KeyError("Key does not exist")

    def __setitem__(self, key, item):
        '''
        #Function: __setitem__
        Sets or replace a given tuple within self.table with a new tuple containing the given key value and the item
        (Uses self.hash(key) to gain the hash value which is the index of self.table to store the key and item as tuple)

        @Parameter: key, the key value to be searched in the lists in self.table
        @Parameter: item, the item to be stored with the key value
        @Pre-condition: If self.table is full and the key is not contained within self.table, calls self.rehash()
        @Post-condition: If the key is not within self.table, store the key and item in self.table[hash_val]
        @Post-condition: If the key is within self.table, replaces tuple's item value with the new item
        @Return: None
        @Complexity: Best case: O(1) and worst case: O(N)
        '''
        #If table is full and key value not in table
        if self.count>=len(self.table) and self.__contains__(key)==False:
            #Calls rehash
            self.rehash()
        hash_val = self.hash(key)
        #The loop iterates to search for the key value
        for _ in range(len(self.table)):
            if self.table[hash_val] is None:    #If the key value is not in table
                #Adds 1 to counter and set the item in the table
                self.table[hash_val] = (key,item)
                self.count += 1
                return
            elif self.table[hash_val][0] == key:    #If the key value is found
                #Replaces the old item with the new item
                self.table[hash_val] = (key,item)
                return
            else:                               
                hash_val = (hash_val + 1) % len(self.table) #Recalculate the hash_val

    def __contains__(self, key):
        '''
        #Function: __contains__
        Searches for the given key value within the tuples in self.table and returns True if it is in self.table,else return False
        (Uses self.hash(key) to gain the hash value which is the index of self.table which should contain a tuple)

        @Parameter: key, the key value to be searched in the lists in self.table
        @Pre-condition: If the initial self.table[hash_val] contains None, return None 
        @Post-condition: If there is a tuple in self.table which contains the key value return True
        @Return: True/False
        @Complexity: Best case: O(1) and worst case: O(N)
        '''
        hash_val = self.hash(key)
        #The loop iterates to search for the key value
        for _ in range(len(self.table)):
            if self.table[hash_val] is None:    #If the key value is not in table
                return False
            elif self.table[hash_val][0] == key:    #If the key value is found
                return True
            else:
                hash_val = (hash_val + 1) % len(self.table) #Recalculate the hash_val
        return False

    def hash(self, key):
        '''
        #Function: hash
        For every character within the given key value.
        Use (value*self.base + ord(char)) % len(self.table) to calculate the value.
        The final output will be the hash_value with the given key value

        @Parameter: key, the key value to be searched in the lists in self.table
        @Pre-condition: None
        @Post-condition: None
        @Return: The value associated with the given key value
        @Complexity: Best case and worst case: O(N)
        '''
        #Turns a string to a list
        lst = list(key)
        value = 0
        for char in lst:    #For every character in the key value
            value = (value*self.base + ord(char)) % len(self.table)
        return value

    def rehash(self):
        '''
        #Function: rehash
        When self.table is full, the table_size is replaced to a value within Primes list.
        Furthermore the function will recompute every tuple within self.table as the
        values hash values for the key value within every tuple is different with the
        new tablesize. If there is no prime in prime list that can be used raise ValueError

        @Parameter: None
        @Pre-condition: Raises ValueError if there is no prime in prime list which is twice the size of the previous tablesize
        @Post-condition: None
        @Return: A self.table with a new tablesize and have all the tuple recomputed
        @Complexity: Best case and worst case: O(N)
        '''
        #Primes holds a list of prime values
        Primes =  [ 3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131,
                    163, 197, 239, 293, 353, 431, 521, 631, 761, 919, 1103,
                    1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013,
                    8419, 10103, 12143, 14591, 17519, 21023, 25229, 30313, 36353,
                    43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437, 187751,
                    225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897,
                    1162687, 1395263, 1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]
        new_capacity = None
        #Iterates every prime number
        for num in Primes:
            if num > len(self.table)*2: #If the prime number is appropriate to be used
                new_capacity = num
                break
        if new_capacity == None:    #If no prime number is appropriate to be used
            #Raises ValueError
            raise ValueError("There exist no prime which suffice the required table capacity increase")
        #Reset the count value
        self.count = 0
        pairs = []
        #Store the items to a temporary list
        for item in self.table:
            if item != None:
                pairs.append(item)
        #Resize the table
        self.table = [None] * new_capacity
        #Recompute the items into the table
        for k,v in pairs:
            self.__setitem__(k,v)

#-----------------------------------Test-----------------------------------
def test_init():
    test1 = HashTable()
    assert len(test1.table) == 101 and test1.base == 31,"Incorrect tablesize/hashbase"
    test2 = HashTable(313,23)
    assert len(test2.table) == 313 and test2.base == 23,"Incorrect tablesize/hashbase"
    
def test_hash():
    test1 = HashTable()
    assert test1.hash("a") == 97,"Incorrect hash value"
    assert test1.hash("ab") == 75,"Incorrect hash value"

def test_contains():
    test1 = HashTable()
    test1.table[97] = ("a",1)
    assert "a" in test1,"Contains failed (item in table)"
    assert "b" not in test1,"Contains failed (item not in table)"

def test_getitem():
    test1 = HashTable()
    test1.table[97] = ("a",1)
    assert test1["a"] == 1,"Get item failed"
    test1.table[97] = ("a",2)
    assert test1["a"] == 2,"Get item failed"

def test_setitem():
    test1 = HashTable()
    test1["a"] = 1
    assert "a" in test1,"Set item failed"
    pairs = [("abc",1),("abc",2)]
    for key,item in pairs:
        test1[key] = item
        assert test1[key] == item,"Set item failed"

def test_rehash():
    test1 = HashTable(1,31)
    correct_primes = [3,7,17,37]
    for i in range(4):
        test1.rehash()
        assert len(test1.table) == correct_primes[i],"Rehash failed"
    test1["abc"] = 123
    hash_valA = test1.hash("abc")
    test1.rehash()
    hash_valB = test1.hash("abc")
    assert hash_valA != hash_valB and test1.table[hash_valB] is not None,"Rehash failed"
    
def self_test():
    try:
        tests = [test_init(),test_hash(),
             test_contains(),test_getitem(),
             test_setitem(),test_rehash()]
        print("Test results (Self-made testing): Success" + "\nTest count= " + str(len(tests)))
    except:
        print("Test results (Self-made testing): Failure" + "\nFailure occurrence:")
        tests = [test_init(),test_hash(),
             test_contains(),test_getitem(),
             test_setitem(),test_rehash()]
#-----------------------------------Test-----------------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#------------------------------Notes------------------------------
'''
#Important notes
a)The position values are random but are within the range(0,table capacity)
b)Use a prime table capacity
c)The hash base is best to have no common factors with the multiplied value
d)Perfect hash maps rely on the keys properties
e)Chance of collision is 1/table capacity (Uniform hash)
f)Best if the hash base and table capacity are prime number
'''
#------------------------------Notes------------------------------
