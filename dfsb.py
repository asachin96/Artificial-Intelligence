import sys
import copy
from collections import Counter
from collections import deque

#Main method of simple DFSB
def dfsb(numList, i):
	if i == len(numList):
		for key, value in solution.items():
			outFile.write("%s\n" % value)
		print(solution)
		return True

	unusedColor = [q for q in range(0, k)]

	neighbors = mapping.get(i, None)
	if neighbors != None:
		for n in neighbors:
			t = solution.get(n, None)
			if t != None:
				try:
					unusedColor.remove(t)
				except ValueError:
					pass

	if len(unusedColor) == 0:
		return False

	for color in unusedColor:
		solution[i] = color
		ret = dfsb(numList, i+1)
		if ret:
			return ret
		solution.pop(i)
	return False

#Method to perform AC3 heuristic
def AC3(var, domainList):
    queue = [(j, var) for j in mapping[var] if sol[j] == -1]
    global prune
    while queue:
        entry = queue.pop()
        if len(domainList[entry[1]])==1:
            if domainList[entry[1]][0] in domainList[entry[0]]:
                
                domainList[entry[0]].remove(domainList[entry[1]][0])
                if len(domainList[entry[0]])==0:
                    return False, domainList
                queue.extend([(item, entry[0]) for item in mapping[entry[0]] if item!=entry[1] and sol[item]==-1])
    return True, domainList

#Method to order domain based on LCV heuristics
def orderDomainValuesLCV(var, domainList):
    finalList=[]
    for domain in domainList[var]:
        list = [len(domainList[i]) for i in mapping[var] if sol[i] != -1]
        finalList.append([domain, min(list or [0])])
    sortedFinalList = sorted(finalList, key=lambda t: t[1], reverse=True)
    return sortedFinalList

#Method to get min conflict unassigned domain
def getMinConflictDomain(domainList):
	list = [(len(domainList[i]), i) for i in range(0, n) if sol[i] == -1]
	return min(list, key = lambda t: t[0])[1]

#Main method of improved DFSB
def idfsb(domainList):
    if -1 not in sol:
        for item in sol:
            outFile.write("%s\n" % item)
        print(sol)
        return sol
    domain = getMinConflictDomain(domainList)
    for candidate in orderDomainValuesLCV(domain, domainList):
        domainListnew=copy.deepcopy(domainList)
        domainListnew[domain] = [candidate[0]]  
        ret, domainListnew = AC3(domain, domainListnew)
        if ret:
            sol[domain] = candidate[0]
            result = idfsb(domainListnew)
            if result!=0:
                return result
        sol[domain]=-1

    return 0

#main function for min conflict method
def parseInput():
	mapping = {}
	tmp = inFile.readline().split("\t")
	n = int(tmp[0])
	k = int(tmp[2])
	for line in inFile:
		tmp = line.split("\t")
		mapping.setdefault(int(tmp[0]), []).append(int(tmp[1]))
		mapping.setdefault(int(tmp[1]), []).append(int(tmp[0]))
	return n, k, mapping

if __name__ == "__main__":
	if len(sys.argv) == 4:
		inFile = open(sys.argv[1], 'r')
		n, k, mapping = parseInput()
		outFile = open(sys.argv[2], 'w')
		mode = sys.argv[3]
		numList = [i for i in range(n)]
		solution = {}
		prune = 0
		domainList = [[] for k in range(n)]
		for i in range(0,n):
			for j in range(0,k):
				domainList[i].append(j)
		sol = [-1 for i in range(n)]
		# print(mapping)
		if mode == '1':
			if dfsb(numList, 0) == False:
				outFile.write("No answer")
		else:
			idfsb(domainList)
		print(prune)
	else:
		print("Wrong arguments")