'''
As a reference:

when iteration through the board, the first variable (usually i) refers to the row it is in.
Ex. i = 0 means you are looking somewhere across the TOP of the chessboard.

The second variable (usually j) refers to the column it is in.

If i = 0 and j = 1, then the piece is at the top of the board, and second square from the left.

'''
from nnf import Var, true
from lib204 import Encoding

BOARD_SIZE = 8

#build up arrays used to count how many of a piece there are
def count_builder(name):
  Count = []
  for i in range(BOARD_SIZE**2):
    Count.append([])
    for j in range((BOARD_SIZE**2)+1):
      Count[i].append(Var(f'{name}_count_by_{i}_is_{j}'))

  Total_Count = []
  for i in range(BOARD_SIZE**2+1):
    Total_Count.append(Var(f'{name}_total_is_{i}'))
  return Count, Total_Count


# Space occupied in general
Space_Occupied = []

#Black king stuff
BK_Space_Occupied = []
BK_Potential_Moves = []
BK_Count, BK_Total_Count = count_builder("BK")

#White queen stuff
WQ_Space_Occupied = []
WQ_Count, WQ_Total_Count = count_builder("WQ")

#White pawn stuff
WP_Space_Occupied = []
WP_Count, WP_Total_Count = count_builder("WP")

#White rook stuff
WR_Space_Occupied = []
WR_Count, WR_Total_Count = count_builder("WR")

#White bishop stuff
WB_Space_Occupied = []
WB_Count, WB_Total_Count = count_builder("WB")

#White knight (called "WH" for white horsem because the white king is WK) stuff
WH_Space_Occupied = []
WH_Count, WH_Total_Count = count_builder("WH")

#White Potential Moves
White_Potential_Moves = []

# Creatting the massive arrays of initialized variables needed for the movements/positions of peices.

for i in range(BOARD_SIZE):
    BK_Space_Occupied.append([])
    WQ_Space_Occupied.append([])
    WP_Space_Occupied.append([])
    WR_Space_Occupied.append([])
    WB_Space_Occupied.append([])
    WH_Space_Occupied.append([])
    Space_Occupied.append([])
    White_Potential_Moves.append([])
    for j in range(BOARD_SIZE):
        BK_Space_Occupied[i].append(Var(f'BK_Occupied_{i},{j}'))
        WQ_Space_Occupied[i].append(Var(f'WQ_Occupied_{i},{j}'))
        WP_Space_Occupied[i].append(Var(f'WP_Occupied_{i},{j}'))
        WR_Space_Occupied[i].append(Var(f'WR_Occupied_{i},{j}'))
        WB_Space_Occupied[i].append(Var(f'WB_Occupied_{i},{j}'))
        WH_Space_Occupied[i].append(Var(f'WH_Occupied_{i},{j}'))
        Space_Occupied[i].append(Var(f'Space_Occupied_{i},{j}'))
        White_Potential_Moves[i].append(Var(f'White_Potential_Moves{i},{j}'))
        if j == BOARD_SIZE-1:
          White_Potential_Moves[i].append(Var(f'White_Potential_Moves{i},{j+1}'))

    if i == BOARD_SIZE-1:
      White_Potential_Moves.append([])
      for j in range(BOARD_SIZE):
        White_Potential_Moves[i+1].append(Var(f'White_Potential_Moves{i+1},{j}'))
        if j == BOARD_SIZE-1:
          White_Potential_Moves[i+1].append(Var(f'White_Potential_Moves{i+1},{j+1}'))

# not done with a loop so we can have the handy comments saying what direction each one is for
BK_Moves = []
for i in range(1,10):
  if (i != 5) & (i != 0):
    BK_Moves.append(Var(f'BK_Move_{i}'))
