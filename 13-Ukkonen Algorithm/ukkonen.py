'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import csv, sys

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
    def __init__(self, edge_start=0, edge_end=0, s_id = 0, inherit_edges = None):
        '''
        Constructs Edge
        '''
        if inherit_edges:
            self.has_edge = True #For checking if the edge list is empty
            self.edges = inherit_edges #Stores edge list passed from the argument
        else:
            self.has_edge = False #For checking if the edge list is empty
            self.edges = [None]*27 #Generates a new edge list
        self.suffix_id = s_id #The suffix id (For Suffix Array)
        '''
        Trick 1: Space-efficient representation of edge-labels/substrings
        Any substring can be represented with two indexes, the start and end of the substring
        '''
        self.start = edge_start #The start-index
        self.end = edge_end #The end-index (Either a value or an End object)

    def new_edge(self,key,new_i,end_obj,s_id):
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
        self.edges[c_index] = Edge(new_i,end_obj, s_id) #Standard edge adding
        
    def branch(self,split_key,new_key,split_i,new_i,end_obj,s_id):
        '''
        Branch method 2 (When split is required):
        When a split is required, split the edge first, then add the new edge
        
        @Arguments:          split_key = the character in string[split_i]
                             new_key = the character in string[new_i]
                             split_i = An index within start to end that the split is performed on
                             new_i = the index where the new edge should be stored in edge list
                             end_obj = the end object
                             s_id = The suffix ID for the new edge
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        '''
        split_index = self.index(split_key) #The index in the edge list to store the split edge
        new_index = self.index(new_key) #The index in the edge list to store the new edge
        split_end = self.end
        self.end = split_i #This start_index should be the index of the correpsonding key
        inherit_edges = self.edges #Temporary store edges
        self.edges = [None]*27 #New list of edges
        if self.has_edge: #If the current edge's list of edge is not empty, then the split edge inherits its list of edges
            self.edges[split_index] = Edge(split_i,split_end,self.suffix_id,inherit_edges) 
        else:
            self.edges[split_index] = Edge(split_i,split_end,self.suffix_id)
        self.edges[new_index] = Edge(new_i,end_obj,s_id) #Edge to add after split
        self.has_edge = True #Ensures this edge is labeled to have an edge

    def index(self,key):
        '''
        When storing an edge,
        this function will retrieve the first character and return the appropriate index 
        to store this edge in the edge list
        '''
        if key == '$': 
            return 0 #For $
        else:
            return ord(key)-96 #Returns the index of the edge list representing the letter

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

    def get_suffixes(self):
        '''
        Visits every node once (From left to right),
        retrieve suffix_id of leaf nodes. (Which will form the suffix array)
        
        @Time complexity:    Best case O(N) (Number of nodes)
                             Worst case O(N)
        '''
        if not self.has_edge: #if the edge list is not empty
            return [self.suffix_id]
        else:
            res = []
            for edge in self.edges: #for every edge
                if edge != None:
                    res += edge.get_suffixes()
            return res

class Tree:
    def __init__(self,text):
        '''
        Constructs the suffix tree
        '''
        self.end = End() #The end object
        self.root = Edge(0,self.end) #The root
        self.string = text #The string the suffix tree is based on
        self.size = len(text) #The string size
        self.suffix_array = [len(text)]
        self.Ukkounen() #Build suffix tree using Ukkounen's algorithm
        
    def traverse(self,j,i):
        '''
        From the root, traverse down the tree till a character
        mismatch (Branch) or reached the last character (Already exist)
        (Implement trick 3 to skip redundant comparisons)
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
                            current.new_edge(self.string[new_i],new_i,self.end, j)
                        else:
                            #If a split is required before extension
                            current.branch(self.string[split_i], self.string[new_i],split_i,new_i,self.end, j)
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

    def get_suffix_array(self):
        '''
        Visits every node to retrieve the suffix ID and form the suffix array.
        Calls get_suffixes recursive function from root.
        Returns the suffix array
        '''
        res = self.root.get_suffixes()
        return res
#========================================================
def read_str(filename):
    txtFile = open(filename,'r')
    txt = txtFile.read()
    txtFile.close()
    return txt

def writeOutput(lst):
    output = open('output_suffix_array.txt','w')
    for item in lst:
        output.write(str(item)+'\n')
    output.close()
    
if __name__=='__main__':
    #Retrieve file names
    filename_txt = sys.argv[1]
    #Read input files
    string = read_str(filename_txt)+'$'
    #Create suffix tree
    tree = Tree(string)
    #Output
    lst = tree.get_suffix_array()
    writeOutput(lst)
            
