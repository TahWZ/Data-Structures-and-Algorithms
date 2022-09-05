#%% The Node class
class Node:
    """
    The Node class for the Trie

    #Attributes
    -----------
    @value : str
        The string value formed through concatenating the parent's value and the character the current value represents
    @children : array
        The array used to store all the child nodes
    @prefix_count : int
        The number of values which has the current node's value as a prefix
    @end_count : int
        Stores the number of occurences where the string checked is equal to the node value (to count duplicates)
    
    #Methods
    --------
    @link(key)
        Method which return the linked child node and add a child node if not yet created
    @check_child(key)
        Method which checks if the child node representing the given key exist
    @get_child()
        Method which retrieves the desired child node
    @increment()
        Increment end_count by 1
    """
    def __init__(self,key=""):
        """
        Parameterizd constructor for the Trie class, it takes a key to store as its value
        
        @Precondition:       key should be a string containing only alphabetic characters
        @Arguments:          key = The string value the node represents
        @Time complexity:    Best case O(1)
                             Worst case O(1) 
        @Space complexity:   O(1)
        """
        #The value the node represents
        self.value = key
        #The array used to store all child nodes (stores None if child node not created)
        self.children = [None]*26
        #The number of values which has the current node's value as a prefix
        self.prefix_count = 0
        #the number of occurences where the string checked is equal to the node value (to count duplicates)
        self.end_count = 0

    def link(self,key):
        """
        Function which returns the linked child node if it exist or creates and return a new linked child node
        
        @Precondition:       key is a character which its ordinal value is index where the linked child node should be
        @Arguments:          key = The character which its ordinal value will be used as the index
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        @Return: The appropriate linked child node
        """
        #Check if child node does not exist
        if self.check_child(key) == False:
            #Creates the child node for corresponding key
            self.children[ord(key)-97] = Node(self.value+key)
        self.prefix_count+=1
        return self.children[ord(key)-97]

    def check_child(self,key):
        """
        Function which returns a boolean value which indicates whether a child node representing the given key exist
        
        @Precondition:       key is a character which its ordinal value is index where the linked child node should be
        @Arguments:          key = The character which its ordinal value will be used as the index
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        @Return: boolean value which indicates whether the linked child node exist (True or False)
        """
        #Check if child node exist
        child = self.children[ord(key)-97]
        if child == None:
            #Returns False if child node does not exist
            return False
        else:
            #Returns True if child node exist
            return True

    def get_child(self,key):
        """
        Function which returns the linked child node (does not create so None is a possible return value)
        
        @Precondition:       key is a character which its ordinal value is index where the linked child node should be
        @Arguments:          key = The character which its ordinal value will be used as the index
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        @Return: The child node or None
        """
        #Returns the child node or None if the child node does not exist
        return self.children[ord(key)-97]
    
    def increment(self):
        """
        Function which increment the end_count value by 1
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        """
        #Increments the end count
        self.end_count += 1


