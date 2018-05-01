def ComputeFail(pattern):
# Border Function
    fail = [0]*len(pattern)
    m = len(pattern)
    i = 1
    j = 0
    while (i < m):
        if (pattern[j].lower() == pattern[i].lower()): #j+1 chars match
            fail[i] = j + 1
            i += 1
            j += 1
        elif (j > 0): #j follows matching prefix
            j = fail[j-1]
        else: #no match
            fail[i] = 0
            i += 1
    return fail

def KMP(text, pattern):
    n = len(text)
    m = len(pattern)

    fail = ComputeFail(pattern)    #border function
    #print(fail)

    i, j = 0, 0
    while (i < n):
        if (pattern[j].lower() == text[i].lower()):
            if (j == m - 1): #match
                return i - m + 1
            i += 1
            j += 1
        elif (j > 0):
            j = fail[j-1]   #b(k)
        else:
            i += 1
    return -1 #not match

def KMPMatching(text, keywords):
    keyIdx = -1
    for keyword in keywords:
        keyIdx = KMP(text, keyword)
        if (keyIdx == -1):
            break
    return keyIdx

#print(KMPMatching("ANAK ABABUBABABABA", ["abuba", "anak", "babab"]))
#print(ComputeFail("abacab"))