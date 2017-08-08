#!/usr/bin/env python3

import sys
from tkinter import *

###############################################################################
# GLOBAL VARIABLES
###############################################################################
esc = "\033["
clear        = esc + "2J"
reset_cursor = esc + "H"
reset        = esc + "0m"
bold         = esc + "1m"
underline    = esc + "4m"
red          = esc + "31m"
green        = esc + "32m"
yellow       = esc + "33m"
blue         = esc + "34m"
azul         = esc + "34m"
purple       = esc + "35m"
cyan         = esc + "36m"
white        = esc + "37m"
#block       = u"\u019f"  # for cli, could replace output[<var>]["char"]

# Represent colors. Might make life easier.
w = "w"
b = "b"
output = { 'w'  : { "color" : white,         "char" : "@" }
          ,'b'  : { "color" : reset,         "char" : " " }
          ,'r'  : { "color" : red,           "char" : "@" }
          ,'g'  : { "color" : green,         "char" : "@" }
          ,'y'  : { "color" : yellow,        "char" : "@" }
          ,'a'  : { "color" : azul,          "char" : "@" }
          ,'p'  : { "color" : purple,        "char" : "@" }
          ,'c'  : { "color" : cyan ,         "char" : "@" }
          ,'br' : { "color" : bold + red,    "char" : "X" }
          ,'bg' : { "color" : bold + green,  "char" : "X" }
          ,'by' : { "color" : bold + yellow, "char" : "X" }
          ,'ba' : { "color" : bold + azul,   "char" : "X" }
          ,'bp' : { "color" : bold + purple, "char" : "X" }
          ,'bc' : { "color" : bold + cyan,   "char" : "X" }
         }
colors = ( 'r', 'g', 'y', 'a', 'p', 'c', 'br', 'bg', 'by', 'ba', 'bp', 'bc' )
curr_color = 0
blank = w
unusable = b

# Not descriptive names. Oh well. Represent a board's max X and Y bounds.
X = 0
Y = 0

window = Tk()
width  = IntVar()
height = IntVar()
board_grid = []
board_grid_buttons = []

# pre-set pieces to make life easier for user hopefully.
standard_values = []
standard_pieces = (
     {'row' : 1, 'col' : 0, 'coords' : ((0,0),)}
    ,{'row' : 1, 'col' : 1, 'coords' : ((0,0),(1,0))}
    ,{'row' : 1, 'col' : 2, 'coords' : ((0,0),(1,0),(2,0))}
    ,{'row' : 1, 'col' : 3, 'coords' : ((0,0),(1,0),(2,0),(3,0))}
    ,{'row' : 2, 'col' : 0, 'coords' : ((0,0),(0,1),(1,0),(1,1))}
    ,{'row' : 2, 'col' : 1, 'coords' : ((0,0),(0,1))}
    ,{'row' : 2, 'col' : 2, 'coords' : ((0,0),(0,1),(0,2))}
    ,{'row' : 2, 'col' : 3, 'coords' : ((0,0),(0,1),(0,2),(0,3))}
    ,{'row' : 3, 'col' : 0, 'coords' : ((0,0),(0,1),(1,0))}
    ,{'row' : 3, 'col' : 1, 'coords' : ((0,0),(1,1),(1,0))}
    ,{'row' : 3, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1))}
    ,{'row' : 3, 'col' : 3, 'coords' : ((1,1),(0,1),(1,0))}
    ,{'row' : 4, 'col' : 0, 'coords' : ((0,0),(0,1),(0,2),(1,1))}
    ,{'row' : 4, 'col' : 1, 'coords' : ((1,0),(1,1),(1,2),(0,1))}
    ,{'row' : 4, 'col' : 2, 'coords' : ((1,0),(0,1),(1,1),(2,1))}
    ,{'row' : 4, 'col' : 3, 'coords' : ((0,0),(1,0),(2,0),(1,1))}
    ,{'row' : 5, 'col' : 0, 'coords' : ((1,0),(1,1),(0,1),(0,2))}
    ,{'row' : 5, 'col' : 1, 'coords' : ((0,0),(0,1),(1,1),(1,2))}
    ,{'row' : 5, 'col' : 2, 'coords' : ((1,0),(2,0),(0,1),(1,1))}
    ,{'row' : 5, 'col' : 3, 'coords' : ((0,0),(1,0),(1,1),(2,1))}
    ,{'row' : 6, 'col' : 0, 'coords' : ((0,0),(1,0),(0,1),(0,2))}
    ,{'row' : 6, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(1,2))}
    ,{'row' : 6, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(2,1))}
    ,{'row' : 6, 'col' : 3, 'coords' : ((2,0),(0,1),(1,1),(2,1))}
    ,{'row' : 7, 'col' : 0, 'coords' : ((1,0),(2,0),(1,1),(0,1),(0,2))}
    ,{'row' : 7, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(2,1),(2,2))}
    ,{'row' : 7, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(1,2),(2,2))}
    ,{'row' : 7, 'col' : 3, 'coords' : ((0,2),(1,1),(1,2),(2,0),(2,1))}
    ,{'row' : 8, 'col' : 0, 'coords' : ((0,2),(1,2),(1,1),(1,0),(2,0))}
    ,{'row' : 8, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(1,2),(2,2))}
    ,{'row' : 8, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(2,1),(2,2))}
    ,{'row' : 8, 'col' : 3, 'coords' : ((0,2),(0,1),(1,1),(2,1),(2,0))}
    )

