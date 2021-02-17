# Kevin Ehlen
# AI
# Puzzle3: 2048

import sys  # for file read-in
import copy # for deep copies in buildTree()
import time # for program runtime
from queue import PriorityQueue # for GrBeFGS
from itertools import count # for unique default value in the pq

class Game:
  def __init__(self):
    self.goal = 0
    self.gameSize = []    # Needs to be width by height
    self.spawnVals = []
    self.board = []
    self.root = 0
    self.movesHist = []
    self.score = 0

  # Read-in from the file
  def readFile(self):
    self.goal = int(input())
    self.gameSize = list(map(int, input().split()))
    self.gameSize.reverse() # Account for correct ordering of dimensions
    self.spawnVals = list(map(int, input().split()))
    for rowI, boardLine in enumerate(sys.stdin):
      boardLine = list(map(int, boardLine.strip().split()))
      self.board.append(boardLine)
      if rowI == self.gameSize[0]-1:  # Height of board
        break

  # Print the board
  def write(self):
    for row in self.board:
      for col in row:
        print(col, end = " ")
      print()
    print()

  # Transpose the game board (matrix) to allow all 4 directions 
  # for move and merge algorthims 
  def transpose(self):
    self.board = list(zip(*self.board))
    row = self.gameSize[0]
    self.gameSize[0] = self.gameSize[1]   # Enforce numRows == numCols
    self.gameSize[1] = row
    for i in range(self.gameSize[0]):
      self.board[i] = list(self.board[i])

  # Merges tiles in the direction of the swipe if they are equal
  def merge(self, dir):
    for i in range(self.gameSize[0]):
      if dir == 1:
        for j in range(self.gameSize[1]-1,0,-1):
          if self.board[i][j] == self.board[i][j-1] and self.board[i][j] != 0:
            self.board[i][j] = 2 * self.board[i][j]
            self.board[i][j-1] = 0
            self.score += self.board[i][j]
      elif dir == -1:
        for j in range(self.gameSize[1]-1):
          if self.board[i][j] == self.board[i][j+1] and self.board[i][j] != 0:
            self.board[i][j] = 2 * self.board[i][j]
            self.board[i][j+1] = 0
            self.score += self.board[i][j]

  # Checks to see if other tiles in the same row as merged tiles 
  # and then moves them to directly after merged tile accordingly
  def moveAfterMerge(self, dir):
    lastNumPosition = ()
    for i in range(self.gameSize[0]):
      if dir == 1:
        lastNumPosition = ()
        for j in range(self.gameSize[1]-1,0,-1):
          if lastNumPosition != ():
            if self.board[i][j] == 0 and self.board[i][j-1] != 0:
              self.board[lastNumPosition[0]][lastNumPosition[1]-1] = self.board[i][j-1]
              self.board[i][j-1] = 0
          if self.board[i][j] != 0:
            lastNumPosition = tuple((i,j))
      elif dir == -1:
        lastNumPosition = ()
        for j in range(self.gameSize[1]-1):
          if lastNumPosition != ():
            if self.board[i][j] == 0 and self.board[i][j+1] != 0:
              self.board[lastNumPosition[0]][lastNumPosition[1]+1] = self.board[i][j+1]
              self.board[i][j+1] = 0
          if self.board[i][j] != 0:
            lastNumPosition = tuple((i,j))

  # perform the swipe action and returns a new game board
  def getMove(self, dir):
    tempGame = Game()
    tempGame = self 
    for i in range(tempGame.gameSize[0]):
      if dir == 1:
        for j in range(tempGame.gameSize[1]-1,0,-1):
          if tempGame.board[i][j] == 0:
            for k in range(j,-1,-1):
              if tempGame.board[i][k] != 0:
                tempGame.board[i][j] = tempGame.board[i][k]
                tempGame.board[i][k] = 0
                break
      elif dir == -1:
        for j in range(tempGame.gameSize[1]):
          if tempGame.board[i][j] == 0:
            for k in range(j,tempGame.gameSize[1]):
              if tempGame.board[i][k] != 0:
                tempGame.board[i][j] = tempGame.board[i][k]
                tempGame.board[i][k] = 0
                break
    return tempGame.board

  def insertTile(self):
    # Account for repeat of spawnVals
    if self.root >= len(self.spawnVals):
      self.root = 0
    # Check if upper left is empty
    if self.board[0][0] == 0:
      self.board[0][0] = self.spawnVals[self.root]
      self.root += 1  # Increment root for next spawnVal
    # Check if upper right is empty
    elif self.board[0][self.gameSize[1]-1] == 0:
      self.board[0][self.gameSize[1]-1] = self.spawnVals[self.root]
      self.root += 1  # Increment root for next spawnVal
    # Check if bottom right is empty
    elif self.board[self.gameSize[0]-1][self.gameSize[1]-1] == 0:
      self.board[self.gameSize[0]-1][self.gameSize[1]-1] = self.spawnVals[self.root]
      self.root += 1  # Increment root for next spawnVal
    # Check if bottom left is empty
    elif self.board[self.gameSize[0]-1][0] == 0:
      self.board[self.gameSize[0]-1][0] = self.spawnVals[self.root]
      self.root += 1  # Increment root for next spawnVal
    # Otherwise no tile is spawned

