'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import sys

def union(p_array,x,y):
    '''
    (Union-by-height with path compression)
    Merge two trees and performs path compression when appropriate during find()
    
    @Arguments:          p_array = Parent array
                         x = Node x
                         y = Node y
    @Return: Boolean value based on whether a cycle is not formed after adding this edge
    '''
    r_x = find(p_array,x) #Retrieve the root node which contains x
    r_y = find(p_array,y) #Retrieve the root node which contains y
    if r_x == r_y: #If they belong in same trees
        return False
    h_x = -p_array[r_x]-1 #Get the height value for the tree containing node x 
    h_y = -p_array[r_y]-1 #Get the height value for the tree containing node y
    '''
    Link tree with the smaller height value to the tree with the higher height value
    '''
    if h_x > h_y: #If the tree containing node y has a smaller height
        p_array[r_y] = r_x
    elif h_y > h_x: #If the tree containing node x has a smaller height
        p_array[r_x] = r_y
    else: #If same height, anything works
        p_array[r_x] = r_y
        p_array[r_y] = -(h_y+1) #Update height
    return True

def find(p_array,x):
    '''
    Find the root node of the tree which contains x through recursion:
        1. If the current node is already the root, return the root
        2. If the current node is not a root,
           get the parent of current node and return the
           result of performing find() on this parent node.
           (Which will be the root node)

    Path compression (Improves armotized complexity):
    Have the parent node of the current node redirected the root.
    This effectively reduces the number of operations.
    
    @Arguments:          p_array = Parent array
                         x = Node x
    @Return: The root node of the tree which contains x
    '''
    if (p_array[x] < 0): #If not a root
        return x
    else:
        p_array[x] = find(p_array,p_array[x]) #Redirect parent node to root
        return p_array[x]

def sort_edges(edges):
    #To sort edge list
    edges.sort(key=lambda x: x[2])

def Kruskal(v_count, edges):
    '''
    The Kruskal algorithm is implemented using a disjoint-set data structure.
    In this case, it is used to form a minimum spanning tree with a list of edges.
    The algorithm works by iterating each edge in a list of weight sorted edges, where:
        1. Add if edge does not form a cycle
        2. Discard if edge forms a cycle

    The way it does this is by forming trees in each iteration of edges from a list of edges sorted by weight,
    it uses a parent array to keep track of the parent of any given node.
    (Negative values indicate root nodes)
    In essence, if an edge of two nodes belonging in the same tree is added, then a cycle is formed.
    The root node is always the same for every node within the same tree.
    Hence, using this information we can check and avoid cycles from being formed,
    resulting in a Minimum spanning tree.
    
    @Arguments:          v_count = Number of vertices
                         edges = List of edges
    @Return: List of edges in minimum spanning tree, The total weight
    '''
    sort_edges(edges) #Sorts list of edges
    p_array = [-1]*v_count # Parent array, negative values are root values with the value itself used to track root height
    res = [] # Array which stores the edges which forms the minimum spanning tree
    total = 0 # The total weight of the minimum spanning tree
    for e in edges: # Iterates every edge in the edge list
        if union(p_array,e[0],e[1]):
            res.append(e)
            total += e[2]
    return total, res
#========================================================
def read_lst(filename):
    res = []
    with open(filename) as txt:
        rows = txt.read().splitlines()
    res = [[int(i) for i in r.split()] for r in rows]
    return res

def writeOutput(t,lst):
    output = open('output_kruskals.txt','w')
    output.write(str(t)+'\n')
    for a,b,w in lst:
        output.write(str(a)+' '+str(b)+' '+str(w)+'\n')
    output.close()
    
if __name__=='__main__':
    #Retrieve file names
    v_count = int(sys.argv[1])
    filename_txt = sys.argv[2]
    #Read input files
    edges = read_lst(filename_txt)
    #Create generalised suffix tree
    total,res = Kruskal(v_count,edges)
    #Output
    writeOutput(total,res)
    
