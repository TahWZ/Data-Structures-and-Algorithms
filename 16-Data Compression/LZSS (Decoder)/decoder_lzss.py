'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import sys

class Node:
    '''
    Node class used to build a Binary trie,
    Only the leaf nodes contain values
    '''
    def __init__(self):
        self.left = None #The left node (Represents 0)
        self.right = None #The right node (Represents 1)
        self.value = None #The value (Only leaf nodes have a value)

    def insert(self,bitstring,i,n,value):
        '''
        Insert function, it will traverse from the current node.
        It traverses based on the current charater 0/1.
        If there is no path, it will create a child node.
        Once the location is reached, the final node is the leaf node
        which will hold the value.
        To avoid the need of string slicing, the string will be passed
        in the argument. With i pointing the current string position and
        n being the number of characters remaining to read from the string
        
        @Arguments:          bitstring = The bitstring
                             i = The current string position
                             n = The number of characters remaining to read from the string
        @Return: The string position after traversal
        '''
        current = self
        end = i+n #The position of the final character to read in the string
        while i < end:
            if bitstring[i] == '0':
                if current.left == None: #If there is no left node
                    current.left = Node() #Create the left node
                    current = current.left #Set current node to left node
                else: #If there is a left node
                    current = current.left #Set current to left node
            else:
                if current.right == None: #If there is no right node
                    current.right = Node() #Create the right node
                    current = current.right #Set current node to left node
                else: #If there is a right node
                    current = current.right #Set current to right node
            i+=1
        current.value = value #Set current node (Leaf) value
        return i

    def get_value(self,bitstring,i):
        '''
        Traverses the tree based on the bitstring values, 
        then retrieves the value.
        (It will traverse till a leaf node is reached)
        
        @Arguments:          string = The bitstring
                             i = The current string position
        @Return: The node value,The next string position
        '''
        current = self #Set current as current node
        while current.value == None:
            if bitstring[i] == '0':
                current = current.left #Set current to left node
            else:
                current = current.right #Set current to right node
            i+=1
        return current.value,i #Return current node value and string position

class Decoder:
    '''
    A decoder class, it contains all the required functions to perform LZSS decoding on a given bitstring.
    The reason it is made in as a class is to eliminate the need of string slicing.
    A pointer will be used throughout to point the current string position.
    The bitstring is stored as an instance variable to remove the need of 
    constantly passing the bitstring as a parameter.
    '''
    def __init__(self,bs):
        self.bs = bs #The bitstring to decode
    
    def bs_number(self, i, n, flip = False):
        '''
        Converts a binary string to a number. The flip parameter is a boolean value
        which indicates that the first value was a flipped bit. Meaning that the
        first value being 0 should actually be 1 but was flipped during Elias coding.
        
        @Arguments:         i = The current string position
                            n = The last string position to read
                            flip = Whether the first bit was flipped
        @Return: The number converted from a binary string
        '''
        if flip: #If first bit was flipped flipped
            res = 2**(n-1) #Treats it as a 1 and retrieve its value
            start = 1 #Iteration starts from the next index
        else:
            res = 0
            start = 0
        for j in range(start,n):
            if self.bs[i+j] == '1':
                res += 2**(n-j-1)
        return res

    def d_huffman(self, i):
        '''
        Decodes a string encoded using Huffman with 7-bit ASCII code.
        
        @Arguments:         i = The current string position
        @Return: The string decoded from a Huffman coding, the current string position
        '''
        res = 0
        for j in range(7): #7-bit ASCII
            if self.bs[i+j] == '1':
                res += 2**(7-j-1)
        return chr(res),i+7

    def d_elias(self,i):
        '''
        Decodes a string encoded using Elias.
        
        @Arguments:         i = The current string position
        @Return: The number decoded from an Elias coding, the current string position
        '''
        n = 1
        while self.bs[i] == '0':
            temp = n
            n = self.bs_number(i,n,True)+1
            i += temp
        return self.bs_number(i,n),i+n

    def d_header(self):
        '''
        Decodes the header part of the bitstring.
        A binary trie is used here to store the decoded characters and
        its codeword, optimizes the codeword retrieve when decoding the data part.
        
        @Return: A binary trie formed from the decoded charaters and their codewords, the current string position
        '''
        b_tree = Node() #The root of the binary tree
        count,i = self.d_elias(0) #The number of unique characters thats expected to be decoded
        for _ in range(count):
            c,i = self.d_huffman(i) #Decode the character
            code_l,i = self.d_elias(i) #Decode the codeword
            i = b_tree.insert(self.bs,i,code_l,c) #Insert to the binary trie
        return b_tree,i

    def d_data(self,b_tree,i):
        '''
        Decodes the data part of the bitstring.
        It loops through each Format-0/1 fields and decode them appropriately:
        Elias, Elias for Format-0 fields
        Huffman for Format-1 field
        The Format-1 field are direct, adding a single character to the result (Uses the binary trie for fast codeword retrieval)
        The Format-0 field will produce two values, offset and length, from (the index of the last character in the result string - offset)
        add the next n characters from that position to the result, where n is the length from the field.
        
        @Arguments:         i = The current string position
        @Return: A binary trie formed from the decoded charaters and their codewords, the current string position
        '''
        res = '' #The result string
        count, i = self.d_elias(i) #The number of Format-0/1 field thats expected to be decoded
        for _ in range(count):
            if self.bs[i] == '0': #Add res[len(res)-offset]...res[len(res)-offset+length] to the result string
                i+=1
                offset, i = self.d_elias(i) #use Elias to get offset
                length, i = self.d_elias(i) #use Elias to get length
                n = len(res) #The length of the result string
                start = n-offset #The start
                end = start + length #The last character in the string to be added
                for j in range(start,end):
                    res += res[j]
            else:
                i+=1
                c,i = b_tree.get_value(self.bs,i) #Get the character's codeword using the binary trie
                res += c
        return res

    def LZSS_decode(self):
        '''
        Main algorithm, its component is broken down to two different functions.
        1. d_header() to handle the header part of the bitstring and get the binary trie for fast codeword retrieval
        2. d_data() to handle the data part of the bitstring and return the decoded string
        
        @Return: Decodes the bitstring
        '''
        b_tree,i = self.d_header()
        return self.d_data(b_tree,i)

#========================================================
def read_str(filename):
    txtFile = open(filename,'r')
    txt = txtFile.read()
    txtFile.close()
    return txt

def writeOutput(res):
    output = open('output_decoder_lzss.txt','w')
    output.write(res)
    output.close()
    
if __name__=='__main__':
    #Read input file
    bitstring = read_str(sys.argv[1])
    #Get result
    decoder = Decoder(bitstring)
    res = decoder.LZSS_decode()
    #Output
    writeOutput(res)
