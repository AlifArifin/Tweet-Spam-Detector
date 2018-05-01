def BoyerMoore (text, pattern) :
	LastPattern = BuildLast(pattern)
	t = len(text)
	p = len(pattern)
	i = p - 1
	if (i > t-1) :
		return -1
	j = p - 1 
	while i < t :
		if (((ord(text[i].lower()))>=0) and((ord(text[i].lower())<=128))):
			if (text[i].lower() == pattern[j].lower()) :
				if (j == 0) :
					return i
				else :
					i-=1
					j-=1
			else :
				l = LastPattern[ord(text[i].lower())]
				i = i + p - min(j, l+1)
				j = p - 1
		else :
			i += 1
	return -1

def BuildLast (pattern) :
	LastPattern = []
	for i in range(128):
		LastPattern.append(-1)
	for i in range (len(pattern)) :
		LastPattern[ord(pattern[i].lower())] = i 
	return LastPattern

def BMMatching(text, keywords) :
	keyIdx = -1
	for keyword in keywords :
		keyIdx = BoyerMoore(text,keyword)
		if (keyIdx == -1) :
			break
	return keyIdx

if __name__ == '__main__' :
	text = input()
	patterns = []
	patterns.append("bo")
	patterns.append("rah")
	idx = BMMatching(text,patterns)
	print(idx)
