import sys
import time
import random

#Method to get total conflicts for a given state
def getConflicts():
    conflict = 0
    for domain in range(n):
        for neighbour in mapping[domain]:
            if sol[domain] == sol[neighbour]:
                conflict+=1
    return conflict

#Method to get random unassigned domain
def getRandomDomain():
    var = []
    for domain in range(n):
        conflict = 0
        for neighbour in mapping[domain]:
            if sol[domain] == sol[neighbour]:
                conflict += 1
        if conflict != 0:
            var.append(domain)
    return random.choice(var)

#Method to get least conflict color
def getLeastConfictColor(var):
    min = sys.maxsize
    for color in range(k):
        conflict = 0
        for p in mapping[var]:
            if color == sol[p]:
                conflict += 1
        if conflict < min:
            min = conflict
            ret = color   
    return ret 

#main function for min conflict method
def minconflicts():
    for i in range(99999):
        if getConflicts() ==0: #if no of conflicts is zero, we reached goal
            for item in sol:
                outFile.write("%s\n" % item)
            print(sol, i)
            return
        else:
            v = getRandomDomain() #chose a random domain
            t = [color for color in range(k)]
            color = getLeastConfictColor(v)
            for j in range(3*k):
                t.append(color)
            sol[v] =  random.choice(t) #assign least conflict color with problabilty 3/4
    print("No solution")
    outFile.write("No answer")
    return 

#Method to parse input file and populate mapping of neighbours
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
    if len(sys.argv) == 3:
        inFile = open(sys.argv[1], 'r')
        n, k, mapping = parseInput()
        outFile = open(sys.argv[2], 'w')
        # print(mapping)
        #init with random state
        sol = [random.randrange(k) for i in range(n)]
        minconflicts()
    else:
        print("Wrong arguments")