there_are_more_pieces = False

###############################################################################
# MAIN
###############################################################################
def main(args):

    #
    # First things first, get the size of the board.
    #
    label = Label(window, text="Enter the board size:")
    label.grid(row=0, columnspan=2)

    width_label  = Label(window, text="Width:")
    height_label = Label(window, text="Height:")
    width_label.grid(row=1, column=0)
    height_label.grid(row=2, column=0)

    width_entry  = Entry(window, validate="key")
    height_entry = Entry(window, validate="key")
    width_entry.grid(row=1, column=1)
    height_entry.grid(row=2, column=1)

    done_button = Button(window, text="Done",
                         command= lambda: get_width_and_height(width_entry,
                                                      height_entry))
    done_button.grid(row=3, columnspan=2)

    window.mainloop()

    clear_window()

    #
    # Next, let the user click on cells that aren't playable.
    #
    middle_col  = int(int(width)/3)
    middle_span = ((int(width)+1)%2)+1

    label = Label(window, text="Click on cells that are unusable:")
    label.grid(row=0)

    # This will be updated to save values that are not playable.
    global board_grid
    global board_grid_buttons
    board_grid = [[blank for a in range(int(width))] for b in range(int(height))]

    frame = Frame(window)
    frame.grid(row=1)

    for a in range(int(height)):
        tmp = []
        for b in range(int(width)):
            curr_button = Button(frame, command = lambda curr_row=b, curr_col=a
                                 : toggleCell(frame, curr_row, curr_col))
            curr_button.grid(row=a, column=b)
            tmp.extend([curr_button])
        board_grid_buttons.append(tmp)

    done_button = Button(window, text="Done", command= lambda: quit_window())
    done_button.grid(row=2)

    window.mainloop()

    #
    # Next, let the user choose some pieces that are common to most boards.
    #

    global standard_values # just to remind us what we're dealing with below.
    num = 0

    for piece in standard_pieces:
        standard_values.extend([0])

        frame = Frame(window, highlightbackground="blue", highlightthickness=1)
        frame.grid(row=piece['row'], column=piece['col'])

        canvas = coord_to_piece(frame, piece['coords'])
        canvas.grid(rowspan=3)

        display = StringVar()
        display.set(0)

        label = Label(frame, textvariable=display)
        label.grid(column=1)

        plus_butt  = Button(frame, text="+", command=lambda d=display, n=num:
                                            standard_plus(d, n))
        minus_butt = Button(frame, text="-", command=lambda d=display, n=num:
                                            standard_minus(d, n))
        plus_butt.grid(row=1, column=1)
        minus_butt.grid(row=2, column=1)

        num += 1

    done_butt = Button(window, text="Done", command=quit_window)
    done_butt.grid(row=99, column=1, columnspan=2)

    window.mainloop()

    #
    # Next, let the user input any strange-looking pieces
    #

    more_input_needed = True

    check_for_more_pieces()

    while there_are_more_pieces

    sys.exit(0)




    init_list = [
#                  [w, w, w]
#                 ,[w, w, w]
#                 ,[w, w, w]
                 [w, w, w, b, w, w, b, w]
                ,[b, w, w, w, w, w, w, w]
                ,[w, w, b, w, w, w, w, w]
                ,[w, w, w, w, w, w, w, w]
                ,[b, w, w, w, w, w, w, w]
                ]
    board = Board(init_list)

    init_pieces = (
#                   Piece( ((0,0), (1,0), (1,1)) )
#                  ,Piece( ((0,0), (0,1), (0,2), (1,1), (1,2)) )
#                  ,Piece( ((0,0),) )
                   Piece( ((1,0), (0,1), (1,1), (2,1)) )
                  ,Piece( ((0,0), (0,1), (1,1), (1,0), (2,1)) )
                  ,Piece( ((0,0), (1,0), (1,1)) )
                  ,Piece( ((0,0), (1,0), (1,1), (2,1)) )
                  ,Piece( ((0,0), (0,1), (1,1), (1,0), (2,0)) )
                  ,Piece( ((1,0), (1,1), (0,1), (0,2)) )
                  ,Piece( ((0,0), (0,1), (1,1), (1,2)) )
                  ,Piece( ((1,0), (1,1), (0,1)) )
                  ,Piece( ((0,0), (1,0)) )
                  ,Piece( ((0,0),) )
                  )
    all = Pieces(init_pieces)

    global X, Y
    X = board.getMaxX()
    Y = board.getMaxY()

    print(all)
    print(board)

    #
    # Strategy: do some kind of depth-first tree recursion stuff.
    #
    # 1. Call recursive method with the blank board and all pieces.
    # 2. Recursive method will find a spot for the 0th piece given to it, and
    #    then call itself with the updated board and pieces.
    # 3. If the successive piece can't be placed, return false and then place
    #    the current piece on the next possible block.
    # 4. Repeat until solution is found (return true).
    #
    if solve(board, all):
        print(board)
        print("Yay")
    else:
        print("NO SOLUTION FOUND")

