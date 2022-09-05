#-----------------------------Task 1----------------------------
#(OPTIMAL)
def longest_oscillation(L):
    """
    Function that find the longest oscillation of a given list
    (Optimally)
    @Precondition:       L should contain only integers
    @Arguments:          L = The list integers to find the longest oscillation
    @Time complexity:    Best case O(N)
                         Worst case O(N)
                        (N is the number of elements in L)
    @Space complexity:   O(N)
    @Aux space complexity:   O(N)
    @Return: A tuple containing the length of the oscillation and the indices of the elements in L which make up the oscillation
    
    @Description:
    The list L can contain multiple longest oscillations, but all the occurences follow a pattern where:
        "The list of elements which make up the oscillation will contain 1 element from every interval between all local extreme values in the list"
    Hence, a list of all local extreme values of a given list is also one of longest oscillations for said list(which is what this function returns)
    """
    # step 1: The function will first select the appropriate behaviour for when (n = 0,n = 1, n > 1)
    # step 2a: The function returns (0,[]) and skips the proceeding steps
    # step 2b: The function returns (1,[0]) and skips the proceeding steps
    # step 2c: Create a variable next_extreme which would be used to indicate what the next extreme should be(peak,trough)
    #           next_extreme can store 4 possible values depending on the scenario:
    #               True = when next extreme is a peak
    #               False = when next extreme is a trough
    #               None = when the next extreme was found
    #               "Unknown" = when the next extreme is unknown (For the beginning elements since duplicates can't indicate the next extreme to be found)
    # step 3: Iterate (step 3 to 4) to search for all local extreme values (When a peak is found, next to find would be a trough and vise versa)
    # step 4: If an extreme value is found, store the local extreme value and increment the length of oscillation by 1
    def check(a,b):
        """
        Function that check what the next extreme value should be
        Arguments:          a = the first element for comparison
                            b = the second element for comparison
        Time complexity:    Best case (O(1))
                            Worst case (O(1))
        Space complexity:   O(1)
        Aux space complexity:   O(1)
        Return: True or False (if its Peak or Trough)
                "Unknown" (indicates unknown when the values a and b are duplicates)
        """
        if a < b:
            return True
        elif a > b:
            return False
        else:
            return "Unknown"
    res_L = 0
    res_ind = []
    n = len(L)
    #The following selects the appropriate behavior based on the list length
    if n == 0:
        #if list is empty,no oscillation possible
        return (0,[])
    elif n == 1:
        #if list length is 1,only 1 oscillation can be done
        return (1,[0])
    #The boolean indicates what extreme value to find next (peak(T), trough(F) or unknown(N))
    #next_extreme can store 4 possible values depending on the scenario:
    #       True = when next extreme is a peak
    #       False = when next extreme is a trough
    #       None = to indicate the current next extreme was found
    #       "Unknown" = when the next extreme is unknown (The beginning values may all be duplicates which require further calls to confirm what the next extreme should be)
    next_extreme = "Unknown"
    #If L is a sorted list, then any two values in the list will form one of the longest oscillations for list L
    sorted_check = True
    for i in range(1,n):
        #The starting elements may all contains duplicates, so we can't indicate what the next extreme is so the next_extreme should be "Unknown"
        if next_extreme == "Unknown":
            next_extreme = check(L[i-1],L[i])
            #If the first two elements are not duplicates, then the first element is considered an extreme value
            if i-1 == 0 and next_extreme != "Unknown":
                next_extreme = None
            #If the whole list consist of duplicates
            if i == n-1:
                return (1,[0])
        #This checks if L[i] is a local peak
        if next_extreme==True and L[i]<L[i-1]:
            sorted_check = False
            next_extreme = None
        #This checks if L[i] is the local trough
        elif next_extreme==False and L[i]>L[i-1]:
            sorted_check = False
            next_extreme = None
        #If next_extreme==None, the extreme value is found and located in L[i-1]
        if next_extreme==None:
            next_extreme = check(L[i-1],L[i])
            res_L += 1
            res_ind.append(i-1)
            #When the current iteration is for the last element, it should only be added if:
            #   (the previous element was an extreme value)
            if i == n-1:
                res_L += 1
                res_ind.append(i)
        #If the list is sorted
        if i == n-1 and sorted_check:
            res_L += 1
            res_ind.append(1)
    return (res_L,res_ind)
