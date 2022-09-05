import math

class Vertex:
    def __init__(self,value):
        """
        Parameterized constructor for the Vertex class, it takes a value which is also value it represents.
        
        @Precondition:       value should be an integer
        @Arguments:          value = The value the vertex represents
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        """
        self.value = value
        self.neighbours = []

    def add_neighbour(self,v,w):
        """
        Function that adds a neighbour, which indicates an edge exist between vertex representing value v with the weight stored as well
        
        @Precondition:       An edge does not already exist for this vertex and vertex representing value v
        @Arguments:          v = the vertex value(id) of another vertex to create an edge with
                             w = the weight of the edge
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        """
        check_exist = False
        #If the neighbour exist, just modify the value
        for i in range(len(self.neighbours)):
            if self.neighbours[i][0]==v:
                self.neighbours[i] = (v,w)
                check_exist = True
                break
        assert check_exist == False,"An invalid edge is included in the gfile provided"
        self.neighbours.append((v,w))

    def get_neighbour(self,v):
        """
        Function that retrieves the neighbour with the given v value
        
        @Arguments:          v = the vertex value(id) of another vertex this vertex is neighbour with
        @Time complexity:    Best case O(1)
                             Worst case O(N)
                            (N is the number of elements in self.neighbours)
        @Space complexity:   O(1)
        @Aux space complexity:   O(1)
        @Return: the neighbour (edge) with the v value provided
                 None if the neighbour doesn't exist
        """
        for n in self.neighbours:
            if n[0]==v:
                return n
        return None

    def __repr__(self):
        """
        Function that modifies the str representation of a vertex object to an appropriate string

        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        """
        return str(self.neighbours)

