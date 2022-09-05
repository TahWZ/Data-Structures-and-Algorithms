#!/usr/bin/env python3
"""
:author: Tah Wen Zhong
"""
import csv
import timeit

class HashTable: #Linear Probing
    def __init__(self, table_capacity = 101, hash_base=31):
        '''
        #Function: __intit__
        Creates an empty object of the class

        @Parameter: table_capacity, the size of the table
        @Parameter: hash_base, the hash base value
        @Pre-condition: None
        @Post-condition: None
        @Return: a table with size table_capacity, two variables which holds the hash_base and the count.
                 Initialise 4 counters (collision_count,probe_total,probe_max,rehash_count)
        @Complexity: Best case and worst case: O(1)
        '''
        #Creates a table of None values
        self.table = [None] * table_capacity
        #Creates a variable to hold the hash base value
        self.base = hash_base
        #Counter which counts the number of items being set in the table
        self.count = 0
        #---------------Task 3--------------
        #Creates 4 counter values
        self.collision_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0
        #---------------Task 3--------------
    
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
        Sets or replace a given tuple within self.table with a new tuple containing the given key value and the item.
        Furthermore, update the counter values if required.
        (Uses self.hash(key) to gain the hash value which is the index of self.table to store the key and item as tuple)

        @Parameter: key, the key value to be searched in the lists in self.table
        @Parameter: item, the item to be stored with the key value
        @Pre-condition: If self.table is full and the key is not contained within self.table, calls self.rehash()
        @Post-condition: If the key is not within self.table, store the key and item in self.table[hash_val]
        @Post-condition: If the key is within self.table, replaces tuple's item value with the new item.
                         Update the counter values based on the values computed
        @Return: None
        @Complexity: Best case: O(1) and worst case: O(N)
        '''
        #If table is full and key value not in table
        if self.count>=len(self.table) and self.__contains__(key)==False:
            #Calls rehash
            self.rehash()
        hash_val = self.hash(key)
        #---------------Task 3--------------
        probe_length = 0
        #---------------Task 3--------------
        #The loop iterates to search for the key value
        for _ in range(len(self.table)):
            if self.table[hash_val] is None:    #If the key value is not in table
                #Adds 1 to counter and set the item in the table
                self.table[hash_val] = (key,item)
                self.count += 1
                #---------------Task 3--------------
                if probe_length > 0:    #If there was a collision
                    self.collision_count += 1
                #Add probe length (If there was no collision the length will be 0)
                self.probe_total += probe_length
                if probe_length > self.probe_max:   #If the current probe length is larger than the max
                    #Replaces the probe_max value
                    self.probe_max = probe_length
                #---------------Task 3--------------
                return
            elif self.table[hash_val][0] == key:    #If the key value is found
                #Replaces the old item with the new item
                self.table[hash_val] = (key,item)
                return
            else:
                hash_val = (hash_val + 1) % len(self.table) #Recalculate the hash_val
                #---------------Task 3--------------
                #Add 1 to probe length
                probe_length += 1
                #---------------Task 3--------------

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
        new tablesize. If there is no prime in prime list that can be used raise ValueError.
        Resets the counter values except hash_count. The hash_count is increased by 1

        @Parameter: None
        @Pre-condition: Raises ValueError if there is no prime in prime list which is twice the size of the previous tablesize
        @Post-condition: None
        @Return: A self.table with a new tablesize and have all the tuple recomputed, Updates the 4 counter values as well
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
        #---------------Task 3--------------
        #Adds the rehash counter by 1
        self.rehash_count += 1
        #Resets the other counters
        self.collision_count = 0
        self.probe_total = 0
        self.probe_max = 0
        #---------------Task 3--------------
        #Recompute the items into the table
        for k,v in pairs:
            self.__setitem__(k,v)

    #-----------------------------Task 3----------------------------
    def statistics(self):
        '''
        #Function: statistics
        Returns the value of the 4 counter values

        @Parameter: None
        @Pre-condition: None
        @Post-condition: None
        @Return: self.collision_count,self.probe_total,self.probe_max,self.rehash_count
        @Complexity: Best case and worst case: O(1)
        '''
        return (self.collision_count,self.probe_total,self.probe_max,self.rehash_count)
    #-----------------------------Task 3----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Task 3----------------------------
def load_dictionary(hash_table,filename,time_limit = None):
    '''
    #Function: load_dictionary
    Reads a file with filename and store the words to use as keys for setting items into the hash_table.
    All keys are associated with the value 1 to use as the value to be stored in the hash table.

    @Parameter: hash_table, the hash table to be used.
    @Parameter: filename, the name of the file to read
    @Parameter: time_limit, the time limit for computation
    @Pre-condition: None
    @Post-condition: An exception is raised if the time taken to set the item into the hash table exceeds time_limit 
    @Return: None
    @Complexity: Best case and worst case: O(n)
    '''
    def read_text_file(name):
        #Opens the file
        f = open(name,"r",encoding='utf-8-sig')
        #Store the words in the file to a list
        text = [word.replace('\n','') for word in f]
        f.close()
        #Returns the list
        return text
    words = read_text_file(filename)
    if time_limit == None:  #If no time limit was given
        for key in words:   #For every word in the list
            hash_table[key]=1
    else:
        start = timeit.default_timer()  #Starts the timer
        for key in words:   #For every word in the list
            hash_table[key]=1
            if time_limit < timeit.default_timer()-start:   #If the timer's time exceeds the time limit
                raise Exception('Time limit was reached')

def load_dictionary_statistics(hash_base,table_size,filename,max_time):
    '''
    #Function: load_dictionary_statistics
    Creates a hash_table with the given hash_base and table_size.
    Reads a file with filename and store the words to use as keys for setting items into the hash_table.
    All keys are associated with the value 1 to use as the value to be stored in the hash table.
    Furthermore, the function counts the distinct words in the file. The function will call a function
    in the hash table which returns 4 counter values (collision_count,probe_total,probe_max,rehash_count)

    @Parameter: hash_base, the hash base for the hash_table.
    @Parameter: table_Size, the table_size for the hash_table.
    @Parameter: filename, the name of the file to read
    @Parameter: max_time, the time limit for computation
    @Pre-condition: None
    @Post-condition: If the max_time limit was reached, the second return value becomes None
    @Return: words, the number of distincts words in the file given
    @Return: time/None, the time taken to compute or None if the computation time exceeds max_time
    @Return: collision_count,probe_total,probe_max,rehash_count, values gained through statistics()
    @Complexity: Best case and worst case: O(n)
    '''
    def read_text_file(name):
        #Opens the file
        f = open(name,"r",encoding='utf-8-sig')
        #Store the words in the file to a list
        text = [word.replace('\n','') for word in f]
        f.close()
        #Returns the list
        return text
    def distinct_count(lst):
        #Returns the distinct word count
        return len(list(set(lst)))
    #Creates a hash table
    hash_table = HashTable(table_size,hash_base)
    try:
        #Starts a timer
        start = timeit.default_timer()
        #Calls a function which would raise an exception if time limit was reached
        load_dictionary(hash_table,filename,max_time)
        #If the time limit was not reached, the time is stored
        time = timeit.default_timer() - start
        #The distinct word count is computed
        words = distinct_count(read_text_file(filename))
        #Calls statistics function which return 4 counter values
        collision_count,probe_total,probe_max,rehash_count=hash_table.statistics()
        #Returns the distinct word count, time taken and 4 counter values
        return (words,time,collision_count,probe_total,probe_max,rehash_count)
    except: #If the time limit was reached
        words = distinct_count(read_text_file(filename))
        #Calls statistics function which return 4 counter values
        collision_count,probe_total,probe_max,rehash_count=hash_table.statistics()
        #Returns the distinct word count, None and 4 counter values
        return (words,None,collision_count,probe_total,probe_max,rehash_count)

def table_load_dictionary_statistics(max_time):
    '''
    #Function: table_load_dictionary_statistics
    The function contains 3 lists which are stored with filenames, hash base values and tablesize values.
    The combinations of the given values are used for computation.
    The max_time value is time limit for every computation.
    A csv file output_task2.csv is made containing the filename,tablesize,hash base value,distinct word count,
    (time taken/"TIMEOUT"),collision_count,probe_total,probe_max and rehash_count

    @Parameter: max_time, the time limit for computation
    @Pre-condition: None
    @Post-condition: If the max_time limit was reached, "TIMEOUT" is stored inplace of the time value in the list of results
    @Return: A csv file is made which contains the results for every combination with the given lists of items
             The csv contains: (filename,tablesize,hash base value,distinct word count,(time taken/"TIMEOUT"),
                                collision_count,probe_total,probe_max,rehash_count)
    @Complexity: Best case and worst case: O(1) 
    '''
    #A list of filenames
    filename_list= ['english_small.txt', 'english_large.txt', 'french.txt']
    #A list of hash bases
    b_list = [1,27183,250726]
    #A list of TABLESIZE
    TABLESIZE_list = [250727,402221,1000081]
    result = []
    #TIMEOUT is (max_time+10)
    TIMEOUT = max_time+10
    #Iterates every filename
    for filename in filename_list:
        #Iterates every TABLESIZE
        for TABLESIZE in TABLESIZE_list:
            #Iterates every hash base
            for b in b_list:
                #Calls a function which returns None as it's second return value if time limit was met
                ret = load_dictionary_statistics(b,TABLESIZE,filename,max_time)
                if ret[1]==None:    #If time limit was met
                    result.append([filename,TABLESIZE,b,ret[0],TIMEOUT,ret[2],ret[3],ret[4],ret[5]])
                else:
                    result.append([filename,TABLESIZE,b,ret[0],ret[1],ret[2],ret[3],ret[4],ret[5]])
    with open('output_task3.csv',mode='w',newline='') as csvfile:   #Creates/write a csvfile
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(["Filename","Tablesize","Hash base","Distinct word count","Runtime","Collision count","Probe total","Probe max","Rehash_count"])
        for res in result:  #For every result
            writer.writerow(res)    #Add results as rows in the csvfile
#-----------------------------Task 3----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#------------------------------Main-----------------------------
if __name__ == '__main__':
    table_load_dictionary_statistics(120)
#------------------------------Main-----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#------------------------------Test-----------------------------
def test_statistics():
    test1 = HashTable()
    condA,condB = False,False
    test1.table[97] = ("wow",5)
    test1.table[98] = ("woah",6)
    test1.table[99] = ("word",7)
    test1["a"] = 3
    if test1.statistics() == (1,3,3,0):
        condA = True
    test1.rehash()
    if test1.statistics()[3] == 1:
        condB = True
    assert condA and condB,"Failure in statistics"

def test_load_dictionary_statistics():
    condA,condB = False,False
    result = load_dictionary_statistics(31,101,"test_task3.txt",None)
    if len(result)==6 and False not in [res>=0 for res in result[2:6]]:
        condA = True
    result = load_dictionary_statistics(31,101,"test_task3.txt",0)
    if len(result)==6 and result[1] == None:
        condB = True
    assert condA and condB,"Failure in load_dictionary_statistics"

def test_table_load_dictionary_statistics():
    #No testing needed
    assert True,"Failure in table_load_dictionary_statistics"

def self_test():
    try:
        tests = [test_statistics(),test_load_dictionary_statistics(),test_table_load_dictionary_statistics()]
        print("Test results (Self-made testing): Success" + "\nTest count= " + str(len(tests)))
    except:
        print("Test results (Self-made testing): Failure" + "\nFailure occurrence:")
        tests = [test_statistics(),test_load_dictionary_statistics(),test_table_load_dictionary_statistics()]
#------------------------------Test-----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Notes-----------------------------
'''
#Important notes
a)The position values are random but are within the range(0,table capacity)
b)Use a prime table capacity
c)The hash base is best to have no common factors with the multiplied value
d)Perfect hash maps rely on the keys properties
e)Chance of collision is 1/table capacity (Uniform hash)
f)Best if the hash base and table capacity are prime number
'''
#-----------------------------Notes-----------------------------
