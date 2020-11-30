'''
After seeing the professors video for counting with the predicate logic, I decided to more-or-less
follow what he said. However, I was very proud of coming up with this way to count if there are up to 2
of a piece, so here it shall reside, in a place of honor
Side note: when running to check for 2 or less pieces (which is really all it can do but I had plans for more originally)
it would be able to confirm that there were 2 or less of a piece with exactly 492 constraints :)

While this may not be the most optimized code possible for such a task, it is FAR from the worst. As the professor talked about
in a video, the easy way to do it is to just compare every two values together to determine if those two are queens, and if they are
everything else must not be. Talking this approach, the number of constraints that would be necessary is 64 choose 2 (for a 8x8 board), 
which comes out to 2016. So my code has roughly 4x fewer constraints than a lesser-optimized version


The other reason I am leaving this here is to demonstrate our group did put in a concentrated effort to create our own counting formula, and
only after succeeding for 2 but failing to figure out how to translate this into counting for more than 2 pieces did we go with the professors code.
'''


def limitNumberPieces(Piece_RowOrColumn, Piece_Space_Occupied, allowedNum):
  if allowedNum < 1:
    raise ValueError("Must be allowing at least 1 piece. If ya don't want any allowed then just get rid of the call for this or some shit idk fuck off")
  constraints = []
  for rowOrColumn in range(2):

    for i in range(BOARD_SIZE):
      # Piece_RowOrColumn[i] is true if and only if (Piece_Space_Occupied[i][0] | Piece_Space_Occupied[i][1] | ..... | Piece_Space_Occupied[i][board_size] )
      left_side = Piece_RowOrColumn[rowOrColumn][i]
      right_side = true.negate()
      for j in range(BOARD_SIZE):
        right_side |= Piece_Space_Occupied[i if rowOrColumn == 0 else j][j if rowOrColumn == 0 else i]
      constraints.append(iff(left_side, right_side))

    # now I know if the Piece_RowOrColumn[i] is true. Next there are 2 main steps:
    # if a row it true, then for each element a) within the row, and b) outside the row, check every 2 elements in the row vs them
    # to see if they are true.
    for i in range(BOARD_SIZE):
      #negated because it's an implication
      selection = Piece_RowOrColumn[rowOrColumn][i]
      for j in range(BOARD_SIZE):
        #j is the index of the first P.O.I
        for k in range(BOARD_SIZE):
          #k is the index of the second P.O.I
          #Only need to check for areas where k>j. Because if k=j, then I am just looking at the same piece, and if
          # k < j, then I am looking back at pieces I have already added.
          if k > j:
            constraint_head = selection & Piece_Space_Occupied[i if rowOrColumn == 0 else j][j if rowOrColumn == 0 else i] & Piece_Space_Occupied[i if rowOrColumn == 0 else k][k if rowOrColumn == 0 else i]
            constraint_head = constraint_head.negate()
            constraint_body = true
            for compareVal in range(BOARD_SIZE):
              #add every other value for a row into the stuff that cannot be, except j and k, cus those are the 2 that are important.
              if compareVal not in [j,k]:

                constraint_body &= ~Piece_Space_Occupied[i if rowOrColumn == 0 else compareVal][compareVal if rowOrColumn == 0 else i]
              #also add every other row into the mix
              if compareVal != i:
                constraint_body &= ~Piece_RowOrColumn[rowOrColumn][compareVal]
            constraints.append(constraint_head | constraint_body)
  # hating my life: so turns out I forgot about diagonal lines. If all the queens arer in diagonals from each other, right now they bypass my checks.
  # so this solves that
  # I need to select the two important rows. also this can only be fore rows and its all cool.
  # i is for the first important row
  for i in range(BOARD_SIZE):
    # j is for the second important row
    for j in range(BOARD_SIZE):
      if j > i:
        #if (Row1 and row2) -> not row3 and not row4 ....
        constraint_head = Piece_RowOrColumn[0][i] & Piece_RowOrColumn[0][j]
        constraint_head = constraint_head.negate()
        constraint_body = true
        # k is iterated through all other rows
        for k in range(BOARD_SIZE):
          if k not in [i,j]:
            constraint_body &= ~Piece_RowOrColumn[0][k]
        constraints.append(constraint_head | constraint_body)

  return constraints