###############################################################################
# HELPER FUNCTIONS
###############################################################################
def solve(board, pieces):

    # Base case: when there are no pieces left to place.
    if pieces.isEmpty():
        return True

    piece = pieces.peek()
    
    for currY in range(Y):
        for currX in range(X):
            if board.can_fit(piece, currX, currY):

                board.place(piece, currX, currY, newColor())
                #print("woop", piece, currX, currY)
                #print(board)
                save_piece = pieces.pop()

                if solve(board, pieces):
                    return True
                else:
                    board.remove(piece, currX, currY)
                    pieces.push(save_piece)
                    decrementColor() 
    #print("can't fit piece ", piece)
    return False
        
def newColor():
    global curr_color
    ret = curr_color

    curr_color += 1
    if curr_color >= len(colors):
        curr_color = 0

    return colors[ret]

def decrementColor():
    global curr_color

    curr_color -= 1
    if curr_color < 0:
        curr_color = len(colors) - 1

def get_width_and_height(w_e, h_e):
    global width
    global height

    width  = w_e.get()
    height = h_e.get()
    quit_window()

def clear_window():
    for widget in window.grid_slaves():
        widget.destroy()

#
# removes button and switches its color from white to black or vice versa.
#
def toggleCell(frame, currX, currY):
    global board_grid
    global board_grid_buttons

    board_grid_buttons[currY][currX].destroy()

    if board_grid[currY][currX] == blank:
        board_grid_buttons[currY][currX] = Button(frame, text = 'X', bg = "black", command = lambda row=currY, col=currX: toggleCell(frame, col, row))
        board_grid[currY][currX] = unusable
    else:
        board_grid_buttons[currY][currX] = Button(frame, command = lambda row=currY, col=currX: toggleCell(frame, col, row))
        board_grid[currY][currX] = blank
    board_grid_buttons[currY][currX].grid(row=currY, column=currX)

