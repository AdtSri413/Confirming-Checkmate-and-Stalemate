from nnf import Var
from lib204 import Encoding

# Call your variables whatever you want
# BK_Current_Pos = Var('BK_Current_Pos')


BK_Space_Occupied = []
WQ_Space_Occupied = []

BK_Potential_Moves = []
WQ_Potential_Moves = []

for i in range(8):
    BK_Space_Occupied.append([])
    WQ_Space_Occupied.append([])

    BK_Potential_Moves.append([])
    WQ_Potential_Moves.append([])

    for j in range(8):
        BK_Space_Occupied[i].append(False)
        WQ_Space_Occupied[i].append(False)

        BK_Potential_Moves[i].append(False)
        WQ_Potential_Moves[i].append(False)



BK_Move_1 = Var('BK_Move_1') # down-left
BK_Move_2 = Var('BK_Move_2') # down
BK_Move_3 = Var('BK_Move_3') # down-right
BK_Move_4 = Var('BK_Move_4') # left
BK_Move_6 = Var('BK_Move_6') # right
BK_Move_7 = Var('BK_Move_7') # up-left
BK_Move_8 = Var('BK_Move_8') # up
BK_Move_9 = Var('BK_Move_9') # up-right

Check = Var('Check')

#example board config
example_board = [["BK",0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,"WQ"]]


#board parser starts here
for i in range(8):
    for j in range(8):
        if example_board[i][j]=="BK":
            BK_Space_Occupied[i][j] = True
            if j<7:
                BK_Potential_Moves[i][j+1] = True
            if j>0: 
                BK_Potential_Moves[i][j-1] = True
            if i<7:
                BK_Potential_Moves[i-1][j] = True
            if i>0:
                BK_Potential_Moves[i+1][j] = True #don't fucking judge me -Josh
            if (j<7 & i<7):
                BK_Potential_Moves[i-1][j+1] = True
            if (j>0 & i<7):
                BK_Potential_Moves[i+1][j+1] = True
            if (j<7 & i>0):
                BK_Potential_Moves[i-1][j-1] = True
            if (j>0 & i>0):
                BK_Potential_Moves[i+1][j-1] = True
            
        elif example_board[i][j]=="WQ":
            WQ_Space_Occupied[i][j] = True




#def set_board_config():

def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def Checkmate_Theory():
    E = Encoding()
    E.add_constraint(~BK_Move_1 & ~BK_Move_2 & ~BK_Move_3 & ~BK_Move_4 & ~BK_Move_6 & ~BK_Move_7 & ~BK_Move_8 & ~BK_Move_9 & Check)
    return E

def Stalemate_Theory():
    E = Encoding()
    E.add_constraint(~BK_Move_1 & ~BK_Move_2 & ~BK_Move_3 & ~BK_Move_4 & ~BK_Move_6 & ~BK_Move_7 & ~BK_Move_8 & ~BK_Move_9 & ~Check)


    return E


if __name__ == "__main__":

    T = Checkmate_Theory()

    solution = T.solve()
    print(solution)
    # print("\nSatisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % T.count_solutions())
    # print("   Solution: %s" % T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     print(" %s: %.2f" % (vn, T.likelihood(v)))
    # print()
# BK_Space_Occupied[0][0] = True
# print(BK_Space_Occupied[0][0])

# for i in range(8):
#     for j in range(8):
#         if (BK_Space_Occupied[i][j] == True):
#             # print(
