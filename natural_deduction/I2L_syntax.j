/*
    $Id: I2L_syntax.j,v 1.18 2012/03/22 15:24:52 rbornat Exp $

    Copyright (C) 2000-8 Richard Bornat
     
        richard@bornat.me.uk

    This file is part of the I2L logic encoding, distributed with jape.

    Jape is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Jape is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with jape; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    (or look at http://www.gnu.org).

*/

CLASS VARIABLE  x y z
      		u v w
                i j k
CLASS FORMULA   BK1 BK2 BK3 BK4 BK6 BK7 BK8 BK9
                BKNoMoves
                CM 
                SM
                A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
CLASS BAG FORMULA Γ

CONSTANT ⊥ ⊤

PREFIX  10  actual

INFIX   100R    →
INFIX   120L    ∨
INFIX   140L    ∧

PREFIX  200 ¬

LEFTFIX 200 ∀ .
LEFTFIX 200 ∃ .

JUXTFIX 3000
SUBSTFIX    4000 

BIND x SCOPE A IN ∀x . A
BIND x SCOPE B IN ∃x . B

SEQUENT IS BAG ⊢ FORMULA

INITIALISE autoAdditiveLeft     true /* allow rules to be stated without an explicit left context */
INITIALISE interpretpredicates  true /* allow predicate syntax ... */