# Check if the goal value is in the game board
def isGoalState(g):
  for row in g.board:
    if g.goal in row:
      return True
  return False    

# Handles all of the functions for each move direction
def moveDir(g, dir, noIns):
  if dir == 'R':
    g.board = g.getMove(1)
    g.merge(1)
    g.moveAfterMerge(1)
    if noIns == False:
      g.insertTile()
    g.movesHist.append('R')
  elif dir == 'L':
    # move left
    g.board = g.getMove(-1)
    g.merge(-1)
    # Need check for other numbers in line to move after a merge
    g.moveAfterMerge(-1)
    if noIns == False:
      g.insertTile()
    g.movesHist.append('L')
  elif dir == 'D':  
    # move down
    g.transpose()
    g.board = g.getMove(1)
    g.merge(1)
    g.moveAfterMerge(1)
    g.transpose()
    if noIns == False:
      g.insertTile()
    g.movesHist.append('D')
  elif dir == 'U':
    # move up
    g.transpose()
    g.board = g.getMove(-1)
    g.merge(-1)
    g.moveAfterMerge(-1)
    g.transpose()
    if noIns == False:
      g.insertTile()
    g.movesHist.append('U')

  return g

# Makes a deep copy of a game
def copyGame(g):
  newG = Game()
  newG.goal = g.goal
  newG.gameSize.extend(g.gameSize)
  newG.spawnVals.extend(g.spawnVals)
  tempRow = []
  for row in g.board:
    tempRow = []
    for col in row:
      tempRow.append(col)
    newG.board.append(tempRow)

  newG.root = copy.deepcopy(g.root)
  newG.movesHist.extend(g.movesHist)
  newG.score = copy.deepcopy(g.score)

  return newG

class State:
  def __init__(self, key):
    self.data = key
    self.child1 = None
    self.child2 = None
    self.child3 = None
    self.child4 = None

  def addC1(self,c1):
    self.child1 = State(c1) 
  def addC2(self,c2):
    self.child2 = State(c2) 
  def addC3(self,c3):
    self.child3 = State(c3) 
  def addC4(self,c4):
    self.child4 = State(c4) 

# Add possible paths to the children
def buildTree(g):
  tempGame = copyGame(g)
  root = State(tempGame)

  # Add possible paths
  if checkValidMove(root, 'L') == True:
    tempL = copyGame(g)
    root.addC1(moveDir(tempL, 'L', False))
  if checkValidMove(root, 'R') == True:
    tempR = copyGame(g)
    root.addC2(moveDir(tempR, 'R', False))
  if checkValidMove(root, 'U') == True:
    tempU = copyGame(g)
    root.addC3(moveDir(tempU, 'U', False))
  if checkValidMove(root, 'D') == True:
    tempD = copyGame(g)
    root.addC4(moveDir(tempD, 'D', False))

  return root