# BK_Move_1 = Var('BK_Move_1') # up-left    0
# BK_Move_2 = Var('BK_Move_2') # up         1
# BK_Move_3 = Var('BK_Move_3') # up-right   2
# BK_Move_4 = Var('BK_Move_4') # left       3
# BK_Move_6 = Var('BK_Move_6') # right      4
# BK_Move_7 = Var('BK_Move_7') # down-left  5
# BK_Move_8 = Var('BK_Move_8') # down       6
# BK_Move_9 = Var('BK_Move_9') # down-right 7
BK_No_Moves = Var('Bk_No_Moves') # true if the black king has no moves (IE everything above is false)

Check = Var('Check')

# the 2 ending configuations. Mutually exclusive, and 1 must be true for the model to exist.
Stalemate = Var('Stalemate')
Checkmate = Var('Checkmate')

# example board config
example_board = [[0,0,0,0,0,0,0,0],
["WQ","WQ","WQ","WQ","WQ",0,0,"WQ"],
[0,0,0,0,"WQ",0,"WQ","WQ"],
[0,"WQ","WQ","WQ",0,0,"WQ","WQ"],
["WQ",0,"WQ","WQ",0,"WQ","WQ",0],
["WQ",0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,"BK",0,0]]

# example_board = [
#   [0,0,0],
#   [0,"WQ",0],
#   ["BK",0,0]
# ]

# function for setting the initial board configuration. ALL it will do is set
# The positions of pieces. This may be a question to ask for feedback, if we can set
# where the king (or other pieces) can move here, but I *think* that would go against
# the idea of using logic, not python programming, to solve it

# Maybe based on the location of the king setting the movement ones to false only in the situation it would be moving
# off the board. The other ones leave to figure out later. Still, maybe the TA's want us to do that with constraints(?)
def parse_board(board):
  #board parser starts here
  f = true
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      if board[i][j]=="BK":
        f &= BK_Space_Occupied[i][j]
      elif board[i][j]=="WQ":
        f &= WQ_Space_Occupied[i][j]
      elif board[i][j]=="WP":
        f &= WP_Space_Occupied[i][j]
      elif board[i][j]=="WR":
        f &= WR_Space_Occupied[i][j]
      elif board[i][j]=="WB":
        f &= WB_Space_Occupied[i][j]
      elif board[i][j]=="WH":
        f &= WH_Space_Occupied[i][j]

      else:
        f &= ~Space_Occupied[i][j]
  return f

