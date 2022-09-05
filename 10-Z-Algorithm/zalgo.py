'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import sys

def z_Algo_S(string):
    """
    An altered version of the Z-Algorithm which does character comparison for the suffix and performs a right-to-left scan.
    Reason for alteration:
    The function APM() implements the normal Z-algorithm with additional computations for approximate pattern matching.
    However, for APM() to perform the approximate pattern matching, the Z-array from a suffix approach of the Z-Algorithm is required.
    Hence, this altered Z-Algorithm was implemented to provide the Z-array (Suffix approach) needed for the APM() function. 
    
    @Arguments:          string = String to be preprocessed
    @Time complexity:    Best case O(N+M) (M being the pattern size)
                         Worst case O(N+M)
    @Space complexity:   O(N+M)
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

#====================( Main Function: Approximate pattern matching )====================

def APM(txt,pat):
    """
    Function which performs an approximate pattern matching by utilizing Z-algorithms with different implementations.
    (Only positions with an edit distance <=1 are needed to search for)
    The process steps are as followed:
    1. Gain the Z-array (suffix approach) from the z_Algo_S() function
    2. Perform the normal Z-Algorithm but with additional features:
        a. During iteration, the approximate pattern matching will be performed simultaneously
        b. If m > 1, the number of iteration required can be reduced to n-m+2. (n is the size of txt, m is the size of pat)
           This is because if the remaining values to process are less than the pattern size.
           Hence, a possible pattern match can only be done through multiple insert operations.
           However, that also indicates that any position > n-m+2 will require an edit distance larger than 1
           Since only positions with an edit distance of <=1 are required,
           the processing of any characters after n-m+2 can be regarded as redundant.
    3. Return the result gain from the approximate pattern matching

    Optimisations:
    1. Since the approximate pattern matching is done simultaneously, redundant loops are removed.
    2. The iteration is reduced based on the pattern size which may be significant.
    
    @Arguments:          txt = String to be check for pattern matches
                         pat = The pattern string used for matching check
    @Time complexity:    Best case O(N+M) (M being the pattern size)
                         Worst case O(N+M)
    @Space complexity:   O(N+M)
    @Return: A list of tuples (position, edit distance) where edit distance <= 1
    """
    res = [] #Stores all position with edit distance <=1
    m = len(pat) #Length of pattern
    string = pat + '$' + txt
    Zarray_S = z_Algo_S(txt + '$' + pat) # Z-array (Suffix approach)
    #====================( Z-Algorithm Implementation )====================
    n = len(string) #The length of the string variable
    o = len(txt) #The length of the text
    end = n #Initialises the value representing the number of iterations required
    if m > 2 and o >= m:
        '''
        Reducing the number of iteration.
        As explain in the function description,
        it is possible to reduce the number of iterations required based on the pattern size
        '''
        end = n-m+2
    elif o+1 < m:
        '''
        If the pattern is larger than the text size +1.
        The minimum edit distance will be larger than 1.
        So no computation is required.
        As the result will definitely be an empty array
        '''
        end = 0
    Zarray_P = [None]*n #Initialises the Z array which stores the Z-values
    Zarray_P[0] = n #The first value is the size of the string since the full string is a prefix of itself
    k = 1 #The pointer used for character comparison, value should start with 1 and remain greater than 0
    rem = 0 #The number of remaining values
    for i in range(1,end):
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
            Zarray_P[i] = count #Store result in Zarray
        else:
            if Zarray_P[k] < rem:
                '''
                Case 2a: z[k] less than remaining
                When z[k] holds a value less than the number of remaining values,
                the characters from position i up till i+z[k] matches the prefix.
                This is because if z[k] < the number of remaining values,
                then there exist values after i+z[k] which are not matched and are within the z-box
                Hence, z[i] is equal to z[k].
                '''
                Zarray_P[i] = Zarray_P[k]
                k+=1 #Updates pointer
                rem -= 1 #Updates remaining count
            elif Zarray_P[k] > rem:
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
                Zarray_P[i] = rem
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
                start = Zarray_P[k] #The Z-score for position k
                count = start #The number of character matches for position i
                j = 0
                #Anything after remaining is unknown, so there is the possibility of matches after outside the Z-box
                while i+j+start < n and string[start+j]==string[i+j+start]:
                    count += 1
                    j += 1 
                Zarray_P[i] = count
                k += 1 #Updates pointer
                rem -= 1 #Updates remaining count
        if i > m:
            if Zarray_P[i] == m:
                res.append((i-m-1,0))
            else:
                j = i - 2 #The position in the Z-array (Suffix approach) that points to the current position
                '''
                Concept:
                With the information gain from the Z-array (Suffix approach) and the Z-value (prefix approach) for the current position.
                We can check whether a single operation can make a matching string (edit distance of 1).
                @Key point: With the Z-array (Suffix approach), we can know the longest matching suffix from any position.
                Let m represent the pattern length
                Let a represent the length of the longest prefix match (Z-value)
                Let b represent m-a which is the remaining characters that don't match
                (Used for the explanation for the each case)
                '''
                if (j+1 == n-1 or Zarray_S[j+1] != m) and (i-1 == m or Zarray_P[i-1] != m):
                    '''
                    Case D: Insert operation
                    From the position of the last matched character,
                    If there exist a substring from that position which matches the pattern's suffix of length b-1.
                    That indicates only one character was missing after position a.
                    So inserting this character will transform the substring to matches the whole pattern.
                    '''
                    caseI = Zarray_P[i]+Zarray_S[j-1]>=m-1 #Case I: Insert operation
                    '''
                    Case D: Delete operation
                    From the position after the character which caused mismatched,
                    If there exist a substring from that position which matches the pattern's suffix of length b.
                    Then that means deleting the mismatched character will transform the substring to matches the whole pattern.
                    '''
                    caseD = Zarray_P[i]+Zarray_S[j+1]>=m #Case D: Delete operation
                    '''
                    Case S: Substitution operation
                    From the position after the last matched character,
                    If there exist a substring from that position which matches the pattern's suffix of length b-1.
                    Then that means the character at position a+1 was the only mismatched character.
                    So substitution will transform the substring to matches the whole pattern.
                    '''
                    caseS = Zarray_P[i]+Zarray_S[j]==m-1 #Case S: Substitution operation
                    if caseI or caseD or caseS:
                        res.append((i-m-1,1)) #Any of the above case will have an edit distance of 1
    return res

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
    output = open('output_editdist.txt','w')
    for i in range(len(lst)):
        output.write(str(lst[i][0])+' '+str(lst[i][1])+'\n')
    output.close()

if __name__=='__main__':
    #Retrieve file names
    filename_txt = sys.argv[1]
    filename_pat = sys.argv[2]
    #Read input files
    pat,txt = readFile(filename_pat,filename_txt)
    #Pattern matching
    lst = APM(txt,pat)
    #Output
    writeOutput(lst)
    
    
