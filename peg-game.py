#!/usr/bin/env python3

#before running this call 'pip install graphics.py' or equivalent
from graphics import *
import random, time

#todo create an object for the board to define constants and methods instead of using global variables

#examples of previously found solutions, for reference only
a_solution = [1, 13, 4, 11, 21, 2, 32, 23, 19, 9, 29, 27, 28] #indexes of valid jumps, works if peg 0 is initially 0 and all rest are 1
another_solution = [0, 3, 6, 10, 16, 27, 18, 20, 5, 15, 30, 32, 31]  #indexes of valid jumps, works if peg 0 is initially 0 and all rest are 1

solutions = [] #store solutions found in an array of arrays

#global variable for storing peg states
#pegs normally ordered 0 to 14, 1 for present, 0 for empty
_peg_states = [0] * 15  

#initial board state
_initial_peg_states = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  

#pegs ordered 0 to 14, peg locations in x,y coordinates
_peg_locs = [[150, 50], [120,100], [180,100], [90,150], [150,150], [210,150], [60,200], [120,200], [180,200], [240,200], [30,250], [90,250], [150,250], [210,250], [270,250]]

#Jumps that would be possible if the conditions are met, peg values from 0 to 14
#there are 36 valid jumps; valid jumps are represented by initial peg, middle peg to be jumped, and final peg
_valid_jumps = [[3,1,0],  [5,2,0],  [6,3,1],  [8,4,1],  [7,4,2],  [9,5,2],   [10,6,3],  [12,7,3],  [5,4,3],  [0,1,3],  [11,7,4], [13,8,4],   [12,8,5],  [14,9,5],   [3,4,5],  [0,2,5],  [1,3,6],  [8,7,6],  [2,4,7],  [9,8,7],   [6,7,8],  [1,4,8],  [7,8,9],   [2,5,9],   [3,6,10],  [12,11,10],  [4,7,11],  [13,12,11],  [10,11,12],  [3,7,12],  [5,8,12],  [14,13,12],  [11,12,13],  [4,8,13],  [12,13,14],  [5,9,14]]

#array of 36 elements, possible jumps, 1 for possible, 0 for not possible
_possible = [0] * 36 

#keep track of the sequence of jumps tried in each round
_jump_sequence = [0] * 15

#create an array of peg circle objects
_circles = []
for peg in range(0,15): #0 to 14
    x,y = _peg_locs[peg] #get location of peg
    _circles.append(Circle(Point(x,y), 10)) 

_win = GraphWin("Peg Game Simulator", 300, 300)

def main():
    global _win
    global _jump_sequence

    #if no more possible moves stuck = 1, otherwise stuck = 0
    stuck = 0 

    #go until success (pegs left is 1)
    success = 0

    #track rounds of play until success
    theround = 0 
    
    initialize_board()
    initialize_state()

    msg = Text(Point(150,285), "Searching for a Solution!")
    msg.setSize(20)
    msg.draw(_win)

    while(success == 0):
        msg.setText("Searching for a Solution!")
        #_win.getMouse() # pause for click in window 
        #reset board back to the beginning state
        initialize_state()
        stuck = 0
        _jump_sequence.clear() #set jump sequence to null

        while(stuck == 0): 
            stuck  = evaluate_and_jump() #keep jumping until stuck

        print("round " + str(theround) + " complete!")
        theround = theround + 1 
        if(theround > 200):
            break #give up, something is wrong

        remaining_pegs = get_pegs_left()
        if(remaining_pegs < 2):
            print("success!")
            success = 1 
            msg.setText("Solution Found!")
            print(_jump_sequence)
            solutions.append(_jump_sequence)   #save the solution
            print("all found solutions so far")
            #todo - filter out known solutions
            for sol in solutions:
                print(sol) 
            success = 0 #jump out and stop
            play_solution(_jump_sequence)  #take a victory lap, slowly

        else:
            print("fail! pegs left: " + str(remaining_pegs))
            #success = 0
            #go back to the top of the while(success == 0) loop

    _win.getMouse() # pause for click in window 
    _win.close()

def initialize_board():
    global _peg_states #use global state array as initial state
    #draw triangle   
    t = Polygon(Point(150,0), Point(300,270), Point(0,270))
    t.setFill("green")
    t.draw(_win)

def initialize_state():
    #set initial state of pegs and draw circles
    for peg in range(0,15): #0 to 14
        set_peg_state(peg, _initial_peg_states[peg]) #set peg state based on initial values
        show_peg_state(peg, _initial_peg_states[peg]) #show the state separately

