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

#White knight (called "WH" for white horse because the white king is WK) stuff
WH_Space_Occupied = []
WH_Count, WH_Total_Count = count_builder("WH")

#White King stuff
WK_Space_Occupied = []
WK_Count, WK_Total_Count = count_builder("WK")

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
    WK_Space_Occupied.append([])
    Space_Occupied.append([])
    White_Potential_Moves.append([])
    for j in range(BOARD_SIZE):
        BK_Space_Occupied[i].append(Var(f'BK_Occupied_{i},{j}'))
        WQ_Space_Occupied[i].append(Var(f'WQ_Occupied_{i},{j}'))
        WP_Space_Occupied[i].append(Var(f'WP_Occupied_{i},{j}'))
        WR_Space_Occupied[i].append(Var(f'WR_Occupied_{i},{j}'))
        WB_Space_Occupied[i].append(Var(f'WB_Occupied_{i},{j}'))
        WH_Space_Occupied[i].append(Var(f'WH_Occupied_{i},{j}'))
        WK_Space_Occupied[i].append(Var(f'WK_Occupied_{i},{j}'))
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

# function for setting the initial board configuration. ALL it will do is set
# The positions of pieces.
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
      elif board[i][j]=="WK":
        f &= WK_Space_Occupied[i][j]

      else:
        f &= ~Space_Occupied[i][j]
  return f

#parse the output from the model into a board array

