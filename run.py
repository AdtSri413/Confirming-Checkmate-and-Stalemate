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

#White queen stuff
WQ_Space_Occupied = []
WQ_Count, WQ_Total_Count = count_builder("WQ")

#White pawn stuff
WP_Space_Occupied = []

#White Potential Moves
White_Potential_Moves = []

# Creatting the massive arrays of initialized variables needed for the movements/positions of peices.

# IDEA: instead of stuff like WQ_Potential_Moves, maybe just make one set of variables called "White_Potential_Moves". Because it
# Really doesn't matter which piece can move where, just that a specific square is 'in danger' by some piece.
for i in range(BOARD_SIZE):
    BK_Space_Occupied.append([])
    WQ_Space_Occupied.append([])
    WP_Space_Occupied.append([])
    Space_Occupied.append([])
    White_Potential_Moves.append([])
    for j in range(BOARD_SIZE):
        BK_Space_Occupied[i].append(Var(f'BK_Occupied_{i},{j}'))
        WQ_Space_Occupied[i].append(Var(f'WQ_Occupied_{i},{j}'))
        WP_Space_Occupied[i].append(Var(f'WP_Occupied_{i},{j}'))
        Space_Occupied[i].append(Var(f'Space_Occupied_{i},{j}'))
        White_Potential_Moves[i].append(Var(f'White_Potential_Moves{i},{j}'))

# not done with a loop so we can have the handy comments saying what direction each one is for
BK_Moves = []
for i in range(1,10):
  if (i != 5) & (i != 0):
    BK_Moves.append(Var(f'BK_Move_{i}'))
# BK_Move_1 = Var('BK_Move_1') # up-left
# BK_Move_2 = Var('BK_Move_2') # up
# BK_Move_3 = Var('BK_Move_3') # up-right
# BK_Move_4 = Var('BK_Move_4') # left
# BK_Move_6 = Var('BK_Move_6') # right
# BK_Move_7 = Var('BK_Move_7') # down-left
# BK_Move_8 = Var('BK_Move_8') # down
# BK_Move_9 = Var('BK_Move_9') # down-right
BK_No_Moves = Var('Bk_No_Moves') # true if the black king has no moves (IE everything above is false)

Check = Var('Check')

# the 2 ending configuations. Mutually exclusive, and 1 must be true for the model to exist.
Stalemate = Var('Stalemate')
Checkmate = Var('Checkmate')

# example board config
example_board = [["BK",0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,"WQ",0,0],
[0,0,0,0,0,0,"WQ",0],
[0,0,0,0,0,0,0,"WQ"]]

# example_board = [
#   [0,0],
#   [0,"WQ"]
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

      else:
        f &= ~Space_Occupied[i][j]
  return f


def rook_move(i, j):
     k = i
     while k >= 0:
         k-=1
         if not Space_Occupied[k][j]:
             break
         else:
             White_Potential_Moves[k][j] = true
     k = i
     while k <= BOARD_SIZE:
         k+=1
         if not Space_Occupied[k][j]:
             break
         else:
             White_Potential_Moves[k][j] = true
     k = j
     while k >= 0:
         k-=1
         if not Space_Occupied[i][k]:
             break
         else:
             White_Potential_Moves[i][k] = true
     k = j
     while k <= BOARD_SIZE:
         k+=1
         if not Space_Occupied[i][k]:
             break
         else:
             White_Potential_Moves[i][k] = true

def bishop_move(i, j):
    k = i
    l = j
    while k >= 0 & l >= 0:
        k-=1
        l-=1
        if not Space_Occupied[k][l]:
            break
        else:
            White_Potential_Moves[k][j] = true
    k = i
    l = j
    while k >= 0 & l <= BOARD_SIZE:
        k-=1
        l+=1
        if not Space_Occupied[i][k]:
            break
        else:
            White_Potential_Moves[i][k] = true
    k = i
    l = j
    while k <= BOARD_SIZE & l >= 0:
        k+=1
        l-=1
        if not Space_Occupied[i][k]:
            break
        else:
            White_Potential_Moves[i][k] = true
    k = i
    l = j
    while k <= BOARD_SIZE & l <= BOARD_SIZE:
        k+=1
        l+=1
        if not Space_Occupied[i][k]:
            break
        else:
            White_Potential_Moves[i][k] = true


              # for k in range(BOARD_SIZE): #i and j are the row and column the queen occupies
              #     for l in range(BOARD_SIZE):
              #         White_Potential_Moves[i][k] = true
              #         White_Potential_Moves[l][j] = true
              #         if (k-i == l-j | k-i == (0-(l-j)) ):
              #             White_Potential_Moves[k][l] = true

    return f

