'''
Student ID: 29940672
Name: Tah Wen Zhong
'''
import random, math, sys

def ME(a,b,n):
    '''
    Modular exponentiation using repeated squaring.
    This function performs the binary conversion while calculating
    the results. The conversion is done using the division 
    by 2 method as required since the binary representation
    is required to determine which successive remainder should be
    used to update the result. 
    
    @Arguments:          a = Base integer
                         b = Power
                         n = Modulus
    @Return: The remainder of the Euclidean division of a^b by n
    '''
    res = 1 #Result start with 1 because any value k multiple 1 is still k
    rem = (a%n) #Base case, where b=1
    while b > 0:
        if b%2 == 1: #When the binary representation has a 1 in the current position
            res = (res*rem)%n #Update result
        rem = (rem*rem)%n #Update remainder
        b >>= 1 #Right shift
    return res

def MRRP(n,k):
    '''
    Miller-Rabin’s Randomized Primality testing algorithm.
    Used to test whether the value n is composite or probably a prime number.
    
    @Arguments:          n = Value to test
                         k = Number of test
    @Return: False if n is a composite number, True if n is probably a prime number
    '''
    #Base case: 2 and 3 are prime number
    if n==2 or n==3:
        return True
    #1 or any even number are not prime numbers
    elif n==1 or (n%2==0):
        return False
    s,t = 0,n-1
    while (t%2==0): #While t is an even number
        s += 1
        t = t//2
    for _ in range(k):
        a = random.randrange(2,n-1) #Get a random value from the range [2...n-1)
        if ME(a,n-1,n) != 1: #Use ME() to get the remainder of the Euclidean division of a^n-1 by n
            return False
        prev = ME(a,t,n) #Only the first instance is calculated using ME() function
        for i in range(1,s+1):
            '''
            Optimisation:
            Since we know that,
                A=(a^(2*b))%n
                B=(a^(b))%n
                A = (B*B)%n
            Repeated squaring isn't required as using the formula above, we know that:
                aˆ{2ˆ(i.t)%n = ((aˆ{2ˆ(i-1).t)%n)*(aˆ{2ˆ(i-1).t)%n))%n
            So each iteration produces the value of form B which can be used to calculate
            the value from the next iteration in the form of A.
            This eliminates the need of repeated squaring.
            '''
            current = (prev*prev)%n
            if (current == 1 and (prev!=1 and prev!=n-1)):
                return False
            prev = current
    return True

def prime_prob(n):
    '''
    Calculate the probability of picking a prime number between 1 to n.
    Using the formula n/ln(n).
    
    @Arguments:          n = The max range value
    @Return: Probability value
    '''
    return n/math.log(n)

def twin_prime(m):
    '''
    Twin prime, the function is used to find a twin prime between (2**(m-1) to (2**m)-1).
    It is done by picking a random number within the range and checking if it
    is a prime number, then checks if it is part of a twin prime and returns the value and its twin.
    
    @Arguments:          m = Value used to set the range
    @Return: A twin prime within the given range
    '''
    while True:
        min_r, max_r = 2**(m-1),(2**m)-1 #the min and max range values
        '''
        prob_l = The estimated number of prime numbers in 1 to 2**(m-1)
        prob_r = The estimated number of prime numbers in 1 to (2**m)-1
        (prob_max - prob_min)/(max_r-min_r) = Probability of prime in range (2**(m-1),(2**m)-1)
        (max_r-min_r)/(prob_max - prob_min) = The number of witnesses needed (Minimum should be 64)
        '''
        prob_min, prob_max = prime_prob(min_r), prime_prob(max_r)
        est = math.ceil((max_r-min_r)/(prob_max - prob_min)) #Find the number of witnesses needed
        n = random.randint(min_r,max_r) #Get a random value from the range [2**(m-1)...(2**m)-1]
        k = max(64,est)
        if MRRP(n,k):
            '''
            Explaination
            Since all twin prime numbers excluding (3,5) are of the form (6x-1,6x+1).
            n has to be a value which fits either 6x-1 or 6x+1.
            So, the algorithm will first check if it fits 6x-1 or 6x+1.
            Then based on which side it fits, it will check if the other side fits
            '''
            #(3,5) does not follow the form (6x-1,6x+1), so 5 is a base case
            if n==5 or (((n-1)/6)%1==0 and MRRP(n-2,64)):  #if n fits 6x+1 and 6x-1 is a prime
                return n-2, n
            if ((n+1)/6)%1==0 and MRRP(n+2,64): #if n fits 6x-1 and 6x+1 is a prime
                return n, n+2

#========================================================
def writeOutput(a,b):
    output = open('output_twin_prime.txt','w')
    output.write(str(a)+'\n'+str(b))
    output.close()
    
if __name__=='__main__':
    #Retrieve file names
    m = int(sys.argv[1])
    #Read input files
    a,b = twin_prime(m)
    #Output
    writeOutput(a,b)