#-----------------------------Task 1----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#-----------------------------Task 2----------------------------
#(OPTIMAL)
def longest_walk(M):
    """
    Function that find the longest increasing walk in a given matrix
    (Optimally)
    @Precondition:       M should contain a list of lists which all have equal lengths
    @Arguments:          M = a list of n lists
    @Time complexity:    Best case O(nm)
                         Worst case O(nm)
                        (n is the number of rows in M)
                        (m is the number of columns in M)
    @Space complexity:   O(nm)
    @Aux space complexity:   O(nm)
    @Return: A tuple containing the length of the longest walk in M and a list of coordinates which make up the longest walk in M
    
    @Description:
    It's possible to solve the longest_walk without a naive recursive approach because all problems in longest_walk have overlapping subproblems and an optimal substructure.
    For every recursion:
    a) The problem is to find the longest walk possible from the current value
    b) The subproblems are to find the longest walk possible for every adjacent values from the problem
    c) Any value thats larger than all its adjacent values is the base case
    d) If the results for each solution are compared and replaced if larger, the final product would be the longest_walk
    The solution for every problems/subproblems are required from other calls, so if we store these solution the solving process can be skipped (optimal)
    Hence, by storing the longest walk solution for each problem/subproblem the solving process is only required n times 
    """
    # step 1: The function will check if n and m are 0 and perform the appropriate behaviour if so
    # step 2: Iterate(step 3 to 5) every element from each rows of every column and store the best result in every iteration
    # step 3: Check if the longest walk for the current element has already been computed (stored in memory)
    # step 4a: If there is already a solution, return the solution and skip the remaining steps
    # step 4b: If there is the solution was not computed previously, proceed with the remaining steps
    # step 5: Iterate all the adjacent elements and compute the longest walk of all adjacent elements(subproblem undergoes step 2)
    # step 6a: With every subproblem computed, the longest walk for the current element will be computed, stored in memory and returned
    # step 6b: If the current value is the base case, the longest walk can be computed without further recursion and returned
    # step 7: After all the iteration, the best result stored is the longest walk and will be returned
    def directions(d):
        """
        Function that produces a list of all combinations of two values both ranging -d to d stored as a tuple
        Arguments:          d = an integer used to produce the combinations
        Time complexity:    Best case (O(1))
                            Worst case (O(1))
        Space complexity:   O(1)
        Aux space complexity:   O(1)
        Return: A list of all combinations of two values both ranging -d to d stored as a tuple
        """
        result = []
        for i in range(-d,d+1):
            for j in range(-d,d+1):
                result.append((i,j))
        return result
    def find_longest(M,r,c,memory):
        """
        Function the longest walk from the current element
        Arguments:          M = a list of lists
                            r = the row index
                            c = the column index
                            memory = contains the longest walk of elements in M if it computed in a previous call
        Time complexity:    Best case (O(1))
                            Worst case (O(nm))
                            (n is the number of rows in M)
                            (m is the number of columns in M)
        Space complexity:   O(nm)
        Aux space complexity:   O(nm)
        Return: The longest walk from the current element
        """
        #If the longest walk from M[r][c] was already computed, return the previously computed solution
        if memory[r][c]!=None:
            return memory[r][c]
        longest = (1,[(r,c)])
        n = len(M)
        m = len(M[0])
        all_directions = directions(1)
        #Iterates to check all adjacent values
        for direction in all_directions:
            #M[row][col] is an adjacent value of M[r][c]
            row = r+direction[0]
            col = c+direction[1]
            #check if row or col is out of range
            check_row = row<n and row>=0 
            check_col = col<m and col>=0
            #if the row and col or not out of range and the adjacent value is larger than M[r][c]
            if check_row and check_col and M[row][col]>M[r][c]:
                temp = find_longest(M,row,col,memory)
                #Holds the longest walk from M[row][col]
                temp_walks = temp[0]+1
                #Holds the elements that make up the longest walk of M[row][col]
                temp_paths =[(r,c)]
                #If the current longest walk is larger than the previous longest walk, store it
                if max(longest[0], temp_walks)==temp_walks:
                    temp_paths.extend(temp[1])
                    longest = (temp_walks,temp_paths)
        #Store the longest walk from M[r][c]
        memory[r][c] = longest
        return longest
    n = len(M)
    if n == 0:
        return (0 ,[])
    m = len(M[0])
    if m == 0:
        return (0, [])
    memory = []
    #Creates a matrix which will store the longest walk computed for every element in M (Starts out with None)
    for _ in range(n):
        memory.append([None]*m)
    #Stores the longest walk in M
    longestM = [0,[]]
    #Iterates every element in M
    for r in range(n):
        for c in range(m):
            #If the longest walk for the current element was already computed
            if memory[r][c]==None:
                pos = find_longest(M,r,c,memory)
                pos_walks = pos[0]
            else:
                pos = memory[r][c]
                pos_walks = pos[0]
            #Store/updates the longest walk in M
            if max(longestM[0],pos_walks)==pos_walks:
                longestM = pos
    return longestM