def parse_solution(solution):
  board = [
    [0 for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)
  ]
  check = False
  checkmate = False
  stalemate = False
  if solution == None:
    print("No solution")
    return board, check, checkmate, stalemate
  #replace the 0's with pieces as needed
  for key, value in solution.items():
    if (key == "Check"):
      check = True
    if (key == "Checkmate") & value:
      checkmate = True
    if (key == "Stalemate") & value:
      stalemate = True
    if (key[:-3] == 'BK_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "BK"
      print(int(key[-3]),int(key[-1]))
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
    if (key[:-3] == 'WK_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WK"

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
  return board, check, checkmate, stalemate

# We want our board to be pretty, so this will make it pretty.
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

# To easily determine/stop the black king from being able to leave the board, adding an additional "invisible" row and column to
# where the white pieces are able to move. Doesn't affect anything, except for the moment the black king tries to leave the bounds
# of the board, in which instance it will encounter this layer and because it says white can move there, the black king won't.
def outerBound():
  constraints = []
  for i in range(BOARD_SIZE+1):
    for j in range(BOARD_SIZE+1):
      if (i == BOARD_SIZE) | (j == BOARD_SIZE):
        constraints.append(White_Potential_Moves[i][j])
  return constraints

# Determines if a rook can move from point (i,j) to point (goal_i,goal_j), where it is unable to if there is a piece (other than the black king)
# in it's way. The reason we DONT take into account if a black king is in the way is because the black king can move, so if it moves to a different square,
# all of a sudden the piece is able to continue on it's path. The black king's location just doesn't matter to block it's movement
def rook_move(i, j, goal_i, goal_j):
  f = true.negate()
  k = i
  # moving to the top of the board
  while (k > 0) & (j == goal_j):
    k-=1
    if (k == goal_i) & (j == goal_j):
      f = true
      for between in range(i-1,goal_i,-1):
        f &= (~Space_Occupied[between][j] | BK_Space_Occupied[between][j])
      return f
  k = i
  # moving to the bottom of the board
  while (k < (BOARD_SIZE-1)) & (j == goal_j):
    k+=1
    if (k == goal_i) & (j == goal_j):
      f = true
      for between in range(i+1,goal_i):
        f &= (~Space_Occupied[between][j] | BK_Space_Occupied[between][j])
      return f
  k = j
  # moving to the left across the board
  while (k > 0) & (i == goal_i):
    k-=1
    if (i == goal_i) & (k == goal_j):
      f = true
      for between in range(j-1,goal_j,-1):
        f &= (~Space_Occupied[i][between] | BK_Space_Occupied[i][between])
      return f
  k = j
  #moving right across the board
  while (k < (BOARD_SIZE-1)) & (i == goal_i):
    k+=1
    if (i == goal_i) & (k == goal_j):
      f = true
      for between in range(j+1,goal_j):
        f &= (~Space_Occupied[i][between] | BK_Space_Occupied[i][between])
      return f
  return f

# Exact same thing as the rook movement, except in diagonals instead of straight lines
def bishop_move(i, j, goal_i, goal_j):
  f = true.negate()
  k = i
  l = j
  # moving up and left
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
  # moving up and right
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
  # moving down and left
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
  # moving down and right
  while (k < BOARD_SIZE-1) & (l < BOARD_SIZE-1):
    k+=1
    l+=1
    if (k == goal_i) & (l == goal_j):
      f = true
      for between in range(1,i-k):
        f &= (~Space_Occupied[i+between][j+between] | BK_Space_Occupied[i+between][j+between])
      return f
  return f

# a queen can just move to any location either a rook or a bishop can move to - ie any direction in a straight line
def queen_move(i,j, i_goal, j_goal):
  horizontal_takes = rook_move(i,j, i_goal, j_goal)
  vertical_takes = bishop_move(i,j, i_goal, j_goal)
  return horizontal_takes | vertical_takes

# same as all the previous, except a little special because a knight has a special "L" shaped moving pattern
# also, because a knight can jump over pieces, we don't need to worry about anything blocking it. So we don't need any of the fancy
# "&" logic from before because it's just: reach a spot
def knight_move(i, j, goal_i, goal_j):
  f = true.negate()
  #up 2
  if ((i-2) == goal_i):
      if ((j-1) == goal_j):
          f = true
      if ((j+1) == goal_j):
          f = true
  #down 2
  if ((i+2) == goal_i):
      if ((j-1) == goal_j):
          f = true
      if ((j+1) == goal_j):
          f = true
  #left 2
  if ((j-2) == goal_j):
      if ((i-1) == goal_i):
          f = true
      if ((i+1) == goal_i):
          f = true
  #right 2
  if ((j+2) == goal_j):
      if ((i-1) == goal_i):
          f = true
      if ((i+1) == goal_i):
          f = true
  return f

#For every possible locaation on a board, we take that location as a "special" spot, and see if there is some piece elsewhere that is
# Capable of moving to this location on the board.
def White_Potential_Movement(availablePieces):
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      #iterate our "special" item to be all of the board locations
      importantSpot = White_Potential_Moves[i][j]
      f = true.negate()
      for i2 in range(BOARD_SIZE):
        for j2 in range(BOARD_SIZE):
          #for every square on the board, see if there is some  piece on that square that is capable of moving to our "special" square
          for piece in availablePieces:
            if piece == WQ_Space_Occupied:
              # Queen can't take the spot it is itself on, but other than that... ehhhh maybe
              if (i2 != i) | (j2 != j):
                queen_spot = WQ_Space_Occupied[i2][j2]
                queen_can_take_i_j = queen_move(i2,j2, i ,j)
                f |= (queen_spot & queen_can_take_i_j)

            if piece == WP_Space_Occupied:
              # In the case of a pawn, the pawn must have an row value 1 smaller than the importantSpot, and a column value either 1 greater or 1 smaller than the importantSpot
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

            if piece == WK_Space_Occupied:
              #A king can take any adjacent square, but not the square where i=i2 and j=j2 (ie its own square)
              if (abs(i2-i) <= 1) & (abs(j2-j) <= 1) & ((i != i2) | (j != j2)):
                king_at = WK_Space_Occupied[i2][j2]
                f |= king_at

      #if (a piece at some location can capture a piece at (i,j)) then White_Potential_Moves[i][j] is true
      constraints.append(iff(importantSpot, f))
  return constraints

# This function has 2 purposes:
# 1. To condense if there is a piece on a particular space into a single variable, which is used to know if there is a piece
#    blocking the movement of another for White_Potential_Moves, as well as when passing in a pre-built board.
# 2. Make sure that there is only 1 piece on a specific square.
def spaceOccupied():
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      # if Space_Occupied[i][j] is true, that means that at at least of of the _Space_Occupied[i][j]'s must be true.
      # if Space_Occupied[i][j] is false, then all of the _Space_Occupied[i][j]'s must be false
      # Handling to maake sure only 1 of the _Space_Occupied[i][j]'s is true is done below
      right = Space_Occupied[i][j]
      #need to expand this as new pieces are added
      left = (WP_Space_Occupied[i][j] | WQ_Space_Occupied[i][j] | BK_Space_Occupied[i][j] | WR_Space_Occupied[i][j] | WB_Space_Occupied[i][j] | WH_Space_Occupied[i][j] | WK_Space_Occupied[i][j])
      constraints.append(iff(right, left))

      #add more constraints for occupying spaces as more white pieces are added.

      # Also here we will make sure there is only 1 piece per square (IE can't have a rook and bishop on the same square).
      # (BK_Space_Occupied[i][j] -> ~WQ_Space_Occupied[i][j]) as well as (WQ_Space_Occupied[i][j] -> ~BK_Space_Occupied[i][j])
      constraints.append( (~BK_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WQ_Space_Occupied[i][j] | (~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WP_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WR_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WB_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WH_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WK_Space_Occupied[i][j] ) ) )
      constraints.append( (~WK_Space_Occupied[i][j] | (~WQ_Space_Occupied[i][j] & ~BK_Space_Occupied[i][j] & ~WP_Space_Occupied[i][j] & ~WR_Space_Occupied[i][j] & ~WB_Space_Occupied[i][j] & ~WH_Space_Occupied[i][j] ) ) )

      #add more constraints for pieces on pieces as pieces are added.
  return constraints

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

#In chess, it's impossible to get into a situation where two kings (of opposite color, not that your really able to get 2 of the same color)
# are directly adjacent to each other.
def Kings_Adjacent():
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      BK_spot = BK_Space_Occupied[i][j]
      adjacentKings = true.negate()
      #all of these if statements are needed so I don't get an out-of-bounds exception
      if i>0:
        adjacentKings |= WK_Space_Occupied[i-1][j]
      if j>0:
        adjacentKings |= WK_Space_Occupied[i][j-1]
      if i < BOARD_SIZE-1:
        adjacentKings |= WK_Space_Occupied[i+1][j]
      if j < BOARD_SIZE-1:
        adjacentKings |= WK_Space_Occupied[i][j+1]

      if (i>0) & (j>0):
        adjacentKings |= WK_Space_Occupied[i-1][j-1]
      if (i>0) & (j < BOARD_SIZE-1):
        adjacentKings |= WK_Space_Occupied[i-1][j+1]
      if (i < BOARD_SIZE-1) & (j>0):
        adjacentKings |= WK_Space_Occupied[i+1][j-1]
      if (i < BOARD_SIZE-1) & (j < BOARD_SIZE-1):
        adjacentKings |= WK_Space_Occupied[i+1][j+1]
      constraints.append(~BK_spot | adjacentKings.negate())
  return constraints

#Function to figure out where the black king is capable of moving to
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

  E = addConstraints(E, White_Potential_Movement([WQ_Space_Occupied,WP_Space_Occupied, WR_Space_Occupied, WB_Space_Occupied, WH_Space_Occupied, WK_Space_Occupied]))

  E = addConstraints(E, Kings_Adjacent())

  E = addConstraints(E, limitNumberPieces(BK_Space_Occupied, BK_Count, BK_Total_Count, 1, True))

  #There must be at least one black king, so that is always limited. The lines below will restrict each piece so some
  #Amount. They are useful for exploring the board in a very controlled way, so uncomment them and change them if you have an idea
  # of what you are doing.

  # E = addConstraints(E, limitNumberPieces(WQ_Space_Occupied, WQ_Count, WQ_Total_Count, 4, True)) #For Queen, 1 is min for stalemate, 2 is min for checkmate, and 43 is max for neither

  # E = addConstraints(E, limitNumberPieces(WP_Space_Occupied, WP_Count, WP_Total_Count, 6, True)) #For Pawn 3 is min for stalemate, 4 is min for checkmate, and 63 is max for neither

  # E = addConstraints(E, limitNumberPieces(WR_Space_Occupied, WR_Count, WR_Total_Count, 2, True)) #For Rook 2 is min for stalemate, 2 is min for checkmate, and 50 is max for neither

  # E = addConstraints(E, limitNumberPieces(WB_Space_Occupied, WB_Count, WB_Total_Count, 2, True)) #For Bishop 3 is min for stalemate, 3 is min for checkmate, and 57 is max for neither

  # E = addConstraints(E, limitNumberPieces(WH_Space_Occupied, WH_Count, WH_Total_Count, 3, True)) #For Knight 2 is min for stalemate, 3 is min for checkmate, and 61 is max for neither

  # E = addConstraints(E, limitNumberPieces(WK_Space_Occupied, WK_Count, WK_Total_Count, 1, True)) #For King 2 is min for stalemate, NaN is min for checkmate, and 58 is max for neither

  # Can't be in both checkmate and stalemate
  E.add_constraint(~Checkmate | ~Stalemate)

  #E.add_constraint(iff(Checkmate, ~Stalemate))

  #comment these out as needed to force the game to be stalemate, checkmate, or neither
  #E.add_constraint(Stalemate)
  #E.add_constraint(Checkmate)
  #E.add_constraint(~Checkmate & ~Stalemate)

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


# The following 3 functions all explore the model in a different way

#This function takes in:
# mate_constraint, which should be either Checkmate, Stalemate, or (~Checkmate & ~Stalemate), as well as the piece you want to check
# (with pieceInfo need to supply: [piece_space_occupied, piece_count, piece_total_count])
# The output, if given the Checkmate or Stalemate for the constraint, is the minimum number of that particular piece needed in order to produce
# that result.
# If given (~Checkmate & ~Stalemate), it will find the maximum number of the piece that satisifies this (ie the max of a piece there can be with the black king still
# being able to move)
def explore_single_piece(mate_constraint, pieceInfo):
  solution = None
  number = 0
  allPieces = [[WQ_Space_Occupied,WP_Space_Occupied, WR_Space_Occupied, WB_Space_Occupied, WH_Space_Occupied, WK_Space_Occupied],
               [WQ_Count, WP_Count, WR_Count, WB_Count, WH_Count, WK_Count],
               [WQ_Total_Count, WP_Total_Count, WR_Total_Count, WB_Total_Count, WH_Total_Count, WK_Total_Count]]

  if mate_constraint in [Checkmate, Stalemate]:
    while (not solution) & (number < 64):
      number += 1
      T = Theory()
      T = addConstraints(T, limitNumberPieces(pieceInfo[0], pieceInfo[1], pieceInfo[2], number, True))

      for i in range(6):
        if allPieces[0][i] != pieceInfo[0]:
          T = addConstraints(T, limitNumberPieces(allPieces[0][i], allPieces[1][i], allPieces[2][i], 0, True))
        
      solution = T.solve()

  if mate_constraint == (~Checkmate & ~Stalemate):
    number = 63
    solution =  "something other than none by default"
    while (solution != None) & (number > 0):
      number -= 1
      T = Theory()
      T = addConstraints(T, limitNumberPieces(pieceInfo[0], pieceInfo[1], pieceInfo[2], number, True))

      for i in range(6):
        if allPieces[0][i] != pieceInfo[0]:
          T = addConstraints(T, limitNumberPieces(allPieces[0][i], allPieces[1][i], allPieces[2][i], 0, True))

      solution = T.solve()

  return number

# This function will take in a 2d array with the same number of rows and columns as BOARD_SIZE. Given this board, it will create
# the constraint necessary to force that board to be satisifed in the constraints. It will then tell you if the board is in either
# stalemate or checkmate
'''
Template for an 8x8 board that can be copy/pasted and filled in with whatever you want, to be used for this function
example_board = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]]
'''
def explore_supplied_board(board):
  T = Theory()
  constraint = parse_board(board)
  T.add_constraint(constraint)

  solution = T.solve()
  result = parse_solution(solution)
  if result[1]:
    print("This board has the king in check")
  if result[2]:
    print("Furthermore, the king is also in checkmate!")
  if result[3]:
    print("This board has the king in stalemate!")


  


if __name__ == "__main__":
    # If you don't want to do any of the board exploration shenanigans, and instead just generate a random board, uncomment the 4
    # lines below (the 3rd one will print about 30k variables, so maybe leave that commented, and the 4th one will print out a nicely
    # parsed board, so definitly uncomment that one)
    # T = Theory()
    # solution = T.solve()
    # print(solution)
    # print(draw_board(parse_solution(solution)[0]))

    # Exploring the model to find the maximum and minimum required
    # (print statement not included in example, do it yourself)
    # amount = explore_single_piece(Checkmate, [WQ_Space_Occupied, WQ_Count, WQ_Total_Count])

    # Exploring the model by creating a board and seeing if the board is in check, checkmate, or stalemate
    # I have provided an example here that has the king in checkmate. There is also an empty board supplied at
    # the start of the explore_supplied_board function the can be filled in as someone pleases
    # board = [
    # ["BK",0,"WP",0,0,0,0,0],
    # [0,"WQ",0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0]]
    # explore_supplied_board(board)