#
# Takes a list of x,y coordinates and creates gui rectangles based on them.
#
def coord_to_piece(frame, coord_list):
    ret = Canvas(frame, width=60, height=50)

    for coord in coord_list:
        x = coord[0]
        y = coord[1]

        ret.create_rectangle(10+10*x, 10+10*y, 20+10*x, 20+10*y, fill="yellow")
    return ret

#
# Increments pre-set pieces
#
def standard_plus(display, index):
    global standard_values
    standard_values[index] += 1
    display.set(standard_values[index])

#
# Decrements pre-set pieces
#
def standard_minus(display, index):
    global standard_values
    if standard_values[index] > 0:
        standard_values[index] -= 1
        display.set(standard_values[index])

#
# Prompts user for more input
#
def check_for_more_pieces():
    label = Label(window, text="Are there any more pieces to enter?")
    yes_butt = Button(window, text="Yes", command=more_pieces(1))
    no_butt  = Button(window, text="No", command=more_pieces(0))

    label.grid(row=0)
    yes_butt.grid(row=1)
    no_butt.grid(row=2)

    window.mainloop()
    return

# Helper to above
def more_pieces(val):
    if val:
        there_are_more_pieces = True
    else:
        there_are_more_pieces = False
    return

def quit_window():
    clear_window()
    window.quit()

###############################################################################
# BACK END CLASSES
###############################################################################

# Board class: represents a game board which a player has to fill in.
class Board:

    #######################################
    # OVERRIDES AND BASIC BOARD FUNCTIONS #
    #######################################

    # Relies on the user entering a fully formed rectangle with blank/dead
    # cells. Might be a good idea to make sure all rows are the same size.
    def __init__(self, board_list):

        # Set max X and Y values.
        self.__maxY = len(board_list)
        longest = 0
        for row in board_list:
            longest = len(row) if len(row) > longest else longest
        self.__maxX = longest

        self.__data = board_list

    def __str__(self):
        ret = ""
        for row in self.__data:
            for cell in row:
                ret += output[cell]["color"] + output[cell]["char"] + reset
            ret += "\n"
        return ret

    # Return longest row
    def getMaxX(self):
        return self.__maxX

    # Return number of columns
    def getMaxY(self):
        return self.__maxY
        return len(self.__data)

    ###########################
    # PRIMARY BOARD FUNCTIONS #
    ###########################

    def can_fit(self, piece, currX, currY):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]

            if (cumulativeX >= self.__maxX or
                cumulativeY >= self.__maxY or
                self.__data[cumulativeY][cumulativeX] != blank):
                return False

        return True

    def place(self, piece, currX, currY, color):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]
            self.__data[cumulativeY][cumulativeX] = color

    def remove(self, piece, currX, currY):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]
            self.__data[cumulativeY][cumulativeX] = blank

# Pieces class: Represents a list of pieces
class Pieces:

    # pieces_list is tuple of Pieces.
    def __init__(self, pieces_list):
        self.__data = pieces_list

    def __str__(self):
        ret = ""
        for piece in self.__data:
            ret += str(piece.getData())
            ret += "\n"
        return ret

    def peek(self):
        return self.__data[0]

    def pop(self):
        ret = self.__data[0]
        self.__data = self.__data[1:]
        return ret

    def push(self, piece):
        self.__data = (piece,) + self.__data

    # "return if self.__data"?
    def isEmpty(self):
        if self.__data:
            return False
        else:
            return True


# Piece class: Represents a single piece which needs to fit onto a board.
#              Is really just a list of points which will be used as offsets.
class Piece:

    # coord_list is tuple of x, y coordinates saved as a tuple.
    def __init__(self, coord_list):
        self.__data = coord_list

    def __str__(self):
        return str(self.__data)

    def getData(self):
        return self.__data

###############################################################################
# GUI CLASSES - TODO: remove?
###############################################################################
#class Gui:

    # Gui starts off as a simple prompt for the size of the board.
    # root is the root window/tk.
    #def __init__(self, root):
    #    self.frame = 
        

###############################################################################
# END CODE
###############################################################################

if __name__ == "__main__":
    f = open('debug.txt', 'w')
    f.close()
    main(sys.argv)