def White_Potential_Movement(row, column, piece):
  f = true
  if piece=="WQ":
     #adds threat squares to each row and column the queen occupies
              #loops break upon encountering a blocking piece, terminating the threat line
              #cardinal directions
              rook_move(i, j)
              bishop_move(i, j)

  if piece=="WP":
    # Implemented edge checking
    if i==0:
      f &= White_Potential_Moves[i+1][j-1]
    elif i==BOARD_SIZE-1:
      f &= White_Potential_Moves[i-1][j-1]
    elif j!=0:
      f &= White_Potential_Moves[i-1][j-1]
      f &= White_Potential_Moves[i+1][j-1]

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
  for key, value in solution.items():
    if (key[:-3] == 'BK_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "BK"
    if (key[:-3] == 'WQ_Occupied_') & value:
      board[int(key[-3])][int(key[-1])] = "WQ"
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

#set spaces_occupied for a space as true if there is a piece on it
def spaceOccupied():
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      #BK_Space_Occupied[i][j] -> Space_Occupied[i][j]
      constraints.append(~BK_Space_Occupied[i][j] | Space_Occupied[i][j])
      #WQ_Space_Occupied[i][j] -> Space_Occupied[i][j]
      constraints.append(~WQ_Space_Occupied[i][j] | Space_Occupied[i][j])
      constraints.append(~WP_Space_Occupied[i][j] | Space_Occupied[i][j])

      #add more constraints for occupying spaces as more white pieces are added.

      # Also here we will make sure there is only 1 piece per square.
      # (BK_Space_Occupied[i][j] -> ~WQ_Space_Occupied[i][j]) as well as (WQ_Space_Occupied[i][j] -> ~BK_Space_Occupied[i][j])
      constraints.append( (~BK_Space_Occupied[i][j] | ~WQ_Space_Occupied[i][j] | ~WP_Space_Occupied[i][j] ) )

      #add more constraiints for pieces on pieces as pieces are added.
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

# function for generating a list of constraints that is everything we need to determine if there are multiple kings
# theoretically without this a person could create a board configuration with multiple black kings on it, which is not
# exactly within the rule set of chess
def singleKing():
  constraints = []
  oneKing = true.negate()
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):

      #BK_Space_Occupied[i][j] -> all other BK_Space_Occupied values are FALSE (ie ~BK_Space_Occupied[x][y])
      allOtherSpaces = true
      for add1 in range(0,BOARD_SIZE):
        for add2 in range(0,BOARD_SIZE):
          # need to add the constraints for every square other than the (i,j) square
          if (not ( ((i + add1) % BOARD_SIZE == i) and ((j + add2) % BOARD_SIZE == j))):
            # We are creating a series of 'and's chained together. the chain will have the value for each
            # and every square other than the square
            allOtherSpaces &= ~BK_Space_Occupied[(i + add1) % BOARD_SIZE][(j + add2) % BOARD_SIZE]

      newConstraint =  ~BK_Space_Occupied[i][j] | (allOtherSpaces)
      constraints.append(newConstraint)

      #Slowely build up the last constraint needed, to make sure there is at least one black king
      oneKing |= BK_Space_Occupied[i][j]
  # add the constraint of eensuring there is at least one king
  constraints.append(oneKing)
  return constraints

def King_Edge_Potential_Moves():
  constraints = []
  for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
      if (i == 0):
        #if i=0, and a king occupies that space, then it cannot move up.
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[1])
      if (i == BOARD_SIZE):
        #if i= the size of the board, and a king occupies that space, then it cannot move down.
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[6])
      if (j == 0):
        # if j=0, then a king can't move left
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[3])
      if (j == BOARD_SIZE):
        # if j= the size of the board, then a king can't move right
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[4])
      if (j == 0) & (i == 0):
        # can't move up/left
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[0])
      if (j == 0) & (i == BOARD_SIZE):
        # can't move down/left
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[5])
      if (j == BOARD_SIZE) & (i == 0):
        # can't move up/right
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[2])
      if (j == BOARD_SIZE) & (i == BOARD_SIZE):
        # can't move down/right
        constraints.append(~BK_Space_Occupied[i][j] | ~BK_Moves[7])

  return constraints

# little function to add multiple constraints from a list
def addConstraints(encoding, constraints):
  for constraint in constraints:
    encoding.add_constraint(constraint)
  return encoding

#main compile for the theory
def Theory():
  E = Encoding()

  #E = addConstraints(E, singleKing())

  #E = addConstraints(E, King_Edge_Potential_Moves())

  #E = addConstraints(E, spaceOccupied())

  #E.add_constraint(White_Potential_Movement(i, j, board[i][j]))

  E = addConstraints(E, limitNumberPieces(WQ_Space_Occupied, WQ_Count, WQ_Total_Count, 36, True))


  # Can't be in both checkmate and stalemate
  #E.add_constraint(iff(Checkmate, ~Stalemate))

  # iff BK_No_Moves (ie the king has no valid moves), the game is either in checkmate or stalemate. pretty obvious
  # this will change if we add other pieces to the black side that are able to move, where we will also have to check
  # if the other peices are unable to move
  #E.add_constraint(iff(BK_No_Moves, Checkmate | Stalemate))

  # if the king is in check, and doesn't have moves, then it is in checkmate. This will narrow the models down from the
  # previous constraint, which only simplified it to either checkmate or stalemate. now we know which one.
  # might be a more efficient way to do this, but this makes more sense in my head, so it's the way I'm doing it.
  #E.add_constraint(iff(Check & BK_No_Moves, Checkmate))

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