#%% The Trie class
class Trie:
    """
    The Trie class uses Nodes to represent a tree structure. It stores only the root node but has methods to modify and locate all child nodes through it.
    Each node can have a maximum of 26 child nodes which is used to represent all alphabetic characters in lowercase.

    #Attributes
    -----------
    @root : Node
        The root of the tree structure

    #Methods
    --------
    @insert(key)
        Function to add a word into the Trie    
    @string_freq(query_str)
        Function to get the number of elements in text which are query_str
    @prefix_freq(query_str)
        Function to get the number of elements in text which has query_str as its prefix
    @wildcard_prefix_freq(query_str)
        Function to get all elements in text which has query_str as its prefix. Furthermore, the query_str may contain a '?' character
        which is used to indicate a wildcard(It represents any lowercase alphabetic characters)
    """
    
    def __init__(self, text):
        """
        Parameterizd constructor for the Trie class, it pre-process all strings in text into the trie when instantiated.
        
        @Precondition:       text should only contain strings with lowercase alphabetic characters
        @Arguments:          text = An array containing strings to be added
        @Time complexity:    Best case O(T)
                             Worst case O(T)
                             (T is the total number of characters over all strings in text)
        @Space complexity:   O(T)
        """
        # step 1: Create an instance variable which stores the Node object
        # step 2: Insert each string in text through the insert() method
        self.root = Node()
        #Iterates every string in text
        for item in text:
            #Inserts the string in trie
            self.insert(item)

    def insert(self, key):
        """
        Function to add a word into the Trie
        
        @Precondition:       key should only consist of lowercase alphabets
        @Arguments:          key = A string value to be added to the trie
        @Time complexity:    Best case O(N)
                             Worst case O(N)
                             (N is the number of characters in the given key)
        @Space complexity:   O(q)
        @Aux space complexity: O(1)
        """
        # step 1: Retrieve the root node and set it as current
        # step 2: Use the Node link method to create(if necessary) and retrieve the appropriate child node to store its reference in current
        # step 3: Repeat step 2 for each character in key
        # step 4: Call the increment method of Node on current
        current = self.root
        #For every element in key
        for c in key:
            assert ord(c) >= 97 and ord(c) <= 122,"Text should only contains strings consisting of alphabetic characters"
            #Retrieve the linked child node as set it to current (Creates a child node when necessary)
            current = current.link(c)
        #Increment end_count (To count duplicates and whether the value of current node is also an element in text)
        current.increment()

            
    def string_freq(self, query_str):
        """
        Function to get the number of elements in text which are query_str
        
        @Precondition:       query_str should only consist of lowercase alphabets
        @Arguments:          query_str = The string to search
        @Time complexity:    Best case O(q)
                            Worst case O(q)
                            (q is the length of query_str)
        @Space complexity:    O(q)
        @Aux space complexity: O(1)
        @Return: The number of elements in text which are query_str
        """
        # step 1: Retrieve the root node.
        # step 2: Check if the current node has a linked child node for the corresponding character
        # step 3a: return 0 if check return false (indicating the query_str is not in trie)
        # step 3b: Store the linked child node as the current node
        # step 4: Repeat step 2 to 3 for each character in query_str
        # step last: Return the end count of the current node
        current = self.root
        #For every element in query_str
        for c in query_str:
            assert ord(c) <= 122 and ord(c)>=97, "Query string contains an illegal string character"
            #If the child node does not exist
            if current.check_child(c)== False:
                #Return 0 (Since if the condition is met then no element has the query_str as a prefix)
                return 0
            current = current.get_child(c)
        return current.end_count
    
    def prefix_freq(self, query_str):
        """
        Function to get the number of elements in text which has query_str as its prefix
        
        @Precondition:       query_str should only consist of lowercase alphabets
        @Arguments:          query_str = The prefix used for searching
        @Time complexity:    Best case O(q)
                            Worst case O(q)
                            (q is the length of query_str)
        @Space complexity:    O(q)
        @Aux space complexity: O(1)
        @Return: The number of elements in text which has query_str as its prefix
        """
        # step 1: Retrieve the root node.
        # step 2: Check if the current node has a linked child node for the corresponding character
        # step 3a: return 0 if check return false (indicating there's no string with query_str as a prefix in trie)
        # step 3b: Store the linked child node as the current node
        # step 4: Repeat step 2 to 3 for each character in query_str
        # step last: Return the addition result of end count and prefix count of the current node
        current = self.root
        #For every element in query_str
        for c in query_str:
            assert ord(c) <= 122 and ord(c)>=97, "Query string contains an illegal string character"
            #If the child node does not exist
            if current.check_child(c)== False:
                #Return 0 (Since if the condition is met then no element has the query_str as a prefix)
                return 0
            current = current.get_child(c)
        return current.prefix_count + current.end_count
    
    def wildcard_prefix_freq(self, query_str):
        """
        Function to get all elements in text which has query_str as its prefix in lexicographic order. Furthermore, the query_str may contain a '?' character
        which is used to indicate a wildcard(It represents any lowercase alphabetic characters)
        
        @Precondition:       query_str should only consist of lowercase alphabets
        @Arguments:          query_str = The prefix used for searching
        @Time complexity:    Best case O(q)
                             Worst case O(q+s)
                            (q is the length of query_str)
                            (S is the total number of characters in all strings of the text which have a prefix matching query_str)
        @Space complexity:   O(q+s)
        @Aux space complexity: O(s)
        @Return: An array containing all elements in text which has query_str as a prefix in lexicographic order
        @Description:
        When computing, there are two nested methods which are used for certain part of the process.
        The results to search for can be split into 4 segments
        (start)'?'(end)(...)
        1)The (start) is every character before the wildcard, this is process by the main method wildcard_prefix_freq
        2)? is the wild card, there are many variations of prefixes to search for due to this
        3)The (end) is every character after the wildcard, this segment's input will vary (due to wildcard) and is processed by the nested method, wildcard_aux()
        4)(....) is the unknown characters after prefix, the nested depth_wildcard_aux is used to retrieve all end child nodes values with a given prefix
        """
        # step 1: Retrieve the root node
        # step 2: Check if the current node has a linked child node for the corresponding character
        # step 3a: return 0 if check return false (indicating there's no string with query_str as a prefix in trie)
        # step 3b: Store the linked child node as the current node
        # step 4: Repeat step 2 to 3 for each character in query_str until a '?' character is processed
        # step 5: if a wildcard was found, proceed the iteration but instead store every character as an element in end
        #(step 6-10 will iterate for every potential character the '?' can refer as)
        # step 6: call wildcard_aux and provide the current iterating child node of current and end array
        # step 7: the wildcard_aux will find the next child node (referring to the end array) and store it as current
        # step 8: call depth_wildcard_aux to find all end child node values from current (meaning finding all characters with the prefix variation given)
        # step 9: return the array of values
        # step 10: add the return values to result
        # step last: return the result
        def wildcard_aux(current,res, end, current_ind=0):
            """
            Recursive function used to check if an element in text has the given prefix variation
            If there is, call depth_wildcard_aux() to search and store all elements that meets the criteri
            
            @Arguments:          current = The node to start from
                                 res = the array to store the results
                                 end = the list of yet to be checked characters of the prefix
                                 currend_ind = the current element in end thats being processed
            @Time complexity:    Best case O(p)
                                 Worst case O(p+t)
                                (p is the number of query_str elements which comes after a wildcard element)
                                (t is the total number of characters in all strings of the text which have a prefix matching the current variation of query_str)
            @Space complexity:   O(p+t)
            @Aux space complexity: O(t)
            @Return: An updated res array which stored all elements in text which has the current prefix variation as a prefix
            """
            #If the current node value is the value of the current prefix variation
            if current_ind == len(end):
                #Call depth_wildcard_aux to search all elements in text with the current prefix variation
                depth_wildcard_aux(current,res)
                return res
            #If the current node has no linked child node for the currently processing prefix element
            elif current.check_child(end[current_ind]) == False:
                return []
            else:
                #Recursive call to check the next prefix element
                wildcard_aux(current.get_child(end[current_ind]),res, end, current_ind + 1)
        def depth_wildcard_aux(current, res = []):
            """
            Recursive function used to search and store all elements in text has the given prefix variation as a prefix
            
            @Arguments:          current = The node to start from
                                 res = the array to store the results
            @Time complexity:    Best case O(t)
                                 Worst case O(t)
                                (t is the total number of characters in all strings of the text which have a prefix matching query_str)
            @Space complexity:   O(t)
            @Aux space complexity: O(t)
            @Return: An updated res array which stored all elements in text which has the current prefix variation as a prefix
            """
            #Store current node's value if it is an element in text (store multiple if duplicates exist)
            res += [current.value]*current.end_count
            if current.prefix_count!=0:
                #Find every child node in the current node
                for i in range(97,123):
                    if current.check_child(chr(i)):
                        #If found, perform a recursive call with the child node set as current
                        depth_wildcard_aux(current.get_child(chr(i)),res)
            return res
        res = []
        current = self.root
        #Boolean used as a condition to set the appropriate behaviour for the iteration below
        check_wc = False
        end = []
        assert query_str != "","Query string should not be empty"
        #Iterates all elements in query_str
        for c in query_str:
            #If '?' found
            if c == "?":
                assert check_wc == False,"Query string should only contain 1 '?'"
                #Set Boolean to True
                check_wc = True
            #If '?' not yet found
            elif check_wc == False:
                assert ord(c) <= 122 and ord(c)>=97, "Query string contains an illegal string character"
                if current.check_child(c) == False:
                    return res
                else:
                    #Set linked child node as current
                    current = current.get_child(c)
            #If '?' has been found
            else:
                #Add the element in end
                end.append(c)
        assert check_wc == True,"Query string should contain a '?' character"
        #For every alphabet
        for i in range(97,123):
            #Check if linked child node exist
            if current.check_child(chr(i)):
                wildcard_aux(current.get_child(chr(i)),res, end)
        return res
    
