# Kevin Ehlen
# AI
# Puzzle2: 2048

import sys  # for file read-in
import copy # for deep copies in buildTree()
import time # for program runtime

class Game:
  def __init__(self):
    self.goal = 0
    self.gameSize = []    # Needs to be width by height
    self.spawnVals = []
    self.board = []
    self.root = 0
    self.movesHist = []

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
      elif dir == -1:
        for j in range(self.gameSize[1]-1):
          if self.board[i][j] == self.board[i][j+1] and self.board[i][j] != 0:
            self.board[i][j] = 2 * self.board[i][j]
            self.board[i][j+1] = 0

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
    # move right
    #g.merge(1)
    g.board = g.getMove(1)
    g.merge(1)
    g.moveAfterMerge(1)
    if noIns == False:
      g.insertTile()
    g.movesHist.append('R')
  elif dir == 'L':
    # move left
    #g.merge(-1)
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
    #g.merge(1)
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
    #g.merge(-1)
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

  return newG

class State:
  def __init__(self, key):
    self.data = key
    self.child1 = None
    self.child2 = None
    self.child3 = None
    self.child4 = None

  def addChildren(self,c1,c2,c3,c4):
    self.child1 = State(c1) 
    self.child2 = State(c2)
    self.child3 = State(c3)
    self.child4 = State(c4)

# Add possible paths to the children
def buildTree(g):
  tempL = copyGame(g)  # Needed to not refrence orginal object
  tempR = copyGame(g)
  tempU = copyGame(g)
  tempD = copyGame(g)

  

  tempRoot = copyGame(g)
  root = State(tempRoot)

  # Add possible paths
  # List of games
  root.addChildren(moveDir(tempL, 'L', False), moveDir(tempR, 'R', False), moveDir(tempU, 'U', False), moveDir(tempD, 'D', False))

  return root

# Prints the answer state 
# and was originaly for debugging purposes
def printTree(root):
  # Base Case
  if root is None:
    return
  for row in root.data.board:
    for tile in row:
      print(tile, end = " ")
    print()

  if root.child1 is not None:
    # Print Child1
    for row in root.child1.data.board:
      print("\t", row)
    print()
  if root.child2 is not None:
    # Print Child2
    for row in root.child2.data.board:
      print("\t", row)
    print()
  if root.child3 is not None:
    # Print Child3
    for row in root.child3.data.board:
      print("\t", row)
    print()
  if root.child4 is not None:
    # Print Child4
    for row in root.child4.data.board:
      print("\t", row)
    print()


def checkValidMove(state, dir):
  tempGame = copyGame(state.data)
  # If move has no change, then it is invalid
  if moveDir(tempGame, dir, True).board == state.data.board:
    return False
  return True

# Performs the Breadth First Tree Search 
# and returns the answer state
def getOrder(root):
  # Base Case
  if root is None:
    return
  queue = []
  queue.append(root)

  rootChecked = False

  while len(queue) > 0:
    # pop from the queue
    state = queue.pop(0)


    # Enqueue each child
    if state.child1 is not None:
      # If move is not valid, do not extend it (do not add to queue)
      if checkValidMove(state, 'L') == True:
        queue.append(state.child1)
    if state.child2 is not None:
      if checkValidMove(state, 'R') == True:
        queue.append(state.child2)
    if state.child3 is not None:
      if checkValidMove(state, 'U') == True:
        queue.append(state.child3)
    if state.child4 is not None:
      if checkValidMove(state, 'D') == True:
        queue.append(state.child4)

    # Check if state.data has goal state
    # If not buildTree for it
    if isGoalState(state.data) == True:
      # Found Goal
      return state
    else:
      # The root is pre-loaded with children 
      # so this is a one time check
      if rootChecked == True:
        newRoot = buildTree(state.data)
        # If move is not valid, do not extend it (do not add to queue)
        if checkValidMove(state, 'L') == True:
          queue.append(newRoot.child1)
        if checkValidMove(state, 'R') == True:
          queue.append(newRoot.child2)
        if checkValidMove(state, 'U') == True:
          queue.append(newRoot.child3)
        if checkValidMove(state, 'D') == True:
          queue.append(newRoot.child4)
    
    rootChecked = True


def boundedDFS(startS, depth):
  depthHit = False
  frontier = []
  frontier.append(startS)

  while frontier != []:
    top = frontier.pop()

    #printTree(top)

    if len(top.data.movesHist) == depth:
      if isGoalState(top.data) == True:
        return top  # Found Goal
      else:  # Check if has neighbors??
        depthHit = True
    else:
      # Right to Left order
      # Only append if valid state
      newRoot = buildTree(top.data)

      if checkValidMove(top, 'D') == True:
        frontier.append(newRoot.child4)
      if checkValidMove(top, 'U') == True:
        frontier.append(newRoot.child3)
      if checkValidMove(top, 'R') == True:
        frontier.append(newRoot.child2)
      if checkValidMove(top, 'L') == True:
        frontier.append(newRoot.child1)

  return depthHit



def iterativeDeepeningDFS(root):
  # Base Case
  if root is None:
    return

  # if isGoalState(root.data) == True:
  #   # Found Goal
  #   return root

  depth = 0
  res = True

  while res:
    res = boundedDFS(root, depth)
    if type(res) is State:
      return res
    depth += 1


def main():
  # Timer start
  start_time = time.time()

  g1 = Game()   # Create a Game instance
  g1.readFile() # Read the file

  root1 = buildTree(g1) # Load in children states

  #root2 = getOrder(root1) # Perform the BFTS
  root2 = iterativeDeepeningDFS(root1)
  print(int((time.time() - start_time)*1000000))  # Runtime in microseconds
  print(len(root2.data.movesHist))  # Number of 'swipes'
  # Print the moves
  for move in root2.data.movesHist:
    print(move, end = "")
  print()
  # Print the answer board
  printTree(root2)


if __name__ == "__main__":
  main()