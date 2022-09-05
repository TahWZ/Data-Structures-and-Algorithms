'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import sys

def Binary_BC_Matrix(pat,n=1):
    """
    Function used to retrieve the Bad Character Matrix with a given pattern.
    The pattern input should consist of only binary values.
    Its intial usage is to find the position of a specific character (If it exist) on the left of any given position.
    If there are multiple instance, the rightmost character's position is stored.
    However, now it finds for specific substrings rather than a character.
    The complexity of this preprocessing will worsen,
    but will optimise the Boyer-Moore algorithm which uses this function.

    !!!Optimisation:
    The function is altered so its capable of handling substring rather than single characters.
    The function will iterate to check every substring of length n for pat through a right to left scan.
    In each iteration, the substrings will determine the placement in the BC matrix.
    The substrings are treated as binary strings.
    Since number of possible binary strings of length n is 2^n.
    The BC matrix will have 2^n rows,
    each row for every unique binary strings of length n.

    @Arguments:          pat = String consisting of binary values
                         n =  The binary size
    @Time complexity:    Best case O(N)
                         Worst case O(N)
    @Space complexity:   O(N)
    @Return: Tne BC Matrix
    """
    m = len(pat) #Length of pattern
    bc_matrix = [] #The Bad Character Matrix
    for i in range(2**n):
        bc_matrix.append([0]*m) #Initialises the matrix
    for i in range(m-1,-2+n,-1): #right-to-left scan
        current = i+1
        bin_value = int(pat[i-n+1:i+1],2) #Binary value for the current substring
        bc_matrix[bin_value][i] = current #Store the position of the current substring to it's appropriate row
        j=i+1
        while j < m and bc_matrix[bin_value][j] == 0: #Updates the previous positions which have a value 0
            bc_matrix[bin_value][j] = current
            j += 1
    return bc_matrix

def GS_Array(pat):
    """
    Function used to retrieve the Good Suffix array with a given pattern.
    The good suffix array is created using the Z-algorithm (Suffix approach) which has Gusfield's improvement
    The GS array stores information of whether there exist some substring on the left portion of a given position in the pattern
    which matches the suffix of pattern on that position.
    It also gives the position of the substring and will retrieve the rightmost substring's position if mutiple
    instances are found.

    @Arguments:          pat = A string value
    @Time complexity:    Best case O(N)
                         Worst case O(N)
    @Space complexity:   O(N)
    @Return: The Good Suffix Array
    """
    m = len(pat) #Size of pattern
    gs_array = [0]*(m+1) #Initialises Good Suffix array
    z_array = z_Algo_S(pat) #Initialises the Z-array (Gained from z_Algo_S())
    for p in range(1,m): #Iterates the results from the z-array to assigned values to appropriate position in the GS array
        j = m - z_array[p-1]
        gs_array[j] = p
    return gs_array

def MP_Array(pat):
    """
    Function used to retrieve the Match Prefix Array with a given pattern.
    The Match Prefix Array is created using the Z-algorithm (Prefix approach)
    Initially, the position of the longest suffix which that matches a prefix of the pattern
    is stored in the MP Array.
    This position is the easily obtainable through the usage of the MP Array

    !!!Optimisation:
    Instead of having one array, there will be two arrays used.
    1) mp_IP: A position array containing all the positions of suffixes which matches a prefix in ascending order
    2) mp_array: The Mp Array that stores an index that refers to mp_IP to gain the position value.

    The reason for this is because with this approach is because with this,
    the next longest suffix which matches a prefix can be obtained easily by using the index mp_array[i]-1,
    
    @Arguments:          pat = A string value
    @Time complexity:    Best case O(N)
                         Worst case O(N)
    @Space complexity:   O(N)
    @Return: Position array,The Match Prefix Array
    """
    m = len(pat) #Size of pattern
    mp_IP = [0] #Position array
    mp_array = [0]*(m+1) #MP array (stores index rather than positions)
    z_array = z_Algo_P(pat) #Initialises the Z-array (Gained from z_Algo_P())
    index = 0
    for i in range(m-1,-1,-1):
        if z_array[i]!=0 and z_array[i]+i+1 == len(pat) + 1:
            index += 1 #Increase index by 1
            mp_IP.append(z_array[i]) #Add position to the Position array
            mp_array[i] = index
        else:
            mp_array[i] = index #Stores the same index as the previous
    return  mp_IP, mp_array

#====================( Main Function: Binary Boyer-Moore )====================