#parse the output from the model into a board array
def parse_solution(solution):
  board = [
    [0 for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)
  ]
  if solution == None:
    print("No solution")
    return board
  #replace the 0's with pieces as needed
  x = ''
  for key, value in solution.items():
    if (key[:7] == "BK_Move"):
      x += f'{key}: {value}\n'
    if (key == "Check"):
      print(f"{key}: {value}")
    if (key == "Checkmate") & value:
      print("Checkmate!!")
    if (key == "Stalemate") & value:
      print("Stalemate!!!")
    if (key[:-3] == 'BK_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "BK"
    if (key[:-3] == 'WQ_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WQ"
    if (key[:-3] == 'WP_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WP"
    if (key[:-3] == 'WR_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WR"
    if (key[:-3] == 'WB_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WB"
    if (key[:-3] == 'WH_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WH"
  print(x)

  # # Below is code to also return where white can move. Comment it out when not needed, but it is useful for comparisons
  # board2 = [
  #   [0 for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)
  # ]
  # if solution == None:
  #   print("No solution")
  #   return board2
  # #replace the 0's with pieces as needed
  # for key, value in solution.items():
  #   if (key[:-3] == 'White_Potential_Moves') & value:
  #     if (int(key[-3]) < 8) & (int(key[-1]) < 8):
  #       board2[int(key[-3])][int(key[-1])] = "WT"
  # return board, board2


  return board

def draw_board(board):
  #set any remaining spaces to 2 spaces as empty squares
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      if board[i][j] == 0:
        board[i][j] = "  "

  string = "-"*BOARD_SIZE*3 + "--" + "\n"
  for i in range(BOARD_SIZE):
    string += "|" + "|".join(board[i]) + "|\n"
    string += "-"*BOARD_SIZE*3 + "--" + "\n"
  return string

# little thing that takes an if and only if statement, and returns it in negation normal form.
# Thanks to the professor for this snippet
def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)

def outerBound():
  constraints = []
  for i in range(BOARD_SIZE+1):
    for j in range(BOARD_SIZE+1):
      if (i == BOARD_SIZE) | (j == BOARD_SIZE):
        constraints.append(White_Potential_Moves[i][j])
  return constraints

def rook_move(i, j, goal_i, goal_j):
  f = true.negate()
  k = i
  while (k > 0) & (j == goal_j):
    k-=1
    if (k == goal_i) & (j == goal_j):
      f = true
      for between in range(i-1,goal_i,-1):
        f &= (~Space_Occupied[between][j] | BK_Space_Occupied[between][j])
      return f
  k = i
  while (k < (BOARD_SIZE-1)) & (j == goal_j):
    k+=1
    if (k == goal_i) & (j == goal_j):
      f = true
      for between in range(i+1,goal_i):
        f &= (~Space_Occupied[between][j] | BK_Space_Occupied[between][j])
      return f
  k = j
  while (k > 0) & (i == goal_i):
    k-=1
    if (i == goal_i) & (k == goal_j):
      f = true
      for between in range(j-1,goal_j,-1):
        f &= (~Space_Occupied[i][between] | BK_Space_Occupied[i][between])
      return f
  k = j
  while (k < (BOARD_SIZE-1)) & (i == goal_i):
    k+=1
    if (i == goal_i) & (k == goal_j):
      f = true
      for between in range(j+1,goal_j):
        f &= (~Space_Occupied[i][between] | BK_Space_Occupied[i][between])
      return f
  return f

def bishop_move(i, j, goal_i, goal_j):
  f = true.negate()
  k = i
  l = j
  while (k > 0) & (l > 0):
    k-=1
    l-=1
    if (k == goal_i) & (l == goal_j):
      f = true
      for between in range(1,i-k):
        f &= (~Space_Occupied[i-between][j-between] | BK_Space_Occupied[i-between][j-between])
      return f
  k = i
  l = j
  while (k > 0) & (l < BOARD_SIZE-1):
    k-=1
    l+=1
    if (k == goal_i) & (l == goal_j):
      f = true
      for between in range(1,i-k):
        f &= (~Space_Occupied[i-between][j+between] | BK_Space_Occupied[i-between][j+between])
      return f
  k = i
  l = j
  while (k < BOARD_SIZE-1) & (l > 0):
    k+=1
    l-=1
    if (k == goal_i) & (l == goal_j):
      f = true
      for between in range(1,i-k):
        f &= (~Space_Occupied[i+between][j-between] | BK_Space_Occupied[i+between][j-between])
      return f
  k = i
  l = j
  while (k < BOARD_SIZE-1) & (l < BOARD_SIZE-1):
    k+=1
    l+=1
    if (k == goal_i) & (l == goal_j):
      f = true
      for between in range(1,i-k):
        f &= (~Space_Occupied[i+between][j+between] | BK_Space_Occupied[i+between][j+between])
      return f
  return f

def queen_move(i,j, i_goal, j_goal):
  horizontal_takes = rook_move(i,j, i_goal, j_goal)
  vertical_takes = bishop_move(i,j, i_goal, j_goal)
  return horizontal_takes | vertical_takes

def knight_move(i, j, goal_i, goal_j):
  f = true.negate()
  #move 2, 1
  #left Moves
  if ((i-2) == goal_i):
      if ((j-1) == goal_j):
          f = true
      if ((j+1) == goal_j):
          f = true
  #Right
  if ((i+2) == goal_i):
      if ((j-1) == goal_j):
          f = true
      if ((j+1) == goal_j):
          f = true
  #forwards
  if ((j-2) == goal_j):
      if ((i-1) == goal_i):
          f = true
      if ((i+1) == goal_i):
          f = true
  #backwards
  if ((j+2) == goal_j):
      if ((i-1) == goal_i):
          f = true
      if ((i+1) == goal_i):
          f = true
  return f

def White_Potential_Movement(availablePieces):
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      importantSpot = White_Potential_Moves[i][j]
      f = true.negate()
      for i2 in range(BOARD_SIZE):
        for j2 in range(BOARD_SIZE):
          for piece in availablePieces:
            if piece == WQ_Space_Occupied:
              #queen can't take the spot it is itself on
              if (i2 != i) | (j2 != j):
                queen_spot = WQ_Space_Occupied[i2][j2]
                queen_can_take_i_j = queen_move(i2,j2, i ,j)
                f |= (queen_spot & queen_can_take_i_j)
            if piece == WP_Space_Occupied:
              #In the case of a pawn, the pawn must have an row value 1 smaller than the importantSpot, and a column value either 1 greater or 1 smaller than the importantSpot
              # Translates to: i2 == i-1 (meaning the pawn is 1 above the importantSpot)
              # and (j2 == j-1) | (j2 == j+1) (means the pawn is 1 spot away from the king horizontally)
              # The nice thing about this is it means tthe pawn being able to take the importantSpot is VERY easy to code, just if there's a pawn at a valid location, then
              # it can take the piece
              if (i2 == i-1) & ((j2 ==j-1) | (j2 == j+1)):
                pawn_at = WP_Space_Occupied[i2][j2]
                f |= pawn_at
            if piece == WR_Space_Occupied:
              #rooks can only move up/down and left/right, so i2 must equal i, OR j2 must equal j for me to even consider it
              if (i2 == i) | (j2 == j):
                rook_at = WR_Space_Occupied[i2][j2]
                rook_can_take_i_j = rook_move(i2,j2,i,j)
                f |= (rook_at & rook_can_take_i_j)
            if piece == WB_Space_Occupied:
              # diagonals means that i-j == i2-j2, or i+j == i2+j2
              if (i-j == i2-j2) | (i+j == i2+j2):
                bishop_at = WB_Space_Occupied[i2][j2]
                bishop_can_take_i_j = bishop_move(i2,j2,i,j)
                f |= (bishop_at & bishop_can_take_i_j)
            if piece == WH_Space_Occupied:
              #A knight will never move more than 2 away in a single axis.
              if (abs(i2-i) <= 2) & (abs(j2-j) <= 2):
                knight_at = WH_Space_Occupied[i2][j2]
                knight_can_take_i_j = knight_move(i2,j2,i,j)
                f |= (knight_at & knight_can_take_i_j)

      #if (a piece at some location can capture a piece at (i,j)) then White_Potential_Moves[i][j] is true
      constraints.append(iff(importantSpot, f))
  return constraints

#set spaces_occupied for a space as true if there is a piece on it
def spaceOccupied():
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      # if Space_Occupied[i][j] is true, that means that at at least of of the _Space_Occupied[i][j]'s must be true.
      # if Space_Occupied[i][j] is false, then all of the _Space_Occupied[i][j]'s must be false
      # Handling to maake sure only 1 of the _Space_Occupied[i][j]'s is true is done below
      right = Space_Occupied[i][j]
      #need to expand this as new pieces are added
      left = (WP_Space_Occupied[i][j] | WQ_Space_Occupied[i][j] | BK_Space_Occupied[i][j] | WR_Space_Occupied[i][j] | WB_Space_Occupied[i][j] | WH_Space_Occupied[i][j] )
      constraints.append(iff(right, left))

      #add more constraints for occupying spaces as more white pieces are added.

      # Also here we will make sure there is only 1 piece per square (IE can't have a rook and bishop on the same square).
      # (BK_Space_Occupied[i][j] -> ~WQ_Space_Occupied[i][j]) as well as (WQ_Space_Occupied[i][j] -> ~BK_Space_Occupied[i][j])
      constraints.append( (~BK_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )
      constraints.append( (~WQ_Space_Occupied[i][j] | (~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )
      constraints.append( (~WP_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )
      constraints.append( (~WR_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )
      constraints.append( (~WB_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )
      constraints.append( (~WH_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] ) ) )
      #add more constraints for pieces on pieces as pieces are added.
  return constraints

# logic I am implementing right now will limit it to 2 or fewer queens. In the future, expand this
# to allow for x or fewer queens

# If exact is true, then must have exactly "allowedNum" number of pieces on the board. If exact is false,
# can have up to and including "allowedNum" number of pieces on the board.
def limitNumberPieces(Piece_Space_Occupied, Piece_Count, Piece_Total_Count, allowedNum, exact = False):
  if (allowedNum > BOARD_SIZE**2) & exact:
    raise ValueError("Can't have more pieces than you have sqaures on the board")
  # The code below was very heavily inspired (read: I rewrote it using our variable names) from the code provided by Prof. Muise.

  constraints = []
  # for whatever count is true when it gets to the end of the board, the corresponding Total_Count should relate to that.
  for i in range(BOARD_SIZE**2+1):
    constraints.append(iff(Piece_Total_Count[i], Piece_Count[(BOARD_SIZE**2)-1][i]))

  # restricting any time that it won't claim there are more pieces than spaces that have been checked
  for i in range(BOARD_SIZE**2):
    for j in range(i+2, (BOARD_SIZE**2)+1):
      constraints.append(~Piece_Count[i][j])

  # the first board value will be true of there is a white queen there, false if there isn't
  constraints.append(iff(Piece_Count[0][0], ~Piece_Space_Occupied[0][0]))
  constraints.append(iff(Piece_Count[0][1], Piece_Space_Occupied[0][0]))

  for i in range(1, BOARD_SIZE**2):
    # i1 and i2 used because shape for the space occupied variable is always a 2d array, while Piece_Count is a 1d array
    i1 = i//BOARD_SIZE
    i2 = i%BOARD_SIZE
    left = Piece_Count[i][0]
    right = Piece_Count[i-1][0] & ~Piece_Space_Occupied[i1][i2]
    constraints.append(iff(left, right))
    for j in range(1, i+2):
      # don't need to create j1 and j2 like with i, because j is never used as an index for the space_occupied variable.
      increase = Piece_Count[i-1][j-1] & Piece_Space_Occupied[i1][i2]
      constant = Piece_Count[i-1][j] & ~Piece_Space_Occupied[i1][i2]
      constraints.append(iff(Piece_Count[i][j], increase | constant))

  # Additional part to use the "allowedNum" and "extra" to make sure there are the right number of pieces
  if exact:
    constraints.append(Piece_Total_Count[allowedNum])
  else:
    allowedPieces = true.negate()
    for i in range(min(allowedNum, BOARD_SIZE**2)):
      allowedPieces |= Piece_Total_Count[i]
    constraints.append(allowedPieces)
  return constraints

def BK_Potential_Moves():
  constraints = []
  allCombined = [true.negate() for i in range(8)]
  
  #The following I believe is slightly unoptimized, but in the grand scheme of things, good enough (if I'm right it's only 512 unneeded constraints, which isn't much)
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      # if a black king is at position (i, j) and there is a white piece able to move to (i-1,j), then the king can't move up

      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j]).negate() | ~BK_Moves[1])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j]).negate() | ~BK_Moves[6])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i][j-1]).negate() | ~BK_Moves[3])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i][j+1]).negate() | ~BK_Moves[4])

      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j-1]).negate() | ~BK_Moves[0])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j+1]).negate() | ~BK_Moves[2])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j-1]).negate() | ~BK_Moves[5])
      constraints.append( (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j+1]).negate() | ~BK_Moves[7])

      allCombined[1] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j])
      allCombined[6] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j])
      allCombined[3] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i][j-1])
      allCombined[4] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i][j+1])

      allCombined[0] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j-1])
      allCombined[2] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i-1][j+1])
      allCombined[5] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j-1])
      allCombined[7] |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i+1][j+1])
  for i in range(8):
    #if all of the combined things are false, then BK_Moves for that one MUST be true
    right = allCombined[i].negate()
    left = BK_Moves[i]
    constraints.append(right.negate() | left) 

  # if all of BK_Moves[i] are false, then BK_No_Moves is true and vise versa (iff)
  availableMoves = true.negate()
  for i in range(8): # can be constant of 8 because the BK can only move 8 ways regardless of board size
    availableMoves |= BK_Moves[i]

  constraints.append(iff(availableMoves, ~BK_No_Moves))

  return constraints