def set_peg_state(peg, peg_state):
    global _peg_states
    #set the value in the array
    _peg_states[peg] = peg_state

def show_peg_state(peg, peg_state):
    #show the peg state on the graphics

    #get location details for the peg number
    x,y = get_peg_location(peg)
    
    #get peg circle object
    c = get_circle_object(peg)
 
    #set fill color
    if(peg_state == 1): 
        c.setFill("red")
    else:
        c.setFill("black")
    #draw it
    try:
        c.draw(_win)
    except GraphicsError:
        pass

def get_peg_location(peg):
   #return location of peg
   global _peg_locs
   x,y = _peg_locs[peg]
   return x,y

def get_peg_state(peg): 
    #return peg state value
    global _peg_states
    return _peg_states[peg]

def get_circle_object(peg):
      #return circle object for the peg
    global _circles
    return _circles[peg]

def get_pegs_left():
    total = 0
    for peg in range(0,15): #0 to 14
        if(_peg_states[peg] == 1):
            total = total + 1
    return total

def get_jumps_possible():
    
    #total number of possible jumps found
    #total = 0
    #array of 36 elements, possible jumps, 1 for possible, 0 for not possible
    possible = [0] * 36 

    for i in range(0,36): #0 to 35
        #for each valid jump, check if the condition is present
        if(_peg_states[_valid_jumps[i][0]] == 1 and _peg_states[_valid_jumps[i][1]]  == 1 and _peg_states[_valid_jumps[i][2]] == 0):   
            #print("valid jump!: " + str(_valid_jumps[i][0]) + " " + str(_valid_jumps[i][1]) + " " + str(_valid_jumps[i][2]) )
            #_possible[i] = 1
            possible[i] = 1 #local variable to be returned
            #total = total + 1    
    
    #return total
    return possible

def evaluate_and_jump():

    possible = [0] * 36 #array of 36 potential jumps 
    total_possible = 0
    possible_jump_indexes = [0] * 12 #array to store indexes of possible jumps, assume no more than 12 would be possible at one time

    #populate array of possible jumps (value 1) and not possible jumps (value 0) out of the 36 valid potential jumps
    possible = get_jumps_possible()

    for i in range(0,36): #0 to 35
        if(possible[i] == 1):
            possible_jump_indexes[total_possible] = i #store the index of the possible jump, use total_possible as array index
            total_possible = total_possible + 1

    if(total_possible == 0):
        return 1  #stuck, no more moves possible 
    
    #Pick a jump
    #we want a random number that goes from 0 to (number of possible jumps - 1) representing the index of the myjumps list
    random_pick = int(total_possible * random.random() )   #random jump, value from 0 to myjumps_total - 1, which should form a good index for the list

    #take the jump, based on the random seelction in the list of indexes of possible jumps (in the array of 36 valid jumps)    
    make_jump(possible_jump_indexes[random_pick]) 

    return 0 #don't know if stuck yet, check next go around 

def make_jump(jump_index):
    global _peg_states
    global _valid_jumps
    global _jump_sequence

    #the three pegs involved in the jump
    peg1 = _valid_jumps[jump_index][0]
    peg2 = _valid_jumps[jump_index][1]
    peg3 = _valid_jumps[jump_index][2]

    #print("making jump: #" + str(jump_index) + " [" + str(_valid_jumps[jump_index][0]) + " " +  str(_valid_jumps[jump_index][1]) + " " + str(_valid_jumps[jump_index][2]) + "]")
    print("making jump: #" + str(jump_index) + " [" + str(peg1) + " " +  str(peg2) + " " + str(peg3) + "]")
    
    _jump_sequence.append(jump_index)

    set_peg_state(peg1, 0)
    show_peg_state(peg1,0)
    set_peg_state(peg2, 0)
    show_peg_state(peg2,0)
    set_peg_state(peg3, 1)
    show_peg_state(peg3,0)

def show_jump(jump_index):
    #show the jump, without actually making it. used for playing jump sequence, when solution found.
    global _valid_jumps

    #the three pegs involved in the jump
    peg1 = _valid_jumps[jump_index][0]
    peg2 = _valid_jumps[jump_index][1]
    peg3 = _valid_jumps[jump_index][2]

    print("showing jump: #" + str(jump_index) + " [" + str(peg1) + " " +  str(peg2) + " " + str(peg3) + "]")

    show_peg_state(peg1, 0)
    show_peg_state(peg2, 0)
    show_peg_state(peg3, 1)

def play_solution(solution):

    initialize_state()

    for move in solution:
        show_jump(move)
        time.sleep(3)

if __name__ == '__main__':
    main()