# Prints the answer state 
def printTree(root):
  # Base Case
  if root is None:
    return
  for row in root.data.board:
    for tile in row:
      print(tile, end = " ")
    print()


def checkValidMove(state, dir):
  tempGame = copyGame(state.data)
  # If move has no change, then it is invalid
  if moveDir(tempGame, dir, True).board == state.data.board:
    return False
  return True


# Determine the heuristic 
# It has an emphasis on empty tiles and more larger tiles
def getScore(root):
  numEmpty = 0
  flatBoard = []

  for row in root.data.board:
    for tile in row:
      flatBoard.append(tile)
  flatBoard.sort()

  for i in range(len(flatBoard)-1):
    flatBoard[1] = 2 ** int(flatBoard[1] / 16)  # / by 16 is simply to scale down exponent

  # The pq finds smallest number, so / is necessary for an inverse
  return root.data.goal / (((numEmpty+1) ** 100) + sum(flatBoard))


# Keeps a dictionary of all the visited states so no cycles are possible
visitedBoards = {}
def isVisited(bd):
  # 2d lists are flattened to a string to be hashed
  newBd = ''.join(str(item) for row in bd for item in row)
  if newBd in visitedBoards:
    return True
  return False


# Increments for each state added to the pq 
# as a backup to sort by if the scores tie.
unique = count()

# Implementation of GrBeFGS
def greedyBFS(root):
  score = getScore(root)

  q = PriorityQueue()
  q.put((score, next(unique), root))

  while not q.empty():
    next_item = q.get()
    if isGoalState(next_item[2].data) == True:
      # Goal is found
      return next_item[2]
    else:
      newRoot = buildTree(next_item[2].data)

      # Add the valid children to the pq
      if newRoot.child1 is not None:
        if isVisited(newRoot.child1.data.board) == False:
          if checkValidMove(newRoot, 'L') == True:
            visitedBoards.update({''.join(str(item) for row in newRoot.child1.data.board for item in row): None})
            newScore = getScore(newRoot.child1)
            q.put((newScore, next(unique), newRoot.child1))

      if newRoot.child2 is not None:
        if isVisited(newRoot.child2.data.board) == False:
          if checkValidMove(newRoot, 'R') == True:
            visitedBoards.update({''.join(str(item) for row in newRoot.child2.data.board for item in row): None})
            newScore = getScore(newRoot.child2)
            q.put((newScore, next(unique), newRoot.child2))

      if newRoot.child3 is not None:
        if isVisited(newRoot.child3.data.board) == False:
          if checkValidMove(newRoot, 'U') == True:
            visitedBoards.update({''.join(str(item) for row in newRoot.child3.data.board for item in row): None})
            newScore = getScore(newRoot.child3)
            q.put((newScore, next(unique), newRoot.child3))

      if newRoot.child4 is not None:
        if isVisited(newRoot.child4.data.board) == False:
          if checkValidMove(newRoot, 'D') == True:
            visitedBoards.update({''.join(str(item) for row in newRoot.child4.data.board for item in row): None})
            newScore = getScore(newRoot.child4)
            q.put((newScore, next(unique), newRoot.child4))



def main():
  # Timer start
  start_time = time.time()

  g1 = Game()   # Create a Game instance
  g1.readFile() # Read the file

  root1 = buildTree(g1) # Load in children states

  root2 = greedyBFS(root1)

  print(int((time.time() - start_time)*1000000))  # Runtime in microseconds

  if root2 is not None: # Is none if no solution was found
    print(len(root2.data.movesHist))  # Number of 'swipes'
    # Print the moves
    for move in root2.data.movesHist:
      print(move, end = "")
    print()
    # Print the answer board
    printTree(root2)


if __name__ == "__main__":
  main()