def BM(txt, pat):
    """
    Function which implements the Boyer-Moore Algorithm.
    This function will perform a 
    
    @Arguments:          txt = String to search pattern on
                         pat = The pattern to search for
    @Time complexity:    Best case O(N/M) (M being the pattern size)
                         Worst case O(N)
    @Space complexity:   O(N)
    @Return: An array containing all positions where the pattern can be found in txt
    """
    res = [] #The result
    n=len(txt) #The length of the text
    m=len(pat) #The length of the pattern
    reset=m+1 #The value which is used to reset the break and resume for Galil's optimization
    '''
    Observation:
    The Bad Character array has been altered to handle.
    The char_space determines the number of character spaces .
    From several tests using large txt files and patterns.
    A character space of 3 provide the best performance boost.
    '''
    char_space = 3
    if char_space > m: #The char_space should be less than pattern
        char_space = m

    #=====Preprocesses=====
    bc_matrix = Binary_BC_Matrix(pat,char_space)
    gs_array = GS_Array(pat)
    mp_IP,mp_array = MP_Array(pat)
    #=====================
    
    i = m - 1
    gal_R, gal_B = reset, reset #Initialises the break and resume trackers
    comparison = 0 #The number of character comparison performed
    while i < n: #Iterates every character but will skip if shifts occur
        j = 0 #Pointer on pattern for pattern matching
        while j != m and txt[i-j] == pat[-1-j]: #Loops as long as
            comparison += 1
            #++++( Galil's Optimisation )+++++
            '''
            For both rules, some of the characters are processed when performing them.
            These characters don't require additional processing.
            With the usage of the resume and break trackers,
            these characters can be skipped during processing
            to avoid redundant checking.
            '''
            if m-gal_B-1 == j+1: #Skips if Galil's optimisation is available
                j = m-gal_R-1
            #+++++++++++++++++++++++++++++++++
            j += 1
        gal_R, gal_B = reset, reset #Resets the Galil's optimisation resume and break tracker
        if j<m-1:
            BC_shift = 1 #The shift length (initialised as 1)
            '''
            The below variables are used as temporary storage for the resume and break tracker for GS and BC.
            This is because the rule that gives the best shift are determined at the end.
            So these variable serve to store the tracker values temporarily.
            '''
            BC_gal_B, BC_gal_R = reset, reset #Reset
            GS_gal_B, GS_gal_R = reset, reset #Reset
            if i-j-char_space >= 0:
                '''
                Bad Character Rule:
                The BC rule tells us that if there exist a character to the left that is equal the mismatched character.
                A shift can be done which aligns these two characters when performing the match checking.
                If multiple same characters exist, the rightmost one is used as it is the safe option.

                Optimisation for BC Rule:
                Substrings are checked (Treated as Binary strings) which performs better compared to single characters
                Since the string only consist of binary values [0,1].
                Smaller shifts are done as each characters only vary between two values.
                To avoid this, having more characters to check essentially improves the shifts performed.
                '''
                current_val = int(txt[i-j-char_space+1:i-j+1],2) #Retrieves the substring from the text
                BC = bc_matrix[current_val][m-1-j] #Retrieve the BC score
                if BC == 0: #If no match was found, shift to the front of the mismatched position
                    BC_shift = m-j-char_space+1
                elif m - j - BC > 0 and BC!=0:
                    BC_gal_B = BC-1 #Sets the break position
                    BC_gal_R = BC-char_space #Sets the resume position
                    BC_shift = m - j - BC
            GS = gs_array[m-j]
            GS_shift = 1 #The shift length (initialised as 1)
            if j!=0: #If there is no suffix, then the Good Suffix rule should be skipped
                if GS>0:
                    '''
                    Good Suffix Rule:
                    The GS rule tells us that if the suffix of the pattern match a substring to the left of the pattern.
                    A shift can be done to align this substring with this suffix
                    Because of the Gusfield's implementation, it also checks 1 additional character on the left of substring and suffix.
                    The rightmost option will be used as it is the safe option

                    Optimisation for GS Rule:
                    One additional character can be skipped in the matching process.
                    The character to the left of the suffix and substring is not equal because of the Gusfield improvement.
                    The mismatched character must also not equal the character to the left of the suffix.
                    Initially, the processing of the left character of the substring needs to be done since it was unknown.
                    However, since the string is binary this character can only be either 0 or 1.
                    In essence, we can conclude that this character must be the same as the mismatched character so the processing
                    of this character can be skipped.
                    '''
                    GS_shift = m-GS #The amount to shift
                    GS_gal_B = GS-1
                    GS_gal_R = max(GS-(m-1)+(m-j-1)-1,0) #Optimisation allow 1 additional character to be skipped
                else:
                    '''
                    Mismatched Prefix Rule:
                    The Mismatched Prefix Rule tells us that if Good Suffix Rule fails to find a substring which matches the suffix.
                    Then, if the suffix matches the prefix the prefix can be aligned to the suffix match position.
                    However, we need to find the longest suffix which matches the prefix as skipping this may lead to unsafe shifts.
                    With the use of the MP array, the longest suffix from any given position can be found efficiently

                    Optimisation for MP Rule:
                    Additional shifts can be done if the next character of the prefix match is not equal to the next character in the iteration.
                    The next character in the txt iteration has a 50% chance of being a 0 or 1 which is a high possibility.
                    So if we compare the characters there is a high chance of a mismatched which means more shifts can be done
                    since a mismatch mean the current shift will definitely lead to a pattern mismatch.
                    For a safe shift, we need to check the next longest suffix which matches the prefix of the pattern.
                    With the modifications to the MP array, the next longest suffix match can be easily obtained as the mp_IP array is arranged from longest to smallest suffix.
                    Thus, if we use the index=i-1 on the mp_IP array,
                    the value obtained is the position of the next longest suffix match in the string.
                    With this, we can very efficiently find the appropriate shift to be done.
                    '''
                    mp_index = mp_array[m-j] #The current MP index
                    mp_pos = mp_IP[mp_index] #The position from the MP array
                    #Iterates while there are still positions left in the mp_IP array and the next character in the text is not equal to the character next to the matched prefix
                    while i+1 < n and mp_index > 0 and txt[i+1]!=pat[mp_pos]:
                        mp_index -= 1
                        mp_pos = mp_IP[mp_index]
                    mp_pos = mp_IP[mp_index]
                    GS_shift = m-mp_pos #Updates the shift length
                    if mp_pos != 0: #If position is 0, then a shift of m is done, so no alignment is done which means no Galil's optimisation
                        GS_gal_B = mp_pos #Optimisation allows 1 additional character to be skipped.
                        GS_gal_R = 0
            if BC_shift<GS_shift or (BC_shift==GS_shift and GS_gal_B-GS_gal_R > BC_gal_B-BC_gal_R):
                gal_B, gal_R = GS_gal_B, GS_gal_R
                i+=GS_shift
            else:
                gal_B, gal_R = BC_gal_B, BC_gal_R
                i+=BC_shift
        elif j==m-1:
            #If j points at the last value, the shift length can only be 1.
            i+=1
        else:
            res.append(i-m+1) #The position contains a matching string, so it will be stored in res
            i+=m-mp_IP[mp_array[1]] #If the whole string matches, the MP array can be used to determine the shift length
    print('Number of comparisons: ' + str(comparison))
    return res

