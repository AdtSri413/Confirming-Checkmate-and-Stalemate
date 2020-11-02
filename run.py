from nnf import Var, true
from lib204 import Encoding

BOARD_SIZE = 8

#Black king stuff
BK_Space_Occupied = []
BK_Potential_Moves = []

#White queen stuff
WQ_Space_Occupied = []
WQ_Potential_Moves = []


# Creatting the massive arrays of initialized variables needed for the movements/positions of peices.

# IDEA: instead of stuff like WQ_Potential_Moves, maybe just make one set of variables called "White_Potential_Moves". Because it
# Really doesn't matter which piece can move where, just that a specific square is 'in danger' by some piece.
for i in range(BOARD_SIZE):
    BK_Space_Occupied.append([])
    WQ_Space_Occupied.append([])

    BK_Potential_Moves.append([])
    WQ_Potential_Moves.append([])

    for j in range(BOARD_SIZE):
        BK_Space_Occupied[i].append(Var(f'BK_Occupied_{i},{j}'))
        WQ_Space_Occupied[i].append(Var(f'WQ_Occupied_{i},{j}'))

        BK_Potential_Moves[i].append(Var(f'BK_Potential_Moves_{i},{j}'))
        WQ_Potential_Moves[i].append(Var(f'WQ_Potential_Moves_{i},{j}'))


# not done with a loop so we can have the handy comments saying what direction each one is for
BK_Move_1 = Var('BK_Move_1') # down-left
BK_Move_2 = Var('BK_Move_2') # down
BK_Move_3 = Var('BK_Move_3') # down-right
BK_Move_4 = Var('BK_Move_4') # left
BK_Move_6 = Var('BK_Move_6') # right
BK_Move_7 = Var('BK_Move_7') # up-left
BK_Move_8 = Var('BK_Move_8') # up
BK_Move_9 = Var('BK_Move_9') # up-right
BK_No_Moves = Var('Bk_No_Moves') # true if the black king has no moves (IE everything above is false)

# 
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
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,"WQ"]]

# function for setting the initial board configuration. ALL it will do is set
# The positions of pieces. This may be a question to ask for feedback, if we can set
# where the king (or other pieces) can move here, but I *think* that would go against
# the idea of using logic, not python programming, to solve it

# Maybe based on the location of the king setting the movement ones to false only in the situation it would be moving
# off the board. The other ones leave to figure out later. Still, maybe the TA's want us to do that with constraints(?)
def set_initial_config(board):
  #board parser starts here
  f = true
  for i in range(BOARD_SIZE):
      for j in range(BOARD_SIZE):
          if board[i][j]=="BK":
              f &= BK_Space_Occupied[i][j]
              
          elif board[i][j]=="WQ":
              f &= WQ_Space_Occupied[i][j]

  return f


# little thing that takes an if and only if statement, and returns it in negation normal form.
# Thanks to the professor for this snippet
def iif(left, right):
    return (left.negate() | right) & (right.negate() | left)


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


# little function to add multiple constraints from a list
def addConstraints(encoding, constraints):
  for constraint in constraints:
    encoding.add_constraint(constraint)
  return encoding

#main compile for the theory
def Theory():
  E = Encoding()

  # Reminder: the line below is temp commented, to reduce output when printing
  E = addConstraints(E, singleKing())

  # Can't be in both checkmate and stalemate
  E.add_constraint(iif(Checkmate, ~Stalemate))

  # iif BK_No_Moves (ie the king has no valid moves), the game is either in checkmate or stalemate. pretty obvious
  # this will change if we add other pieces to the black side that are able to move, where we will also have to check
  # if the other peices are unable to move
  E.add_constraint(iif(BK_No_Moves, Checkmate | Stalemate))

  # if the king is in check, and doesn't have moves, then it is in checkmate. This will narrow the models down from the
  # previous constraint, which only simplified it to either checkmate or stalemate. now we know which one.
  # might be a more efficient way to do this, but this makes more sense in my head, so it's the way I'm doing it.
  E.add_constraint(iif(Check & BK_No_Moves, Checkmate))

  return E




if __name__ == "__main__":
    T = Theory()

    #If we want to add an initial board setting you need:
    # T.add_constraint(set_inital_config(board))

    solution = T.solve()
    print(solution)

    # print("\nSatisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % T.count_solutions())
    # print("   Solution: %s" % T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     print(" %s: %.2f" % (vn, T.likelihood(v)))
    # print()
