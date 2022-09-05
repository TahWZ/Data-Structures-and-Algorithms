'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import sys,heapq

def Huffman(cfreq_lst):
    '''
    Huffman coding, generates prefix-free code word for each character in cfreq_lst.
    The frequency is needed to ensure:
    the shortest code word should be for the most frequent character,
    the second shortest code word should be for the second most frequent character,
    and so on.

    The priority is as followed:
    1. Frequency
    2. Number of characters
    
    @Arguments:         cfreq_lst = A list containing items in with the format [frequency, Number of characters, character list]
    @Return: a list with the code word for all characters in character list, an empty code word will be given if character not in character list
    '''
    chr_lst = ['']*128
    heapq.heapify(cfreq_lst) #Heapify
    if len(cfreq_lst) == 1: #When there is only one unique character
        f_serve = heapq.heappop(cfreq_lst)
        for c in f_serve[2]: #There will be only 1 character here since there is only one unique character
            c_i = ord(c)
            chr_lst[c_i] = '0'
    while cfreq_lst:
        f_serve = heapq.heappop(cfreq_lst) #First serve
        s_serve = heapq.heappop(cfreq_lst) #Second serve
        '''
        Explanation:
        A linked list or reversing a list is not required here since our final output is also a bitstring.
        In a sense, there is no escaping string concatenation since the output is also a bitstring.
        So instead, we can do the concatenation straight. 
        Furthermore, since concatenation is already unavoidable.
        Might as well do the prepending here, since we can just do
            a = b + a
        where b is the character to be preprended on string a.
        '''
        for c in f_serve[2]: #Prepends 0 to all characters in the characters list from the first serve
            c_i = ord(c)
            chr_lst[c_i] = '0' + chr_lst[c_i]
        for c in s_serve[2]: #Prepends 1 to all characters in the characters list from the first serve
            c_i = ord(c)
            chr_lst[c_i] = '1' + chr_lst[c_i]
        if cfreq_lst:
            '''
            Explanation:
            When heapq handles a list, the comparison during rise or sink 
            between two lists will be based on the first element.
            If they are the same, it will compare the next element.
            So, to ensure the priority is correct.
            The format of the list became [frequency, Number of characters, character list]
            As this ensures that frequency takes priority, followed by the number of characters.
            '''
            serve_n = f_serve[1]+s_serve[1] #Calculates the new character list size
            heapq.heappush(cfreq_lst,[f_serve[0]+s_serve[0],serve_n,f_serve[2]+s_serve[2]])
    return chr_lst

def binary(num, flip = False):
    '''
    Converts a number to its bitstring equivalent, using the division by 2 method.
    Elias coding may require the first bit to be flipped.
    So a flip argument can be passed which will flip the first bit.
    
    @Arguments:         num = The number to be converted
                        flip = To determine whether the first bit should be flipped
    @Return: bitstring (May be flipped based on flip argument)
    '''
    if num == 0:
        return '0'
    res = ''
    '''
    Explanation:
    As explained earlier, there is no escaping string concatenation.
    So it will be used here and since prepending will cost the same,
    it will be done straight as well.
    '''
    while num != 0:
        if num%2 == 0 or (flip and num==1): 
            res = '0'+res #Prepend 0 to res
        else:
            res = '1'+res #Prepend 1 to res
        num = num//2
    return res

def bin_char7(char):
    '''
    Comverts a character to its bitstring equivalent in 7-bit ASCII
    
    @Arguments:         char = character to be converted
    @Return: bitstring
    '''
    end = binary(ord(char))
    start = '0'*(7-len(end)) #Ensures that it will be encoded using 7-bit ASCII
    return start+end

def Elias(num):
    '''
    Elias coding, used to encode numbers.
    The way its done is by having the bit length of the number prepended.
    Followed by the bit length of that value prepended.
    And it repeats until 0.
    All bit lengths values that are prepended will have their first bit flipped.
    So only the encoded number will have its first bit being 1.
    
    @Arguments:         char = character to be converted
    @Return: bitstring
    '''
    res = binary(num)
    n = num.bit_length()-1
    while n > 0:
        '''
        Explanation:
        Again, prepending because of concatenation (Explained earlier)
        '''
        res = binary(n,True) + res 
        n = n.bit_length()-1
    return res

def header(string):
    '''
    The main function which constructs a header.
    The header is formed using Huffman and Elias coding.
    The output begins with the number of unique characters in the string (Encoded using Elias)
    Then for each unique character in the string.
    Add them to the output in the following format:
        Character's bitstring equivalent with 7-bit ASCII + The length of the code word (Encoded using Elias) + The code word of the character (Determined using Huffman)
    
    @Arguments:         string = Input string
    @Return: the header(bitstring) for the string
    '''
    res = ''
    n = len(string)
    c_array = [None]*128 #Count array
    cfreq_lst = [] #Character frequency array
    u_char = [] #List of unique characters in string
    u_count = 0 #Number of unique characters, also used for indexing
    for i in range(n):
        ord_c = ord(string[i]) #The ordinal value of the current character, also used for indexing
        if c_array[ord_c] == None: #If this is the first instance of the character
            c_array[ord_c] = u_count #Stores the index where the character string[i] is located in the cfreq_lst
            cfreq_lst.append([1,1,[string[i]]]) #Append item in the format [frequency, number of characters, character list]
            u_char.append(string[i]) #Add new unique character to list
            u_count += 1 #Number of unique character increases by 1
        else:
            cfreq_lst[c_array[ord_c]][0] += 1
    code_map = Huffman(cfreq_lst) #Perform Huffman on cfreq_lst to get code_map
    res += Elias(u_count) #The number of unique characters
    for c in u_char: #For each unique character in string (Not ordered)
        code = code_map[ord(c)] #Get codeword
        res += bin_char7(c) #First add the character encoded using 7-bit ASCII
        res += Elias(len(code)) #Then the length of the codeword
        res += code #Followed by the codeword
    return res

#========================================================
def read_str(filename):
    txtFile = open(filename,'r')
    txt = txtFile.read()
    txtFile.close()
    return txt

def writeOutput(res):
    output = open('output_header.txt','w')
    output.write(res)
    output.close()
    
if __name__=='__main__':
    #Read input file
    bitstring = read_str(sys.argv[1])
    #Get results
    res = header(bitstring)
    #Output
    writeOutput(res)
        