#==============================( Z-Algorithms from Question 1 )==============================
        
def z_Algo_P(string):
    """
    A function transferred from my program for Assignment 1 Question 1.
    
    @Arguments:          string = String to be preprocessed
    @Time complexity:    Best case O(M+N) (M being the pattern size)
                         Worst case O(N+N)
    @Space complexity:   O(N)
    @Return: Z array which contains the Z-values (Prefix approach) of the string input
    """
    n = len(string)
    Zarray = [None]*n #Initialises the Z array which stores the Z-values
    Zarray[0] = n #The first value is the size of the string since the full string is a prefix of itself
    k = 1 #The pointer used for character comparison, value should start with 1 and remain greater than 0
    rem = 0 #The number of remaining values
    for i in range(1,n):
        if rem == 0:
            '''
            Case 1: index i is not within the z-box
            When i points to a value that's not within a z-box, there is no memoisation available.
            Hence, character comparison will be required.
            '''
            k = 1 #Resets the pointer when memoisation not available
            count = 0 #Stores the number of matched character comparison
            j = 0 #For the while loop and character comparison
            while i+j < n and string[i+j] == string[j]: #Iterates as long as the characters matched
                if j > 0: #The remaining should only begin starting from the second match
                    rem += 1
                count += 1
                j += 1 #Next character to check for match
            Zarray[i] = count #Store result in Zarray
        else:
            if Zarray[k] < rem:
                '''
                Case 2a: z[k] less than remaining
                When z[k] holds a value less than the number of remaining values,
                the characters from position i up till i+z[k] matches the prefix.
                This is because if z[k] < the number of remaining values,
                then there exist values after i+z[k] which are not matched and are within the z-box
                Hence, z[i] is equal to z[k].
                '''
                Zarray[i] = Zarray[k]
                k+=1 #Updates pointer
                rem -= 1 #Updates remaining count
            elif Zarray[k] > rem:
                '''
                Case 2b: z[k] more than remaining
                if z[k] is more than remaining,
                then that means z[i] will be the number of remaining values.
                This is because z[i] were to match more characters after z[i+rem],
                then the remaining values would had been larger than the current.
                So, the first value outside the z-box will definitely be a mismatch
                Hence, the matched characters are bounded by the remaining.
                Therefore, the remaining is also the number of matched characters.
                '''
                Zarray[i] = rem
                k += 1 #Updates pointer
                rem -= 1 #Updates remaining count
            else:
                '''
                Case 2c: z[k] equals to remaining
                When z[k] is equal to the number of remaining values,
                computation for i till z[i]+rem are the same as z[k]+rem.
                However, the values of z[i]+rem+1 onwards are yet to be computed.
                This means its possible for the next values to match as well.
                Hence, z[i] is equal to z[k]+(The result of comparison)
                '''
                start = Zarray[k] #The Z-score for position k
                count = start #The number of character matches for position i
                j = 0
                #Anything after remaining is unknown, so there is the possibility of matches after outside the Z-box
                while i+j+start < n and string[start+j]==string[i+j+start]:
                    count += 1
                    j += 1 
                Zarray[i] = count
                k += 1 #Updates pointer
                rem -= 1 #Updates remaining count
    return Zarray

