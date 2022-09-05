'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import math,csv,sys #Math imported for math.trunc and math.log2 (Used in Sparse Table)

class End:
    def __init__(self, initial_val=0):
        self.value = initial_val #Value end object represents

    def increment(self):
        self.value += 1 #Increments value by 1

    def get_val(self):
        return self.value #Returns value

class Edge:
    '''
    A class which combines Node and Edge properties,
    each edge has a start and end value along with an array of edges
    '''
    def __init__(self, edge_start=0, edge_end=0, inherit_edges = None):
        '''
        Constructs Edge
        '''
        if inherit_edges:
            self.has_edge = True #For checking if the edge list is empty
            self.edges = inherit_edges #Stores edge list passed from the argument
        else:
            self.has_edge = False #For checking if the edge list is empty
            self.edges = [None]*28 #Generates a new edge list
        '''
        Trick 1: Space-efficient representation of edge-labels/substrings
        Any substring can be represented with two indexes, the start and end of the substring
        '''
        self.start = edge_start #The start-index
        self.end = edge_end #The end-index (Either a value or an End object)
        '''
        Bellow are additional items for Q3 LCP
        '''
        self.length = 0
        self.label = None

    def new_edge(self,key,new_i,end_obj):
        '''
        Branch method 1 (When split isn't required):
        When the edge doesn't need to split, adds new edge to the edges list directly
        
        @Arguments:          current = Active node
                             active_length = Active length
                             n_char = Current i
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        c_index = self.index(key) #Index to store new edge
        self.edges[c_index] = Edge(new_i,end_obj) #Standard edge adding
        
    def branch(self,split_key,new_key,split_i,new_i,end_obj):
        '''
        Branch method 2 (When split is required):
        When a split is required, split the edge first, then add the new edge
        
        @Arguments:          split_key = the character in string[split_i]
                             new_key = the character in string[new_i]
                             split_i = An index within start to end that the split is performed on
                             new_i = the index where the new edge should be stored in edge list
                             end_obj = the end object
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        split_index = self.index(split_key) #The index in the edge list to store the split edge
        new_index = self.index(new_key) #The index in the edge list to store the new edge
        split_end = self.end
        self.end = split_i #This start_index should be the index of the correpsonding key
        inherit_edges = self.edges #Temporary store edges
        self.edges = [None]*28 #New list of edges
        if self.has_edge: #If the current edge's list of edge is not empty, then the split edge inherits its list of edges
            self.edges[split_index] = Edge(split_i,split_end,inherit_edges) 
        else:
            self.edges[split_index] = Edge(split_i,split_end)
        self.edges[new_index] = Edge(new_i,end_obj) #Edge to add after split
        self.has_edge = True #Ensures this edge is labeled to have an edge

    def index(self,key):
        '''
        When storing an edge,
        this function will retrieve the first character and return the appropriate index 
        to store this edge in the edge list
        '''
        ord_val = ord(key)
        if ord_val >= 97: 
            return ord_val-95 #For alphabets
        else:
            return ord_val-35 #For terminal values ($ and #) 

    def get_val(self):
        if not isinstance(self.end, int): #If the edge is not an End object
            return self.start, self.end.get_val()
        return self.start,self.end
        
    def get_edge(self,key):
        return self.edges[self.index(key)] #Get edge from edge list

    def check_edge(self,key):
        if self.edges[self.index(key)]: #Checks if an edge already exist in the edge list for a given key
            return True
        else:
            return False

    def check_node(self):
        return self.has_edge #Return boolean indicating whether the edge list is empty

    def get_end(self):
        if not isinstance(self.end, int): #If the edge is not an End object
            return self.end.get_val()
        return self.end    

    def preprocess(self,edges,euler,depth,fo,suffix_leaf,size,i,d=0,l=0):
        '''
        (All required preprocesses can be done with one visit to each node)
        Preprocessing each edge using an Euler walk (each edge is only visited once)
        In each edge, this function will:
            1. Fill the arrays with apropriate values
            2. Label this edge (For referencing, allows labels to find their associated edges using the edges list)
            3. Store the length of the current edge in the edge itself
        If this is a leaf node:
            4. Store the node itself in the suffix_leaf list
        
        @Arguments:          edges = Edge list (Ordered by labels)
                             euler = Euler walk array (Uses Edge labels)
                             depth = Depth of nodes in Euler walk array
                             fo = First occurence of a given node in Euler walk array
                             suffix_leaf = A list which maps suffix number to leaf nodes
                             size = The size of the string
                             i = the current count of processed edges (Uses End object)
                             d = The previous depth
                             l = The previous length
        @Time complexity:    Best case O(N) (Where N is the number of nodes)
                             Worst case O(N)
        '''
        l = l + self.get_end()-self.start #Computes the length
        self.label = i.get_val()
        edges.append(self)
        euler.append(i.get_val())
        depth.append(d)
        fo.append(len(euler)-1)
        self.length = l #Stores length in the current edge
        if self.has_edge:  #if the edge list is not empty (Not a leaf)
            for edge in self.edges:
                if edge != None:
                    i.increment()
                    edge.preprocess(edges,euler,depth,fo,suffix_leaf,size,i,d+1,l)
                    euler.append(self.label)
                    depth.append(d)            
        else: #if the edge list is empty, this is a leaf node
            '''
            In essence, every leaf node represents a suffix.
            So every leaf node is unique and are based on a suffix in the string.
            In addition, we can determine which suffix this node represents
            using the length of the current edge as every suffix has a different length.
            Thus, with the length of the current node computed:
                If this node is a leaf node, this node represents the suffix of length n.
                n being the length of the current node.
            '''
            suffix_leaf[size-l] = self
            

