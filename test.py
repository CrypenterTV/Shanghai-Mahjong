from math import ceil


def palindrome(chaine):

    i = 0
    while i < len(chaine) // 2:
        if chaine[i] != chaine[len(chaine) - i - 1]:
            return False
        i += 1
    return True

"""
print(palindrome("ABA"))
print(palindrome("A"))
print(palindrome(""))
print(palindrome("ABBA"))
print(palindrome("ABC"))
print(palindrome("AB"))
"""


def dichotomie(n, L):
    i = 0
    j = len(L) - 1
    while i <= j:
        m = (i + j) // 2
        if L[m] == n:
            return m
        elif L[m] < n:
            i = m + 1
        elif L[m] > n:
            j = m - 1
    return -1


#print(dichotomie(8, [1,2,3,4,5,6,7,8]))

def seuil(n):
    p = 0
    s = 1
    while s <= n:
        s = s *2
        p += 1
    return p

print(seuil(3))

import math
n= 10

for i in range(1, n + 1):

    j = 0

    while j <= math.log(i):

        print("Bonjour !")
        
        j += 1