def z_Algo_S(string):
    """
    A function transferred from my program for Assignment 1 Question 1.
    
    @Arguments:          string = String to be preprocessed
    @Time complexity:    Best case O(N+M) (M being the pattern size)
                         Worst case O(N+M)
    @Space complexity:   O(N)
    @Return: Z array which contains the Z-values (Suffix approach) of the string input
    """
    n = len(string)
    Zarray = [None]*n #Initialises the array which stores the Z-values
    Zarray[-1] = n #The last value is the size of the string since the full string is a suffix of itself
    k = -2 #Pointer used for character comparison when memoisation is available, starts from -2
    rem = 0 #The number of remaining values
    for i in range(n-2,-1,-1):
        '''
        Case 1: index i is not within the z-box
        When i points to a value that's not within a z-box, there is no memoisation available.
        Hence, character comparison will be required.
        '''
        if rem == 0:
            k = -2 #Resets the pointer when memoisation not available
            count = 0 #Stores the number of matched character comparison
            j = -1 #For the while loop and character comparison
            while i+j+1 >= 0 and string[i+j+1] == string[j]: #Iterates as long as the characters matched
                if j < -1: #The remaining should only begin starting from the second match
                    rem += 1 
                count += 1
                j -= 1 #Next character to check for match
            Zarray[i] = count #Store result in Zarray
        else:
            if Zarray[k] < rem:
                '''
                Case 2a: z[k] less than remaining
                When z[k] holds a value less than the number of remaining values,
                the characters from position i up till i-z[k] matches the suffix.
                This is because if z[k] < the number of remaining values,
                then there exist values after i-z[k] which are not matched and are within the z-box
                Hence, z[i] is equal to z[k].
                '''
                Zarray[i] = Zarray[k]
                k -= 1 #Updates pointer
                rem -= 1 #Updates remaining count
            elif Zarray[k] > rem:
                '''
                Case 2b: z[k] more than remaining
                if z[k] is more than remaining,
                then that means z[i] will be the number of remaining values.
                This is because z[i] were to match more characters after z[i-rem],
                then the remaining values would had been larger than the current.
                So, the first value outside the z-box will definitely be a mismatch
                Hence, the matched characters are bounded by the remaining.
                Therefore, the remaining is also the number of matched characters.
                '''
                Zarray[i] = rem
                k -= 1 #Updates pointer
                rem -= 1 #Updates remaining count
            else:
                '''
                Case 2c: z[k] equals to remaining
                When z[k] is equal to the number of remaining values,
                computation for i till z[i]-rem are the same as z[k]-rem.
                However, the values of z[i]-rem-1 onwards are yet to be computed.
                This means its possible for the next values to match as well.
                Hence, z[i] is equal to z[k]-(The result of comparison)
                '''
                start = Zarray[k] #The Z-score for position k
                count = start #The number of character matches for position i
                j = -1
                #Anything after remaining is unknown, so there is the possibility of matches after outside the Z-box
                while i+j-start+1 >= 0  and string[j-start]==string[i+j-start+1]:
                    count += 1 
                    j -= 1
                Zarray[i] = count
                k -= 1 #Updates pointer
                rem -= 1 #Updates remaining count
    return Zarray

#==============================( Command line functions )==============================

def readFile(filename_pat,filename_txt):
    patFile = open(filename_pat,'r')
    pat = patFile.read()
    patFile.close()
    txtFile = open(filename_txt,'r')
    txt = txtFile.read()
    txtFile.close()
    return pat,txt

def writeOutput(lst):
    output = open('output_binary_boyermoore.txt','w')
    for i in range(len(lst)):
        output.write(str(lst[i])+'\n')
    output.close()

if __name__=='__main__':
    #Retrieve file names
    filename_txt = sys.argv[1]
    filename_pat = sys.argv[2]
    #Read input files
    pat,txt = readFile(filename_pat,filename_txt)
    #Pattern matching
    lst = BM(txt,pat)
    #Output
    writeOutput(lst)