class Tree:
    def __init__(self,string_A,string_B):
        '''
        Constructs a generalized suffix tree
        '''
        self.end = End() #The end object
        self.root = Edge(0,self.end) #The root
        self.l_size = len(string_A) #The length string's length
        self.r_size = len(string_B) #The right string's length
        self.string = string_A + '#' + string_B + '$' #The string the suffix tree is based on
        self.size = len(self.string) #The length of the whooe string (including terminal values)
        self.Ukkounen() #Build suffix tree using Ukkounen's algorithm
        '''
        Bellow are additional items for Q3 LCP
        '''
        self.edges = [] #To assist on node searching O(1)
        self.euler = [] #Euler walk array (Store labels of edges)
        self.depth = [] #Tracks the depth of nodes in euler walk array
        self.fo = [] #First appearance of edge in the Euler walk/Depth list
        self.sparse = None #Sparse table for Depth list
        self.suffix_leaf = [None]*self.size #An array which maps suffix numbers its associated leaf nodes
        self.preprocess() #Performs preprocessing
        
        
    def traverse(self,j,i):
        '''
        From the root, traverse down the tree till a character
        mismatch (Branch) or the last character was reached (Already exist)
        (Implemented trick 3 to skip redundant comparisons)
        '''
        res = self.root #The root of the tree
        while j < i:
            k, end = res.get_val()
            '''
            Trick 3: Skip count trick
            Since we know that the substrings between str[0]...str[j-1] already exist.
            We can skip character comparisons for any edge
            which has a length less than the remaining length.
            '''
            if end-k < i-j-1:
                j+=end-k #Skips
                k+=end-k #Skips
            else:
                while k < end:
                    if j==i or self.string[k]!=self.string[j]: #If a string doesn't match or the whole sub-string[:j] already exist
                        return res, j, k
                    k+=1
                    j+=1
            if j!=i and j<self.size and res.check_edge(self.string[j]): #Not the last string char, has edge
                res = res.get_edge(self.string[j])
            else: #If no edge is found 
                return res, j, k

    def check_next(self,current,active_length,n_char):
        '''
        (Used for the showstopper trick)
        Instead of traversing the tree, use the active edge and active length
        and only check the next character i.
        
        @Arguments:          current = Active node
                             active_length = Active length
                             n_char = Current i
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        start, end = current.get_val()
        if n_char < self.size and start+active_length+1 < end: #If string[i] matches (already exist)
            if self.string[start+active_length+1] == self.string[n_char]:
                return current, active_length+1
        elif n_char < self.size and current.check_edge(self.string[n_char]): #If the current edge is done, checks the next edge
            current = current.get_edge(self.string[n_char]) #Set active to this new edge (Reset active length)
            return current,0
        #No suffix link, so return None to indicate branch case
        return None, None 
    
    def Ukkounen(self):
        '''
        Ukkounen algorithm, implemented using the 3 rules and 4 tricks.

        @Time complexity:    O(n^2) (Missing suffix link)
        '''
        i = 1
        j = 0
        reset = 0 #The value j resets to each phase
        root_leaf = False #To indicate whether it is currently still the initial root's leaf extension
        active_node = None #Active edge
        active_length = None #Active length
        while i <= self.size: #Phases
            '''
            Trick 2.1: Rapid leaf extension trick (Increment mechanic)
            Once a leaf, always a leaf.
            Incrementing end essentially performs an extension
            on all leaves.
            '''
            self.end.increment()
            while j < i: #Suffix extension
                '''
                Trick 4: Showstopper trick
                if a previous phase has proven str[j-1] to already exist
                we dont need to check str[j-1],str[j-2]...
                we only need to check the next character each phase until a suffix extension is required.
                (Pauses j as well)
                '''
                if active_node and i <= self.size:
                    #Only checks the latest character (ignore previous)
                    active_node, active_length = self.check_next(active_node, active_length, i)
                    break
                else:
                    #Gets the last edge that was traversed, the last character during tree traverse and the position to split (if required)
                    current, new_i, split_i = self.traverse(j,i)
                    #Gets the start and end of the current edge
                    current_start, current_end = current.get_val()
                    #+++++(Rule 2: Does not end at leaf)+++++
                    if new_i <= i-1:
                        if split_i==current_end and current.check_node() and not current.check_edge(self.string[new_i]):
                            #If a new edge is required
                            current.new_edge(self.string[new_i],new_i,self.end)
                        else:
                            #If a split is required before extension
                            current.branch(self.string[split_i], self.string[new_i],split_i,new_i,self.end)
                        j+=1
                        '''
                        Trick 2.2: Rapid leaf extension trick (Reset mechanic)
                        The reset allows us to skip the iteration which were meant for
                        leaf extensions since they are already extended automatically. 
                        '''
                        reset = j
                        root_leaf = True
                    #+++++(Rule 3: Already exist)+++++
                    elif root_leaf:
                        active_node, active_length = current, split_i-current_start-1
                    #+++++(Rule 1: End at leaf (Only for the initial root leaf extension)+++++
                    else:
                        j+=1
            j=reset
            i+=1

    def preprocess(self):
        '''
        Function which:
            1. Calls the preprocess recursive function from root.
            2. Creates sparse table.
        This preprocessing makes finding longest common prefix for any given i and j values in O(1)
        The preprocess itself has an O(N) time complexity, where N is the number of nodes

        Concept:
        (Reminder: Edges and nodes are combined, so the edges and nodes use the same class)
        GST:
            Since this is a generalised suffix tree,
            if there exist a common prefix for a given suffix of the first string and a given suffix of the second string
            There would be a common ancestors for these two suffixes thats not the root.
            The lowest common ancestor of these suffixes within the GSF is also the longest common prefix.
            So if we can find the lowest common ancestor, the length up till that node is the length of the longest common prefix
        Preprocess:
            The length of string for each edge is computed and store in every node.
            An euler walk array is created along with the depth. (Stores labels instead of direct references)
            Another array stores the first appearance of each node in the euler walk.
            In essence, the node with the smallest depth between the two nodes in their
            first appearance in the Euler walk array is the longest common prefix.
            With the usage of a sparse table, the smallest depth value between the first apperance of the two values (i,j)
            can be done in O(1).
            And since the length has already been computed and stored within the array, retrieval of length is also O(1)
            So, by preprocessing the required arrays, we can retrieve the LCP with any given suffix numbers in O(1)
        '''
        self.root.preprocess(self.edges,self.euler,self.depth,self.fo,self.suffix_leaf,self.size,End())
        self.sparse = Sparse_Table(self.depth) #Creates sparse table

    def LCP(self,i,j):
        '''
        Finds the longest common prefix of the suffix of two strings
        
        @Arguments:          i = the suffix number on first string
                             j = the suffix number on second string
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        A = self.fo[self.suffix_leaf[i].label] #Uses array to get index of first appearance of suffix in euler walk array O(1)
        B = self.fo[self.suffix_leaf[self.l_size+j+1].label] #Uses array to get index of first appearance of suffix in euler walk array O(1)
        return self.edges[self.euler[self.sparse.RMQ(A,B)]].length #Using sparse table, find the minimum and get its length O(1)

