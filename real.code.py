import random 

pieces = []
def roll():
    for i in range (3):
        pieces.append(random.randomint(0, 4))
#0 = "h"     #horse
#1 = "c"     #camel
#2 = "s"     #sheep
#3 = "g"     #goat

score = 0
def scoring_condition():
    roll()
    if pieces == []
    if pieces == [3, 3, 3, 3]:
       score += 8
    for i in range (3):
        if pieces == [i, i, i, i]:
            score += 4
    for i in range 
