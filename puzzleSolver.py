import sys
import csv
import copy
import queue
import time
from collections import deque
import itertools as iter

# moves = UP, RIGHT, DOWN, LEFT
moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def getPath(move):
   if move == moves[0]:
      return "U"
   if move == moves[1]:
      return "R"
   if move == moves[2]:
      return "D"
   return "L"

def getReverseMap(move):
   if move == moves[0]:
      return moves[2]
   if move == moves[2]:
      return moves[0]
   if move == moves[1]:
      return moves[3]
   return moves[1]

def findGap(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '':
                return i,j
    return -1, -1

def isPositionLegal(board, x, y):
    n = len(board)
    return ((x >= 0) and (x < n) and (y >= 0) and (y < n))

def nextPos(x,y, move):
    nextX = x + move[0]
    nextY = y + move[1]

    return nextX, nextY

def possibleMoves(board):
    global moves
    x, y = findGap(board)
    res = []
    for mv in moves:
        x2, y2 = nextPos(x, y, mv)
        if isPositionLegal(board, x2, y2):
            res.append(mv)
    return res

def isBoardValid(board):
    x = 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if x == n*n:
                return True
            if board[i][j] == '':
                return False
            if int(board[i][j]) != x:
                return False
            x+=1
    return True

def getVisited(board):
    ret = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '':
                ret += "X"
            else:
                ret += board[i][j]
    return ret

def solvePuzzle(board):
    q = deque()
    q.append(board)
    q.append("")
    explored = {}
    while q:
        st = q.popleft()
        curPath = q.popleft()
        explored[getVisited(st)] = "1"
        x,y = findGap(st)
        if isBoardValid(st) == True:
            outFile.write(curPath[:len(curPath)-2])
            print("success", curPath[:len(curPath)-2])
            return
        temp = possibleMoves(st)
        for z in temp:
            x1 = x+z[0]
            y1 = y+z[1]
            t = copy.deepcopy(st)
            t[x][y] = t[x1][y1]
            t[x1][y1] = ''
            if explored.get(getVisited(t), None)== None:
                q.append(t)
                tempPath = copy.deepcopy(curPath) + getPath(z) + ", "
                q.append(tempPath)
    print("No Solution")

def getCost(board):
    cost = 0
    x = 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '' and int(board[i][j]) != x:
               cost+= 1
            x+=1
    return cost

def getTilePosition(x):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '' and int(board[i][j]) == x:
                return i, j
    return -1,-1

def getManhattanCost(board):
    cost = 0
    x = 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '' and int(board[i][j]) != x:
               cost+= abs(i-(x-1)%3)+abs(j-(x-1)/3)
            x+=1
    return cost

class PQEntry:
    state = []
    cost = 0 
    level = 0
    path = ""
    def __lt__(self, other):
         return (self.cost + self.level) < (other.cost + other.level)

def solvePuzzle2(board):
    q = queue.PriorityQueue()
    entry = PQEntry()
    entry.state = copy.deepcopy(board)
    entry.cost = getCost(board)
    q.put(entry)
    explored = {}
    i = 0
    while q:
        # if i == 10:
        #      break
        i+=1
        entry = q.get()
        explored[getVisited(entry.state)] = "1"
        x,y = findGap(entry.state)
        if entry.cost == 0:
            outFile.write(entry.path[:len(entry.path)-1])
            print("success", entry.level,i)
            return
        temp = possibleMoves(entry.state)
        for z in temp:
            x1 = x+z[0]
            y1 = y+z[1]
            newentry = PQEntry()
            newentry.state = copy.deepcopy(entry.state)
            newentry.state[x][y] = newentry.state[x1][y1]
            newentry.state[x1][y1] = ''
            newentry.level = entry.level + 1
            newentry.cost = getManhattanCost(newentry.state)
            newentry.path = copy.deepcopy(entry.path) + getPath(z) + ","
            # print(getVisited(newentry.path), newentry.cost)
            if explored.get(getVisited(newentry.state), None)== None:
                q.put(newentry)
    print("No Solution")

def solvePuzzle1(board):
    q = queue.PriorityQueue()
    entry = PQEntry()
    entry.state = copy.deepcopy(board)
    entry.cost = getCost(board)
    q.put(entry)
    explored = {}
    i = 0
    while q:
        i+=1
        entry = q.get()
        explored[getVisited(entry.state)] = "1"
        x,y = findGap(entry.state)
        if entry.cost == 0:
            outFile.write(entry.path[:len(entry.path)-1])
            print("success", entry.level, i, entry.path[:len(entry.path)-1])
            return
        temp = possibleMoves(entry.state)
        for z in temp:
            x1 = x+z[0]
            y1 = y+z[1]
            newentry = PQEntry()
            newentry.state = copy.deepcopy(entry.state)
            newentry.state[x][y] = newentry.state[x1][y1]
            newentry.state[x1][y1] = ''
            newentry.level = entry.level + 1
            newentry.cost = getCost(newentry.state)
            newentry.path = copy.deepcopy(entry.path) + getPath(z) + ","
            if explored.get(getVisited(newentry.state), None)== None:
                q.put(newentry)
    print("No Solution")

p=0
def solvePuzzle3(board, bound):
    global p
    q = deque()
    entry = PQEntry()
    entry.state = copy.deepcopy(board)
    entry.cost = getCost(board)
    q.append(entry)
    explored = {}
    bound = float("inf")
    while q:
        p+=1
        entry = q.popleft()
        explored[getVisited(entry.state)] = "1"
        x,y = findGap(entry.state)
        if entry.cost == 0:
            outFile.write(entry.path[:len(entry.path)-1])
            print("success", entry.level, p, entry.path[:len(entry.path)-1])
            return -999

        totalCost = entry.level + entry.cost;

        if totalCost > bound:
            return totalCost

        temp = possibleMoves(entry.state)
        for z in temp:
            x1 = x+z[0]
            y1 = y+z[1]
            newentry = PQEntry()
            newentry.state = copy.deepcopy(entry.state)
            newentry.state[x][y] = newentry.state[x1][y1]
            newentry.state[x1][y1] = ''
            newentry.level = entry.level + 1
            newentry.cost = getCost(newentry.state)
            newentry.path = copy.deepcopy(entry.path) + getPath(z) + ","
            if explored.get(getVisited(newentry.state), None)== None:
                q.append(newentry)
    sys.exit(0)

j=0
def solvePuzzle4(board, bound):
    global j
    q = deque()
    entry = PQEntry()
    entry.state = copy.deepcopy(board)
    entry.cost = getCost(board)
    q.append(entry)
    explored = {}
    bound = float("inf")
    while q:
        j+=1
        entry = q.popleft()
        explored[getVisited(entry.state)] = "1"
        x,y = findGap(entry.state)
        if entry.cost == 0:
            outFile.write(entry.path[:len(entry.path)-1])
            print("success", entry.level, j, entry.path[:len(entry.path)-1])
            return -999

        totalCost = entry.level + entry.cost;

        if totalCost > bound:
            return totalCost

        temp = possibleMoves(entry.state)
        for z in temp:
            x1 = x+z[0]
            y1 = y+z[1]
            newentry = PQEntry()
            newentry.state = copy.deepcopy(entry.state)
            newentry.state[x][y] = newentry.state[x1][y1]
            newentry.state[x1][y1] = ''
            newentry.level = entry.level + 1
            newentry.cost = getManhattanCost(newentry.state)
            newentry.path = copy.deepcopy(entry.path) + getPath(z) + ","
            if explored.get(getVisited(newentry.state), None)== None:
                q.append(newentry)
    sys.exit(0)
        
if __name__ == '__main__':
    if len(sys.argv) == 6:
        algo = int(sys.argv[1])
        n = int(sys.argv[2])
        h = int(sys.argv[3])
        inFile = open(sys.argv[4], 'r')
        outFile = open(sys.argv[5], 'w')
        board = list(range(1, n*n + 1))
        with open(sys.argv[4], 'r') as f:
            reader = csv.reader(f)
            board = list(reader)
        if algo == 1:
            if h == 1:
                a = time.time()
                solvePuzzle1(board)
                b = time.time();
                print(b-a)
            else:
                a = time.time()
                solvePuzzle2(board)
                b = time.time()
                print(b-a)
        else: 
            if h == 1:
                a = time.time()
                bound = getCost(board)
                while True:
                    ret = solvePuzzle3(board, bound)
                    if ret == -999:
                        break
                    bound = ret
                b = time.time()
                print(b-a)
            else: 
                a = time.time()
                bound = getCost(board)
                while True:
                    ret = solvePuzzle4(board, bound)
                    if ret == -999:
                        break
                    bound = ret
                b = time.time()
                print(b-a)
    else:
        print("wrong args")
    