#====================( New item for Q3 )====================
class Sparse_Table:
    '''
    The sparse table is used so range minimum queries can be computed in O(1).
    It works so that given an array and two values i and j,
    the sparse table can allow us to retrieve the index of the smallest value
    from array[i:j+1] in O(1).

    Dynamic programming:
    Instead of having a table of size NxN for all cases.
    We can reduce it to NxLog(N)+1 instead as when a query is performed.
    This is because the query can decompose to be answered in a form from:
        find the minimum between i and j
    to:
        k = log2(length of i to j)+1
        find the minimum between (minimum of i to k) and (minimum of k to j)
    which greatly reduces preprocessing time and space complexity as well as
    maintain the O(1) range minimum query.
    
    (Used so LCP computation can be done in O(1) after preprocessing)
    '''
    def __init__(self,array):
        '''
        Constructs the sparse table
        '''
        self.array = array #The array itself
        self.length = len(array) #Length of array
        self.ST = [[0 for i in range(self.length)]for j in range(math.trunc(math.log2(self.length))+1)] #ST should be size N*log(N)+1
        self.preprocess() #Preprocess

    def preprocess(self):
        '''
        Preprocess (part of sparse table construction)
        
        @Arguments:          array = list of values
        @Time complexity:    Best case O(N log N)
                             Worst case O(N log N)
        '''
        self.ST[0] = [i for i in range(self.length)] #The minimum from array[i:i+1] is array[i] (Self explanatory)
        for i in range(1,len(self.ST)): #1 to N
            for j in range(self.length - 2**i + 1): #0 to log(N)
                '''
                Essentially, the subsequent rows can be produced with
                comparison of the previous rows rather than comparing one character at a time again.
                '''
                if(self.array[self.ST[i-1][j]] < self.array[self.ST[i-1][j+2**(i-1)]]): #Using the previous computed row (i-1), find the minimum
                    self.ST[i][j] = self.ST[i-1][j]
                else:
                    self.ST[i][j] = self.ST[i-1][j+2**(i-1)]

    def RMQ(self,i,j):
        '''
        Range minimum query, given two values i and j,
        retrieve the index of the smallest value
        in array[i:j+1] in O(1) time.
        
        @Arguments:          array = list of values
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        if i==j:
            return self.array[i]
        elif j < i:
            i,j = j,i
        k = int(math.log2(j-i)+1) #Find where to split
        #if (minimum of i to k) is less than (minimum of k to j)
        if self.array[self.ST[k-1][i]] < self.array[self.ST[k-1][j-2**(k-1)+1]]:
            return self.ST[k-1][i] #return the index of the minimum value in the array from i to k
        else:
            return self.ST[k-1][j-2**(k-1)+1] #return the index of the minimum value in the array from k to j
#========================================================
def read_lst(filename):
    res = []
    with open(filename) as txt:
        rows = txt.read().splitlines()
    res = [[int(i) for i in r.split()] for r in rows]
    return res

def read_str(filename):
    txtFile = open(filename,'r')
    txt = txtFile.read()
    txtFile.close()
    return txt

def writeOutput(lst):
    output = open('output_lcp.txt','w')
    for a,b,w in lst:
        output.write(str(a)+' '+str(b)+' '+str(w)+'\n')
    output.close()
    
if __name__=='__main__':
    #Retrieve file names
    string_A = read_str(sys.argv[1])
    string_B = read_str(sys.argv[2])
    filename_txt = sys.argv[3]
    #Read input files
    queries = read_lst(filename_txt)
    #Create generalised suffix tree
    tree = Tree(string_A, string_B)
    #Output
    lst = []
    for q in queries:
        lst.append([q[0],q[1],tree.LCP(q[0],q[1])])
    writeOutput(lst)
                        
            