#%% Main driver
if __name__ == "__main__":
    # driver for the test cases
    print("Running test")
    def test_q2():
        #Test for empty trie
        testA = Trie([""])
        #Test for normal trie
        testB = Trie(["the","words","this","and","there","has","the","same","prefix","that","is","th"])
        assert testA.string_freq("no") == 0,"failed test for q2"
        assert testB.string_freq("th") == 1,"failed test for q2"
        assert testB.string_freq("the") == 2,"failed test for q2"
        assert testB.string_freq("averylongword") == 0,"failed test for q2"
        print("pass test for q2")
    def test_q3():
        #Test for empty trie
        testA = Trie([""])
        #Test for normal trie
        testB = Trie(["the","words","this","and","there","has","the","same","prefix","that","is","th"])
        assert testA.prefix_freq("no") == 0,"failed test for q3"
        assert testB.prefix_freq("th") == 6,"failed test for q3"
        assert testB.prefix_freq("the") == 3,"failed test for q3"
        assert testB.prefix_freq("") == 12,"failed test for q3"
        assert testB.prefix_freq("averylongword") == 0,"failed test for q3"
        print("pass test for q3")
    def test_q4():
        #Test for empty trie
        testA = Trie([""])
        #Test for normal trie
        testB = Trie(["the","words","this","and","there","has","the","same","prefix","that","is","th","but","not","tall"])
        assert testA.wildcard_prefix_freq("?") == [],"failed test for q4"
        assert testB.wildcard_prefix_freq("t?") == ['tall', 'th', 'that', 'the', 'the', 'there', 'this'],"failed test for q4"
        assert testB.wildcard_prefix_freq("?a") == ['has', 'same', 'tall'],"failed test for q4"
        assert testB.wildcard_prefix_freq("?") == ['and', 'but', 'has', 'is', 'not', 'prefix', 'same', 'tall', 'th', 'that', 'the', 'the', 'there', 'this', 'words'],"failed test for q4"
        assert testB.wildcard_prefix_freq("the?") == ['there'],"failed test for q4"
        assert testB.wildcard_prefix_freq("th?") == ['that', 'the', 'the', 'there', 'this'],"failed test for q4"
        assert testB.wildcard_prefix_freq("anextremelylongwordthatshouldnotcrashtheprogram") == [],"failed test for q4"
        print("pass test for q4")
    test_q2()
    test_q3()
    test_q4()
    print("pass all test")