#-----------------------------Task 2----------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#------------------------------Test-----------------------------
if __name__ == "__main__":
    # driver for the test cases
    print("Running test")
    def test_q1():
        def check(res,ans):
            if len(res[1]) >= 2:
                CheckAlt = res[1][0]<res[1][1]
                for i in range(1,len(res[1])):
                    if CheckAlt == res[1][i-1]>res[1][i]:
                        return False
                    CheckAlt = res[1][i-1]>res[1][i]
            return res[0]==ans and len(res[1])==ans
        #Test values
        TestA = [1,5,7,4,6,8,6,7,1]
        TestB = [1,1,1,1,1]
        TestC = [1,2,3,4,5,6,7,8,9,10]
        TestD = [10,9,8,7,6,5,4,3,2,1]
        TestE = []
        TestF = [1]
        TestG = [2,-5,7,-7,12,-15]
        #Test with a normal list
        assert check(longest_oscillation(TestA),7),"TestA for q1 failed"
        #Test with a list of duplicates
        assert check(longest_oscillation(TestB),1),"TestB for q1 failed"
        #Test with a list sorted in ascending order
        assert check(longest_oscillation(TestC),2),"TestC for q1 failed"
        #Test with a list sorted in descending order
        assert check(longest_oscillation(TestD),2),"TestD for q1 failed"
        #Test with an empty list
        assert check(longest_oscillation(TestE),0),"TestE for q1 failed"
        #Test with a list of size 1
        assert check(longest_oscillation(TestF),1),"TestF for q1 failed"
        #Test with a list containing negative values
        assert check(longest_oscillation(TestG),6),"TestG for q1 failed"
    def test_q2():
        def check(res,ans):
            return res[0] == ans and len(res[1]) == ans
        #Test values
        TestA = [[1,2,3], [4,5,6], [7,8,9]]
        TestB = [[1,2,3], [1,2,1], [2,1,3]]
        TestC = [[4,6], [7,2]]
        TestD = []
        TestE = [[]]
        TestF = [[-7,-3],[2,1]]
        #Test with a normal matrix
        assert check(longest_walk(TestA),7),"TestA for q2 failed"
        #Test with a normal matrix
        assert check(longest_walk(TestB),3),"TestB for q2 failed"
        #Test with a different matrix size
        assert check(longest_walk(TestC),4),"TestC for q2 failed"
        #Test with an empty list
        assert check(longest_walk(TestD),0),"TestD for q2 failed"
        #Test with a list stored with an empty list
        assert check(longest_walk(TestE),0),"TestE for q2 failed"
        #Test with a normal matrix containing negative values
        assert check(longest_walk(TestF),4),"TestF for q2 failed"
    test_q1()
    test_q2()
    print("pass all")