class Graph:
    #-----------------------------Task 1----------------------------
    def __init__(self, gfile):
        """
        Parameterized constructor for graph class, it takes a file name to be used to retrieve the graph to form
        
        @Precondition:       gfile should contain appropriate values in the correct format 
        @Arguments:          gfile = A file of integer values which follows a fixed format in order to process
        @Time complexity:    Best case O(V^2)
                             Worst case O(V^2)
                            (V is the number of vertices in the graph)
        @Space complexity:   O(V+E)
                             (E is the number of edges in the graph)
        @Aux space complexity:   O(V+E)
        """
        # step 1: Calls the read function which reads and process the gfile which returns the processed gfile as an array
        #         of arrays which contain each integers for every line in the gfile
        # step 2: Take the processed file and use the integer of the first line as the number of vertices to create
        # step 3: For every line after the first, take the integer values to form appropriate edges based on the values in the line
        def read(gfile):
            #Opens the file
            f = open(gfile,"r",encoding='utf-8-sig')
            #Store the words in the file to a list
            text = []
            for words in f:
                temp = []
                for line in words.strip("\n").split():
                    temp.append(int(line))
                text.append(temp)
            assert len(text) >= 1,"Invalid file"
            f.close()
            #Returns the list
            return text
        file = read(gfile)
        self.vertices = []
        self.min = 0
        self.max = file[0][0]
        #Produces the vertices
        [self.vertices.append(Vertex(i)) for i in range(self.max)]
        for i in range(1,len(file)):
            assert len(file[i]) == 3,"Invalid file"
            u = file[i][0]
            v = file[i][1]
            w = file[i][2]
            self.add_edge(u,v,w)

    def add_edge(self,u,v,w):
        """
        Function that adds a neighbour for two given vertexs along with the given weight
        @Precondition:       u and v should be an existing vertex
        @Arguments:          u is the value(id) of the first vertex
                             v is the value(id) of the second vertex
                             w is the weight value
        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        @Aux space complexity:   O(1)
        # step 1: Checks if the vertex values are appropriate
        # step 2: Add neighbour u for v and vise versa, along with storing the weight value for both
        """
        check_u = u<self.max and u>=self.min
        check_v = v<self.max and v>=self.min
        assert check_u and check_v, "A parameter provided was invalid in the add_edge method"
        self.vertices[u].add_neighbour(v,w)
        self.vertices[v].add_neighbour(u,w)
    #-----------------------------Task 1----------------------------
    #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #-----------------------------Task 2----------------------------
    def BFS(self, start):
        """
        Function that traverse the graph from the indicated starting vertex. And returns the deepest depth (which is the number of edges needed to reach the furthest vertex)
        @Arguments:          start = The vertex t start traversing from
        @Time complexity:    Best case O(V^2)
                             Worst case O(V^2)
                            (V is the number of vertices)
        @Space complexity:   O(V)
        @Aux space complexity:   O(V)
        @Return: The maximum depth (the number of edges needed to go through to reach the furthest vertex)
        
        @Description:
        A queue will store all of the vertex to visit in order. So it begins from 1 edge away to 2,3,4 all the way to the maximum depth (which is what we are searching for) 
        """
        # step 1: The function will traverse the graph from the starting vertex, so we add it to the queue
        # step 2: The vertex is popped of the queue
        # step 2: The neighbours of the vertex is added to a queue (if they haven't been visited)
        # step 3: The neighbours depth is also stored, and set visited to true (this will prevent the same vertex being visited more than once)
        # step 4: Check if the depth is larger, and if so replace the result to this
        # step 5: Repeat step 2 until the queue is empty
        # final step: All the vertex will be visited and the result will hold the maximum depth
        Queue = []
        dist = []
        [dist.append([False,0]) for _ in range(self.max)]
        depth = 0
        dist[start] = [True,0]
        #This to initialize the queue with the start indicated on the paramter
        for n_val in self.vertices[start].neighbours:
            n = self.vertices[n_val[0]]
            if dist[n.value][0] == False:
                dist[n.value] = [True,1]
                depth = 1
                Queue.append(n.value)
        #For every vertex in the graph
        while len(Queue) != 0:
            current = self.vertices[Queue.pop(0)]
            for n_val in current.neighbours:
                n = self.vertices[n_val[0]]
                if dist[n.value][0] == False:
                    new_dist = dist[current.value][1]+1
                    dist[n.value] = [True,new_dist]
                    #If the maximum depth is more than the previous, replace the value to return
                    if depth < new_dist:
                        depth = new_dist 
                    Queue.append(n.value)
        return depth
        
    def shallowest_spanning_tree(self):
        """
        Function that finds the vertex to start traversing the graph from that produces the minimum depth (the least edges needed to visit the furthest vertex)
        @Time complexity:    Best case O(V^3)
                             Worst case O(V^3)
                            (V is the number of vertices)
        @Space complexity:   O(V)
        @Aux space complexity:   O(V)
        @Return: 1. the vertex which requires the least amount of edges to visit before reaching the furthest vertex
                 2. the least number of edges required to visit the furthest vertex
        @Description:
        The function will iterate for each vertex, having all vertices tested to be the starting vertex to traverse the graph from
        """
        # step 1: Prepare the vertices for looping
        # step 2: Call BFS function to find the maximum depth of the current vertex
        # step 3: Check if the maximum depth of the current vertex is less than the previous, and if so replace the result values
        # step 4: Iterate this till all vertices were used
        min_vertex = None
        min_depth = math.inf
        #For all vertices in the graph
        for v in self.vertices:
            current_depth = self.BFS(v.value)
            #If the result from BFS function is less than the previous, replace the value to return
            if current_depth < min_depth:
                min_vertex = v.value
                min_depth = current_depth
        return min_vertex,min_depth
    #-----------------------------Task 2----------------------------
    #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #-----------------------------Task 3----------------------------
    def dijkstra(self,start):
        """
        Function that performs the dijkstra shortest path algorithm
        
        @Precondition:       The graph can't contain any negative edges
        @Arguments:          start = The vertex which the dijkstra algorithm should start from
        @Time complexity:    Best case O(Elog(V))
                             Worst case O(Elog(V))
                            (E is the number of edges in the graph)
                            (V is the number of vertices in the graph)
        @Space complexity:   O(V+E)
        @Aux space complexity:   O(V+E)
        @Return: A tuple containing the length of the oscillation and the indices of the elements in L which make up the oscillation
        
        @Description:
        The algorithm will find the shortest path from a certain vertex to all others vertices (with the assistance of a minimum heap)
        This works due to the order in which the algorithm performs, all vertices will be used and will follow this order:
        1) Each vertex should be used only once 
        2) The next vertex to used should always be the one requiring the least weight needed to reach and not one used previously
        """
        # step 1: The function will initialize 3 things:
        #         a) An min heap which first element is the size of the min heap
        #           (The minheap will store arrays representing each vertex, it contains the vertex ID of the vertex it represents along with the total weight needed)
        #         b) An array will represent each vertex and store the location of its representation in the min heap
        #         c) An array which is ordered to the vertexID, this will be the result to return
        #           (The result array contains for every vertex the vertexID of previous vertex to visit along the shortest path and the total weight to reach the given vertex)
        # step 2: The function will start by modifying the total weight value of the starting vertex to 0 (which will cause it to rise)
        # step 3: The function causes the min heap to performs a serve, getting the vertex with the least total weight to be used (a sink may occur)
        # step 4: The edges involving the current vertex will be used, computed and compared with previous results, if the weight cost less it will modify it (causing a rise)
        #         (If the edge involes a vertex previously used it is skipped as the algorithm ensures that the total weight stored for that vertex is already the minimum)
        # step 5: step 3 to step 4 will be repeated till the min heap size is 0 (Its a concept so the array representing the min heap doesn't decrease in size)
        # final step: return the final result
        def serve(min_heap,location):
            """
            Function that performs a serve on the min heap.
            
            @Arguments:          min_heap = The min heap to perform the serve on
                                 location = This array contains reference for which vertex is represented by which elements in the min heap
            @Time complexity:    Best case O(1)
                                 Worst case O(log(N))
                                (N is the size of the min heap)
            @Space complexity:   O(1)
            @Aux space complexity:   O(1)
            @Return: The element in the min heap to serve
            """
            # step 1: The function will first retrieve the root of the min heap
            # step 2: The root will then be swapped with the last element in the min_heap
            # step 3: The new root will sink if required, maintaining the min heap
            # step 4: Modify the location elements to ensure the references are correct
            # final step: return the retrieved root value
            ret = min_heap[1]
            A = min_heap[1]
            B = min_heap[min_heap[0]]
            min_heap[1],min_heap[min_heap[0]] = B,A
            location[A[0]] = min_heap[0]
            location[B[0]] = 1
            min_heap[0] -= 1
            k = 1
            #Sink
            while (2*k <= min_heap[0] and min_heap[k][1] > min_heap[2*k][1]) or (2*k+1 <= min_heap[0] and min_heap[k][1] > min_heap[2*k+1][1]):
                A = min_heap[k]
                #Check left child
                if min_heap[k][1] > min_heap[2*k][1] and (2*k+1 > min_heap[0] or min_heap[2*k][1] < min_heap[2*k+1][1]):
                    B = min_heap[2*k]
                    min_heap[k],min_heap[2*k] = B,A
                    location[A[0]] = 2*k
                    location[B[0]] = k
                    k *= 2
                #Check right child
                elif min_heap[k][1] > min_heap[2*k+1][1]:
                    B = min_heap[2*k+1]
                    min_heap[k],min_heap[2*k+1] = B,A
                    location[A[0]] = 2*k+1
                    location[B[0]] = k
                    k = 2*k+1
            return ret
        def modify(min_heap,location,ind,new_dist):
            """
            Function that modifies a value in a min heap (Only a rise would occur as the value changed will always be less than the previous)
            @Arguments:          min_heap = The min heap to perform the serve on
                                 location = This array contains reference for which vertex is represented by which elements in the min heap
                                 ind = The element index in the min heap to modify
                                 new_distance = The new distance to modify to
            @Time complexity:    Best case O(1)
                                 Worst case O(log(N))
                                (N is the number of elements in min heap)
            @Space complexity:   O(1)
            @Aux space complexity:   O(1)
            """
            # step 1: The function first sets the element of the given index to the new total weight (which will always be less than the previous)
            # step 2: The function will perform a rise on the element to ensure the min heap maintain its form
            # step 3: The location array is also updated to ensure reference remains correct
            min_heap[ind][1] = new_dist
            k = ind
            #Rise
            while k>1 and min_heap[k][1] < min_heap[k//2][1]:
                A = min_heap[k]
                B = min_heap[k//2]
                min_heap[k],min_heap[k//2] = B,A
                location[A[0]] = k//2
                location[B[0]] = k
                k = k//2
        location = []
        min_heap = [self.max]
        res = []
        #To initialize the required arrays
        for i in range(self.max):
            location.append(i+1)
            min_heap.append([i,math.inf])
            res.append([None,math.inf])
        res[start] = [None,0]
        modify(min_heap,location,start+1,0)
        #For all vertices (Minimum total weight priority)
        while min_heap[0] != 0:
            current = self.vertices[serve(min_heap,location)[0]]
            #For all edges of the current vertex
            for edge in current.neighbours:
                if location[edge[0]] <= min_heap[0]:
                    dist = min_heap[location[current.value]][1]+edge[1]
                    if dist < min_heap[location[edge[0]]][1]:
                        modify(min_heap,location,location[edge[0]],dist)
                        res[edge[0]] = [current.value,dist]
        return res

    def retrace(self,starts):
        """
        Function that adds a temporary vertex on the graph to represents the start, this allows previous results of a dijkstra algorithm to "retrace steps", explained further in Description
        @Arguments:          starts = Edges to add only to the temporary vertex (which helps represent multiple starting points)
        @Time complexity:    Best case O(Elog(V))
                             Worst case O(Elog(V))
                            (E is the number of edges in the graph)
                            (V is the number of vertices in the graph)
        @Space complexity:   O(V)
        @Aux space complexity:   O(V)
        @Return: The shortest path with multiple starting points
        @Description:
        The retrace function is basically a way to continue a dijkstra algorithm by performing dijkstra once more with the appropriate result values transferred from the previous
        Lets say we require to start at A, head towards either B,C or D and then reach the final location E.
        Computing dijktra on A gives us the shortest path to B,C and D (ignore E)
        So we know the shortest path from A to B,C,D,E but not from A to B,C or D and then to E. (A -> B,C,D,E) is not (A -> B or C or D -> E)
        To fix this we can add a temporary vertex Z which represents A to B,C and D.
        This is done by having Z be neighbours with B,C and D along with the total weights gained from the results of the previous dijkstra.
        Z : [B, ?],[C, ?],[D, ?]
        If we perform dijkstra on Z, the results will be finalised.
        As stated before, this is a continuation of a dijkstra algorithm by doing dijkstra once more. Having the results of the previous one transferred to the current
        """
        # step 1: The function will create a new TEMPORARY vertex for the table
        # step 2: From the filtered results of the previous dijkstra, add these results as neighbours to the temporary vertex (The weights are included)
        # step 3: Perform dijkstra on the table with the temporary vertex addition
        # step 4: Remove temporary vertex and return results
        self.vertices.append(Vertex(self.max))
        #For all locations to form edges with
        for start in starts:
            self.vertices[self.max].add_neighbour(start[0],start[1])
        self.max += 1
        shortest_path = self.dijkstra(self.max-1)
        del self.vertices[self.max-1]
        self.max -= 1
        return shortest_path
            
    def shortest_errand(self,home,destination,ice_locs,ice_cream_locs):
        """
        Function that solves the given problem through the use of the dijkstra algorithm.
        @Arguments:          starts = Edges to add only to the temporary vertex (which helps represent multiple starting points)
        @Time complexity:    Best case O(Elog(V))
                             Worst case O(Elog(V))
                            (E is the number of edges in the graph)
                            (V is the number of vertices in the graph)
        @Space complexity:   O(V)
        @Aux space complexity:   O(V)
        @Return: 1. The shortest distance (total weight) required
                 2. The path which achieves the shortest distance
        @Description:
        The shortest errand function always performs dijkstra algorithm 3 times (fixed number), constants are not included in Big-O so the
        time complexity will remain Elog(V) (The time complexity of dijkstra)
        """
        # step 1: The function will perform dijkstra with home as the start and store the result (Goal: Shortest distance to all ice locs)
        # step 2: The function will perform retrace with the previous result from step 1 after filtering. (Goal: Shortest distance to all ice cream locs after retrieving ice)
        # step 3: The function will perform retrace once more with result from step 2 after filtering. (Goal: Shortest distance from home, to a ice loc, to a ice cream loc and finally the destination)
        # step 4: Store the shortest distance which is store in the result of step 3 where the vertex represents the destination
        # step 5: The get_path function is then called to retrieve sub-paths to form the final path which achieves the shortest distance (uses the results of step 2,3 and 4)
        # step 6: Return the result
        def result_filter(path, locs):
            """
            Filter the results to only have the results of given location
            @Arguments:          path = The results of dijkstra
                                 locs = The locations which results we require
            @Time complexity:    Best case O(n)
                                 Worst case O(n)
                                (n is the number of locs)
            @Space complexity:   O(n)
            @Aux space complexity:   O(n)
            @Return: Filters to retrieve only the results of the given locations on path 
            """
            res = []
            for loc in locs:
                res.append([loc,path[loc][1]])
            return res
        def get_path(path, i):
            """
            Each result from dijkstra contains the sub-path of the final path for the shortest distance to be achieved. This function filters a given result
            to retrieve only the required sub-path
            
            @Arguments:          path = The results of dijkstra
                                 i = The end of the path, which is the start to retrieve the sub-path
            @Time complexity:    Best case O(1)
                                 Worst case O(V)
                                (V is the number of vertices in the graph)
            @Space complexity:   O(V)
            @Aux space complexity:   O(V)
            @Return: 1. The required sub-path to achieve the shortest distance
                     2. The place which the sub-path ends
            """
            ret = []
            while path[i][0] != self.max:
                ret = [i] + ret
                if path[i][0] != None:
                    i = path[i][0]
                else:
                    break
            return ret,i
        results = []
        results.append(self.dijkstra(home))
        results.append(self.retrace(result_filter(results[0],ice_locs)))
        results.append(self.retrace(result_filter(results[1],ice_cream_locs)))
        distance = results[2][destination][1]
        i = destination
        ret = []
        for current in reversed(results):
            path,i = get_path(current,i)
            ret = path + ret
        return distance,ret
        
    #-----------------------------Task 3----------------------------
    #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #---------------------------Additional--------------------------
    def __repr__(self):
        """
        Function that modifies the str representation of a Graph object to an appropriate string

        @Time complexity:    Best case O(1)
                             Worst case O(1)
        @Space complexity:   O(1)
        """
        res = ""
        for vertex in self.vertices:
            res += str(vertex.value) + ": " + str(vertex) + "\n"
        return res

if __name__ == "__main__":
    #The submission won't include test data so the below code is commented out
    test = Graph("test5.txt")
    print(test)
    print(test.shallowest_spanning_tree())
    print(test.shortest_errand(0,5,[1,3],[2,4]))
    #print(test.shortest_errand(0,8,[1,5,8],[4,6]))
