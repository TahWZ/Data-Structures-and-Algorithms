# import libraries
import random
import timeit
import csv #To produce csv containing the results for Task 2

#---------------------------------------------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Task 1----------------------------
def radix_sort(num_list, b):
    """
    Function that performs radix sort
    Precondition:       num_list should contain only positive integers
    Arguments:          num_list = The list of numbers (integers) to be sorted
                        b = The base used
    Time complexity:    Best case (O(N+b)M)
                        Worst case (O(N+b)M)
                        (N is the number of elements in num_list,
                        M is the number of digits in the largest number in the input list when represented in base b,
                        b is the base used)
    Space complexity:   O(N+b)
    Aux space complexity:   O(N+b)
    Return: A list containing all elements in num_list sorted in ascending order
    """
    # step 1: It takes the input num_list and retrieve its maximum number value, followed by producing a result list with the same size as num_list
    # step 2: A loop iterates to check if each value is non-negative and fill the value in result list (duplicates the list)
    # step 3: Another loop iterate to perform counting sort M amount of times
    # last step: Returns the result list which is num_list in ascending order
    def counting_sort(lst, b, bPow):
        """
        Function that performs counting sort
        Arguments:          lst = The list of numbers to be sorted
                            b = The base used
                            bPow = The power that the base uses
        Time complexity:    Best case (O(N+b))
                            Worst case (O(N+b))
                            (N is the number of elements in lst,
                            b is the base used)
        Space complexity:   O(N+b)
        Aux space complexity:   O(N+b)
        Return: None (But has lst sorted based on each value's resulting value through (value//b^bpow)%b in ascending order)
        """
        # step 1: It takes the input lst and duplicates it, followed by creating a count array of size b
        # step 2: Iterates to have each value of list run through calculation((lst[i]//(b**bPow))%b),
        #         having the resulting value used as an index, adding 1 to the value stored in the count array of the resulting index
        # step 3: Converts the value stored to position values and shift the values right
        # last step: Iterates and have each element stored in the appropriate positions based on count array and the calculation ((lst[i]//(b**bPow))%b
        n = len(lst)
        count = [0]*b
        temp = [0]*n
        # Duplicate the list
        for i in range(n):
            temp[i] += lst[i]
        # Stores the occurence count of each count value
        for i in range(n):
            count[(lst[i]//(b**bPow))%b] += 1
        # Convert count array values into position values
        for i in range(1,b):
            count[i] += count[i-1]
        # Shift all values to the right
        for i in range(b-1,-1,-1):
            if i == 0:
                count[i] = 0
            else:
                count[i] = count[i-1]
        for val in temp:
            index = (val//(b**bPow))%b
            lst[count[index]] = val
            count[index] += 1
    try:
        # Finds the maximum value and stores it in numMax
        numMax = max(num_list)
        res = [0]*len(num_list)
        bPow = 0
        # Duplicates and checks list
        for i in range(len(num_list)):
            res[i] += num_list[i]
            assert num_list[i] >= 0, "radix_sort failed, given list contains negative values"
            assert isinstance(num_list[i],int), "radix_sort failed, given list has non-integer values"
        while numMax > 0:
            numMax //= b
            counting_sort(res,b,bPow)
            bPow += 1
        return res
    except AssertionError as msg:
        print(msg)
#-----------------------------Task 1----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Task 2----------------------------
def time_radix_sort():
    """
    Function that time radix radix sort
    Time complexity:    Best case O(1)
                        Worst case O(1)
    Space complexity: O(1)
    Aux space complexity: O(1)
    Return: An array containing the results stored in the following format:(the time needed to radix_sort the test_data with a given base,the base used)
    """
    # step 1: Iterates to perform radix_sort with each base of bases and store the time needed along with the base used in result
    # last step: return result
    bases = [2,8,64,256,4096,2**14,2**16,2**18,2**21,2**24,2**25,2**26]
    result = []
    test_data = [random.randint(1,(2**64)-1) for _ in range(100000)]
    # Performs radix_sort with each base and stores the time needed for radix_sort to complete
    for b in bases:
        start = timeit.default_timer()
        radix_sort(test_data,b)
        time = timeit.default_timer() - start
        result.append([b,time])
    return result

def task2_csv(result):
    """
    Function that creates/write the result of time_radix_sort to a csv 
    Time complexity:    Best case (O(1))
                        Worst case (O(1))
    Space complexity:   O(1)
    Aux space complexity:   O(1)
    Return: None
    """
    #Creates/write a csvfile
    with open('output_task2.csv',mode='w',newline='') as csvfile:   
            writer = csv.writer(csvfile,delimiter=',')
            writer.writerow(["Base","Time taken"])
            for res in result:  
                writer.writerow(res)
#-----------------------------Task 2----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Task 3----------------------------
def find_rotations(string_list, p):
    """
    Function that finds all the strings in string_list whose p-rotations also appear in the list
    Arguments:          string_list = A list of string 
                        p = the rotation size
    Time complexity:    Best case (O(NM))
                        Worst case (O(NM))
                       (N is the number of strings in the input list
                        M is the maximum number of letters in a word, among all words in the input list)
    Space complexity: O(NM)
    Aux space complexity: O(NM)
    Return: a list of all string which p-rotations also appear in the list
    """
    # step 1: Creates an array (temp) which stores the string_list elements and it's p-rotation
    # step 2: Find the values which contain duplicates in temp and store it in an array (res)
    # last step: Rotate each element in res with -p as the p value to retrieve each element's initial form before p-rotation
    def rotate(string,p):
        """
        Function that returns the p-rotation of the given string value
        Arguments:          string = String value
                            p = rotation size
        Time complexity:    Best case (O(N))
                            Worst case (O(N))
                            (N is the length of string)
        Space complexity:  O(1)
        Aux space complexity: O(1)
        Return: p-rotation of string
        """
        s = p % len(string) 
        return string[s:]+string[:s]
    def radix_sort(string_list):
        """
        Function that performs radix sort
        Arguments:          string_list = The list of strings to be sorted
        Time complexity:    Best case (O(NM))
                            Worst case (O(NM))
                            (N is the number of elements in string_list,
                            M is the number of characters of the string with the most number of characters in string_list
        Space complexity:   O(NM)
        Aux space complexity:   O(NM)
        Return: A list containing all elements in string_list sorted
        """
        # step 1: It takes the input string and retrieve the length of the string with the most number of characters in string_list
        # step 2: A loop iterates to duplicate the string_list
        # step 3: Another loop iterate to perform counting sort M times
        # last step: Returns the result list which is the sorted version of string_list
        def counting_sort(lst,p,m):
            """
            Function that performs counting sort
            Arguments:          lst = The list of strings to be sorted
                                p = The string's character position which the sorting is based on
                                m = The number of characters of the string with the most number of characters in string_list
            Time complexity:    Best case (O(N))
                                Worst case (O(N))
                                (N is the number of elements in lst)
            Space complexity:   O(NM)
            Aux space complexity:   O(NM)
            Return: None (But has lst sorted based on the string's character in position p)
            """
            # step 1: It takes the input lst and duplicates it, followed by creating a count array of size 27 (26 alphabets and an additional slot for strings with length <= p)
            # step 2: Iterates to obtain the ordinal value of each string's character in the given position p
            # step 3: During each iteration, with the ordinal value used as the index for count array, have the value assigned increment by 1
            # step 3: Converts the value stored to position values and shift the values right
            # last step: Sort the array by having each value placed in the correct position within the list
            n = len(lst)
            # Creates count list with size 27 (26 alphabets and an additional slot for strings with length <= p)
            count = [0]*27
            temp = [""]*n
            # Duplicate list
            for i in range(n):
                temp[i] += lst[i]
            #Store the occurence count of each count value (If it is " " then +1 in count[0])
            for item in temp:
                if len(item) <= p:
                    count[0] += 1
                else:
                    ord_val = ord(item[p])
                    assert (ord_val>=97 and ord_val<=122), "find_rotations failed, string list should only contain lowercase alphabet characters"
                    count[ord_val-96]+=1
            # Convert count array values into position values
            for i in range(1,27):
                count[i] += count[i-1]
            # Shift all values right
            for i in range(26,-1,-1):
                if i == 0:
                    count[i] = 0
                else:
                    count[i] = count[i-1]
            # Sort the array
            for item in temp:
                if len(item) <= p:
                    index = 0
                else:
                    index = ord(item[p])-96
                lst[count[index]] = item
                count[index] += 1
        n = len(string_list)
        # To obtain the length of the string with the most characters
        m = len(max(string_list, key=len))
        res = [""]*n
        # Duplicates the list
        for i in range(n):
            res[i] += string_list[i]
        # Perform counting sort based on each string's p position value
        for p in range(m-1,-1,-1):
            counting_sort(res,p,m)
        return res
    def find(lst):
        """
        Function that finds the values which have duplicates within the same lst
        Time complexity:    Best case (O(N+k))
                            Worst case (O(N+k))
                            (N is the number of strings in the input list,
                            k is the slicing size)
        Space complexity:   O(1)
        Aux space complexity:   O(1)
        Return: A list of values which have duplicates in lst
        """
        # step 1: The loop iterates (length of given lst) times
        # step 2: During each iteration, if the value lst[j]==lst[i+1] then the values i and j increments.
        #         else swap the values in lst[j] and lst[i+1]
        #(This loop is to have each unique value and duplicates to be placed on the top. Furthermore, have lst[j:] to contain only one of each values which had a duplicate in the lst)
        # last step: Return lst[j:]
        i = 0
        j = 0
        #To iterate (length of given lst) times
        while i < len(lst)-1:
            if lst[j] == lst[i+1]:
                i += 1
            else:
                # To have duplicates and unique values placed on the top of the list
                lst[j+1],lst[i+1] = lst[i+1],lst[j+1]
                j += 1
                i += 1
        j += 1
        return lst[j:]
    n = len(string_list)
    #Creates an empty array to hold values
    temp = [""]*(2*n)
    try:
        assert n > 0, "find_rotations failed, string list given should not be empty"
        # Adds the string and its p-rotation in temp
        for i in range(n):
            temp[i] += string_list[i]
            temp[i+n] += rotate(string_list[i],p)
        # Find the values which had duplicates in temp and store is res
        res = find(radix_sort(temp))
        # Retrieve the intital form (the value before p-rotation) of each element in res
        for i in range(len(res)):
            res[i] = rotate(res[i],-p)
        return res
    except AssertionError as msg:
        print(msg)
#-----------------------------Task 3----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#------------------------------Test-----------------------------
if __name__ == "__main__":
    # driver for the test cases
    print("Running test")
    def test_q1():
        try:
            #Test values
            test_list = [random.randint(1,(2**32)) for _ in range(1000)]
            test_bases = [2,5,100,999]
            #Test A (Test to check if list is sorted after radix sort)
            outputA = radix_sort(test_list,10)
            for i in range(1,len(outputA)):
                assert outputA[i] > outputA[i-1],"radix sort output is not sorted"
            #Test B (Test to check if different bases still produce a sorted array)
            for b in test_bases:
                outputB = radix_sort(test_list,b)
                assert outputB == outputA,"radix sort fail to run for given base"
            #Test C (Test if an already sorted list and a list in descending order can be sorted)
            outputB.reverse()
            outputC = [radix_sort(outputB,10),radix_sort(outputA,10)]
            assert outputC[0] == outputA,"radix sort failed to sort a list in descending order"
            assert outputC[1] == outputA,"radix sort failed to handle sorting an already sorted list"
            print("pass q1 test")
        except AssertionError as msg:
            print("task 1 test failed:\n" + msg)
    def test_q2():
        try:
            ######################(Takes around 2 minutes)########################
            ##Test A (Test to validate whether time_radix_sort operates as intended)
            test = time_radix_sort()
            bases = [2,8,64,256,4096,2**14,2**16,2**18,2**21,2**24,2**25,2**26]
            for b,time in test:
                assert b in bases,"time radix sort failed to store the bases provided"
                assert isinstance(time,float),"time radix sort failed to produce valid time values"
            #Test B (Test to check whether the csv output function operates as intended)
            task2_csv(time_radix_sort())
            with open('output_task2.csv','r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row != ['Base','Time taken']:
                        try:
                            assert float(row[0]).is_integer(),"csv output function failed to record bases used"
                        except ValueError:
                            assert False,"csv ouput function failed to produce valid values"
            ######################################################################
            print("pass q2 test")
        except AssertionError as msg:
            print("task 2 test failed:\n" + msg)
    def test_q3():
        #Test values
        initial = ["aaa", "abc", "cab", "acb", "wxyz", "yzwx"]
        #match_list holds the correct output values for find_rotations in match_list
        match_list = [["aaa", "cab"],["aaa", "abc", "yzwx", "wxyz"],
                  ["aaa", "abc", "cab", "acb", ],["aaa", "cab", "yzwx", "wxyz"],
                  ["aaa", "abc"],["aaa", "abc", "cab", "acb", "wxyz", "yzwx"],
                  ["aaa", "cab"],["aaa", "abc", "yzwx", "wxyz"],["aaa", "abc", "cab", "acb"],
                  ["aaa", "cab", "yzwx", "wxyz"],["aaa", "abc"]]
        p_list = [integer for integer in range(-5, 6)]
        #Test
        for p in p_list:
            temp = find_rotations(initial,p)
            temp.sort()
            match_list[p+5].sort()
            assert temp == match_list[p+5],"find_rotations failed to produce correct output"
        print("pass q3 test")
    # run test Q1
    test_q1()
    test_q2()
    test_q3()
    print("pass all")