# little function to add multiple constraints from a list
def addConstraints(encoding, constraints):
  for constraint in constraints:
    encoding.add_constraint(constraint)
  return encoding

#main compile for the theory
def Theory():
  E = Encoding()

  E = addConstraints(E, BK_Potential_Moves())

  E = addConstraints(E, spaceOccupied())

  E = addConstraints(E, outerBound())

  E = addConstraints(E, White_Potential_Movement([WQ_Space_Occupied,WP_Space_Occupied, WR_Space_Occupied, WB_Space_Occupied, WH_Space_Occupied]))

  E = addConstraints(E, limitNumberPieces(BK_Space_Occupied, BK_Count, BK_Total_Count, 1, True))

  E = addConstraints(E, limitNumberPieces(WQ_Space_Occupied, WQ_Count, WQ_Total_Count, 0, True)) #For Queen, 1 is min for stalemate, 2 is min for checkmate, and 43 is max for neither

  E = addConstraints(E, limitNumberPieces(WP_Space_Occupied, WP_Count, WP_Total_Count, 0, True)) #For Pawn 3 is min for stalemate, 4 is min for checkmate, and 63 is max for neither

  E = addConstraints(E, limitNumberPieces(WR_Space_Occupied, WR_Count, WR_Total_Count, 0, True)) #For Rook 2 is min for stalemate, 2 is min for checkmate, and 50 is max for neither

  E = addConstraints(E, limitNumberPieces(WB_Space_Occupied, WB_Count, WB_Total_Count, 0, True)) #For Bishop 3 is min for stalemate, 3 is min for checkmate, and 57 is max for neither

  E = addConstraints(E, limitNumberPieces(WH_Space_Occupied, WH_Count, WH_Total_Count, 61, True)) #For Knight 2 is min for stalemate, 3 is min for checkmate, and  is max for neither

  # Can't be in both checkmate and stalemate
  E.add_constraint(~Checkmate | ~Stalemate)
  
  #E.add_constraint(iff(Checkmate, ~Stalemate))

  #comment these out as needed to force the game to be stalemate, checkmate, or neither
  #E.add_constraint(Stalemate)
  #E.add_constraint(Checkmate)
  E.add_constraint(~Checkmate & ~Stalemate)

  # iff BK_No_Moves (ie the king has no valid moves), the game is either in checkmate or stalemate. pretty obvious
  # this will change if we add other pieces to the black side that are able to move, where we will also have to check
  # if the other peices are unable to move
  E.add_constraint(iff(BK_No_Moves, Checkmate | Stalemate))

  # if the king is in check, and doesn't have moves, then it is in checkmate. This will narrow the models down from the
  # previous constraint, which only simplified it to either checkmate or stalemate. now we know which one.
  # might be a more efficient way to do this, but this makes more sense in my head, so it's the way I'm doing it.
  E.add_constraint(iff(Check & BK_No_Moves, Checkmate))

  #Seeing if the king is in check
  allPotential = true.negate()
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      allPotential |= (BK_Space_Occupied[i][j] & White_Potential_Moves[i][j])
  #if allPotential is FALSE, that means that the king certainly is not in check
  #if allPotential is TRUE, that means the king is in check
  E.add_constraint(iff(allPotential, Check))

  return E

if __name__ == "__main__":
    T = Theory()
    # If we want to add an initial board setting you need:
    #T.add_constraint(parse_board(example_board))

    solution = T.solve()
    #print(solution)
    print(draw_board(parse_solution(solution)))

    # print("\nSatisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % T.count_solutions())
    # print("   Solution: %s" % T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     print(" %s: %.2f" % (vn, T.likelihood(v)))
    # print()
