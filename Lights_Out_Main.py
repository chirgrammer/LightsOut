from tkinter import *
from MatrixRing import *
from PrimeField import *
import random

# Basic functions for setting up the board
# Command to give all lights the same rule.
def copyRule(crule):  # If there are m rows and n columns, crule is a 2m-1 x 2n-1 matrix of elements of
    # the finite field F_p where p is the number of states. To form the rule R for the lights out
    # board, the i, j entry of R is the submatrix of r ending at (2m-2-i, 2n-2-j) and starting at
    # (m-1-i, n-1-j).
    m = int((len(crule.entries)+1)/2)  # Variable representing the number of rows of the returned rule
    n = int((len(crule.entries[0])+1)/2)  # Variable representing the number of columns of the returned rule
    rule = []  # Rule we wish to return
    rowrule = [] # A temporary placeholder which collects all matrices in a row of rule
    for r in range(m):
        for c in range(n):
            # Adding rule at light with indices (r,c) to rowrule.
            rowrule.append(Matrix.submatrix(crule, m-r, n-c, 2*m-1-r, 2*n-1-c))
        rule.append(rowrule)  # Adding rowrule to rule
        rowrule = []
    return rule

def defaultrule(m, n, f):  # Changes the rule of the lights out board to the default when there are
    # |f| states
    m1 = 2*m-1
    n1 = 2*n-1
    defcrulerow = []  # A row of the rule which will be copied to all lights
    defcruleentries = []  # The rule which will be copied to all lights
    for r in range(m1):
        for c in range(n1):
            # These are the locations of the three, four, or five lights whose states will be changed
            if [r, c] == [m-2, n-1] or [r, c] == [m-1, n-2] or [r, c] == [m-1, n-1] or [r, c] == [m, n-1] or [r, c] == [m-1,n]:
                defcrulerow.append(1)
            else:
                defcrulerow.append(0)
        defcruleentries.append(defcrulerow)
        defcrulerow = []
    defcrule = Matrix(defcruleentries, f)  # Creates matrix which will be copied to create the
    # default rule
    defrule = copyRule(defcrule)  # Creates the default rule to be returned.
    return defrule

def defaultcolors(n):  # Returns the default color scheme for n colors. The default color scheme when
    # there are n colors are just n approximately evenly spaced shades of gray
    colors = ["#000000"]  # List containing only the black color
    for i in range(1,n):
        j = format(int(255*i/(n-1)), "02x")
        s = f"#{j}{j}{j}"
        colors.append(s)
    return colors

def defaultsolcolors(n):  # Returns the default color scheme for n colors. The default color scheme when
    # there are n colors are just n approximately evenly spaced shades of gray
    colors = ["#000000"]  # List containing only the black color
    for i in range(1,n):
        j = format(int(255*i/(n-1)), "02x")
        s = f"#00{j}00"
        colors.append(s)
    return colors

def findsolboard(rule, board):  # Finds a solution for a given lights out board and returns a matrix
    # of the number of times each light needs to be clicked to return the board to the state where
    # all lights are off.
    rulematrix = []  # initializes 2D list of entries of rule matrix used to solve the system
    # of equations which allows us to find a solution to the given board.
    # creates rule matrix. If the dimensions of the board are r by c, rulematrix
    for c in range(len(rule[0])):
        for r in range(len(rule)):
            if r == 0 and c == 0:  # For the first term, convert the matrix in the upper left
                # corner of rule to a column vector
                rulematrix = Matrix.matrixtocolvector(rule[0][0])
            # For the rest of the terms, repeatedly join together entries of rule proceeding
            # down the columns first and then to the right after converting them to column
            # vectors.
            else:
                rulematrix = Matrix.hjoin(rulematrix, Matrix.matrixtocolvector(rule[r][c]))
    boardcvector = Matrix.matrixtocolvector(board)  # Converts board into a column vector
    puzzlesol = Matrix.solve(rulematrix, boardcvector)  # Finds solution to the given board
    # Converts solution into a matrix detailing the number of times we have to click each
    # button to get a board of all lights fully off.
    puzzlesol = Matrix.colvectortomatrix(puzzlesol, board.rows, board.cols)
    return puzzlesol
                

# Game Settings Variables:
num_rows = 10  # Integer representing the number of rows of lights
num_cols = 10  # Integer representing the number of columns of lights
num_states = 2 # Number of states the lights have
f = PrimeField(num_states)  # Field for which the states of the lights are in
# Matrix containing the states of every light. By default, every light is set to be on.
# A num_rows by num_cols 2D List of Matrices each representing the way the states of the lights
# change when the light at its index is clicked change. It is by default set to the normal
# rule where when the state of a light is changed, all adjacent lights also switch.
game_rule = defaultrule(num_rows, num_cols, f)
game_colors = defaultcolors(num_states)  # Default colors of the game
sol_colors = defaultsolcolors(num_states)  # Default colors for displaying solutions

# Game Variables:
num_moves = 0
# Default states assigned to the lights where all lights are on their brightest setting.
game_states = Matrix.const(num_rows, num_cols, f, num_states-1)
original_states = Matrix(game_states.entries, game_states.field)  # Contains original states before player changes them to allow the
# player to restart
game_buttons = []  # 2D List of buttons for the game board.
game_solution = findsolboard(game_rule, game_states)  # Solution of given board
original_game_solution = Matrix(game_solution.entries, game_solution.field)  # Solution of original game board for when player choses to restart
show_solution = False  # Variable that indicates whether user would like to see the solution
# to the given puzzle or not.

# Commands for functions in game window

def start():  # Creates the game window and hides original
    # Config Variables:
    defaultbackgroundcolor = "#999999"  # Background color of window
    gamemenuwidgetbgcolor = "#CCCCCC"  # Widget background color
    lightbuttonheight = 1  # Height of light button
    lightbuttonwidth = 3  # Width of light button
    lightbuttonfont = ("Calibri", 18)
    lightbuttonfontcolor = "#007F00"
    gamewindowpadx = 20  # x spacing between lights and edge of window
    gamewindowpady = 20  # y spacing between lights and edge of window
    gamemenuwidgetheight = 1  # Height of widgets in the game menu
    gamemenuwidgetwidth = 15  # Width of widgets in the game menu
    gamemenuwidgetrelief = RAISED  # Relief of widgets in game menu
    gamemenuwidgetfont = ("Calibri", 18)  # Font of widgets in game menu
    gamemenuwidgetborder = 4  # Size of game menu widget border
    gamemenuwidgetpadx = 20  # x spacing between game menu widgets and edge of frame
    gamemenuwidgetpady = 5  # y spacing between game menu widgets

    # Beginning of method creation
    game_buttons = []

    GameWindow = Tk()
    MainMenu.withdraw()

    # Frame containing all the lights
    GameWindowLightsFrame = Frame(GameWindow,
                                  bg=defaultbackgroundcolor,
                                  padx=gamewindowpadx,
                                  pady=gamewindowpady)
    GameWindowLightsFrame.grid(row=0, column=0, sticky="NS")  # Positions the frame with the lights on the left

    # Frame containing the number of moves, buttons for returning to the menu, showing the solution
    # and quitting the game.
    GameWindowMenuFrame = Frame(GameWindow,
                                bg=defaultbackgroundcolor,
                                padx=gamewindowpadx,
                                pady=gamewindowpady)
    GameWindowMenuFrame.grid(row=0, column=1, sticky="NS")  # Positions the frame with game options and score on
    # the right
    # Creates buttons representing the lights
    game_buttons_row = []  # A temporary row of buttons to be added to the 2D list of buttons eventually.
    # Creates the board of lights (i.e. 2D list of buttons)
    for r in range(num_rows):
        for c in range(num_cols):
            game_buttons_row.append(Button(GameWindowLightsFrame,
                                           bg=game_colors[game_states.entries[r][c]],
                                           fg=lightbuttonfontcolor,
                                           width=lightbuttonwidth,
                                           height=lightbuttonheight,
                                           font=lightbuttonfont))
        game_buttons.append(game_buttons_row)
        game_buttons_row = []

    # Command used to update buttons colors with states matrix game_states
    def updatelights():
        global num_rows
        global num_cols
        global game_solution
        global show_solution
        global game_colors
        # Checks once if player requests to see the solution
        if show_solution:
            for i in range(num_rows):
                for j in range(num_cols):
                    game_buttons[i][j].configure(bg=game_colors[game_states.entries[i][j]])
                    if game_solution.entries[i][j] != 0:
                        game_buttons[i][j].configure(bg=sol_colors[game_solution.entries[i][j]])
        # Does not show text if player does not request solution.
        else:
            for i in range(num_rows):
                for j in range(num_cols):
                    game_buttons[i][j].configure(bg=game_colors[game_states.entries[i][j]])

    # Command which is assigned to each button in board of lights:
    def updategamestates(r, c):  # Updates the states of the board once button in row r column c
        # is clicked.
        def changegamestates():
            global num_moves  # global keyword needed as outside variable is being accessed
            global game_states  # global keyword needed as outside variable is being accessed
            global game_solution  # global keyword needed as outside variable is being accesed
            num_moves += 1  # Increases number of moves by 1
            GameMovesCountLabel["text"] = f"Moves: {num_moves}"
            # Changes matrix of button states
            game_states = Matrix.add(game_states, game_rule[r][c])
            game_solution.entries[r][c] = game_states.field.add(game_solution.entries[r][c], game_states.field.one())
            original_game_solution.printentries()
            # Updates colors of game buttons once button is clicked
            updatelights()

        return changegamestates

    # Assigns commands to each button in the board of lights
    for r in range(num_rows):
        for c in range(num_cols):
            game_buttons[r][c]["command"] = updategamestates(r, c)
            game_buttons[r][c].grid(row=r, column=c)

    # Commands for buttons in game menu
    def restart():
        global game_states
        global original_states
        global game_solution
        global original_game_solution
        num_moves = 0
        GameMovesCountLabel["text"] = f"Moves: {num_moves}"
        game_states = original_states  # Sets game light states to original states
        game_solution = original_game_solution  # Sets game solution to original game solution
        game_solution.printentries()
        updatelights()  # Changes colors of the lights to the original colors.

    def randomize():  # Randomizes the board and resets move count
        global num_moves
        global game_states
        global original_states
        global game_solution
        global original_game_solution
        num_moves = 0  # Increases number of moves by 1
        GameMovesCountLabel["text"] = f"Moves: {num_moves}"
        game_states = Matrix.const(num_rows, num_cols, f, 0)
        r = 0
        for i in range(num_rows):
            for j in range(num_cols):
                r = random.randint(0,num_states-1)
                game_solution.entries[i][j] = r
                if r != 0:
                    game_states = Matrix.add(game_states, Matrix.scale(game_rule[i][j], r))
        original_states = Matrix(game_states.entries, game_states.field)
        original_game_solution = Matrix(game_solution.entries, game_solution.field)
        updatelights()

    def showsolution():
        global show_solution
        show_solution = not show_solution
        if show_solution:
            GameShowSolutionButton.configure(text="Hide Solution")
        else:
            GameShowSolutionButton.configure(text="Show Solution")
        updatelights()

    def returntomenu():
        GameWindow.destroy()
        MainMenu.deiconify()

    # Creating widgets for game menu
    def GameMenuLabel(t):  # Creates game menu label widget with text t
        return Label(GameWindowMenuFrame,
                     text=t,
                     height=gamemenuwidgetheight,
                     width=gamemenuwidgetwidth,
                     bg=gamemenuwidgetbgcolor,
                     bd=gamemenuwidgetborder,
                     relief=SUNKEN,
                     font=gamemenuwidgetfont)

    def GameMenuButton(t, cmd):  # Creates game menu button widget with text t and command c
        return Button(GameWindowMenuFrame,
                      text=t,
                      height=gamemenuwidgetheight,
                      width=gamemenuwidgetwidth,
                      bg=gamemenuwidgetbgcolor,
                      bd=gamemenuwidgetborder,
                      relief=gamemenuwidgetrelief,
                      font=gamemenuwidgetfont,
                      command=cmd)

    GameMovesCountLabel = GameMenuLabel(f"Moves: {num_moves}")
    GameMovesCountLabel.grid(row=0, column=0, padx=gamemenuwidgetpadx, pady=20, sticky="s")

    GameRandomizeButton = GameMenuButton(t="Randomize Board", cmd=randomize)
    GameRandomizeButton.grid(row=1, column=0, padx=gamemenuwidgetpadx, pady=gamemenuwidgetpady, sticky="s")

    GameRestartButton = GameMenuButton(t="Restart", cmd=restart)
    GameRestartButton.grid(row=2, column=0, padx=gamemenuwidgetpadx, pady=gamemenuwidgetpady, sticky="s")

    GameShowSolutionButton = GameMenuButton(t="Show Solution", cmd=showsolution)
    GameShowSolutionButton.grid(row=3, column=0, padx=gamemenuwidgetpadx, pady=gamemenuwidgetpady, sticky="s")

    GameReturnToMenuButton = GameMenuButton(t="Return to menu", cmd=returntomenu)
    GameReturnToMenuButton.grid(row=4, column=0, padx=gamemenuwidgetpadx, pady=gamemenuwidgetpady, sticky="s")

    GameQuitButton = GameMenuButton(t="Quit", cmd=quit)
    GameQuitButton.grid(row=5, column=0, padx=gamemenuwidgetpadx, pady=gamemenuwidgetpady, sticky="s")

    GameWindow.mainloop()

# Commands for functions in the settings window
def settings():  # Creates settings window and hides main menu
    # Config Variables:
    settingsmenuwidgetheight = 1
    settingsmenuwidgetwidth = 20
    settingsmenuwidgetbgcolor = "#CCCCCC"
    settingsmenuwidgetborder = 4
    settingsmenuwidgetrelief = SUNKEN
    settingsmenubuttonrelief = RAISED
    settingsmenuwidgetfont = ("Calibri", 18)

    SettingsWindow = Tk()
    MainMenu.withdraw()

    # Settings commands
    def returntomenu():
        global num_rows
        global num_cols
        global num_states
        global game_rule
        global game_solution
        global game_states
        global original_game_solution
        global game_colors
        global sol_colors
        global f
        num_rows = int(SettingsMenuRowEntry.get())
        num_cols = int(SettingsMenuColEntry.get())
        num_states = int(SettingsMenuStatesEntry.get())
        f = PrimeField(num_states)
        game_colors = defaultcolors(num_states)
        sol_colors = defaultsolcolors(num_states)
        game_rule = defaultrule(num_rows, num_cols, f)
        game_states = Matrix.const(num_rows, num_cols, f, num_states-1)
        original_game_states = Matrix(game_states.entries, game_states.field)
        game_solution = findsolboard(game_rule, game_states)
        original_game_solution = Matrix(game_solution.entries, game_solution.field)
        SettingsWindow.destroy()


        MainMenu.deiconify()

    def SettingsMenuLabel(t):  # Creates game menu label widget with text t
        return Label(SettingsWindow,
                     text=t,
                     height=settingsmenuwidgetheight,
                     width=settingsmenuwidgetwidth,
                     bg=settingsmenuwidgetbgcolor,
                     bd=settingsmenuwidgetborder,
                     relief=settingsmenuwidgetrelief,
                     font=settingsmenuwidgetfont)

    def SettingsMenuEntryBox():  # Creates game menu label widget with text t
        return Entry(SettingsWindow,
                     width=settingsmenuwidgetwidth,
                     bg=settingsmenuwidgetbgcolor,
                     bd=settingsmenuwidgetborder,
                     relief=settingsmenuwidgetrelief,
                     font=settingsmenuwidgetfont)

    def SettingsMenuButton(t, cmd):  # Creates game menu label widget with text t
        return Button(SettingsWindow,
                     text=t,
                     height=settingsmenuwidgetheight,
                     width=settingsmenuwidgetwidth,
                     bg=settingsmenuwidgetbgcolor,
                     bd=settingsmenuwidgetborder,
                     relief=settingsmenubuttonrelief,
                     font=settingsmenuwidgetfont,
                     command=cmd)

    SettingsMenuRowLabel = SettingsMenuLabel("Number of rows")
    SettingsMenuRowLabel.grid(row=0, column=0)

    SettingsMenuRowEntry = SettingsMenuEntryBox()
    SettingsMenuRowEntry.grid(row=0, column=1)

    SettingsMenuColLabel = SettingsMenuLabel("Number of columns")
    SettingsMenuColLabel.grid(row=1, column=0)

    SettingsMenuColEntry = SettingsMenuEntryBox()
    SettingsMenuColEntry.grid(row=1, column=1)

    SettingsMenuStatesLabel = SettingsMenuLabel("Number of states")
    SettingsMenuStatesLabel.grid(row=2, column=0)

    SettingsMenuStatesEntry = SettingsMenuEntryBox()
    SettingsMenuStatesEntry.grid(row=2, column=1)

    SettingsMenuReturnButton = SettingsMenuButton(t="Return to menu", cmd=returntomenu)
    SettingsMenuReturnButton.grid(row=3, column=0)

    SettingsMenuQuitButton = SettingsMenuButton(t="Quit", cmd=quit)
    SettingsMenuQuitButton.grid(row=3, column=1)

    SettingsWindow.mainloop()
# Config Variables:

h = 1  # Variable for height of buttons
w = 15  # Variable for width of buttons
brd = 5  # Variable for size of borders of buttons
bgcol = "#999999"  # Variable for color of background
bcol = "#CCCCCC"  # Variable for color of buttons
lcol = "#FFFFFF"  # Variable for color of label
bfont = ("Calibri", 18)  # Variable for button font
lfont = ("Calibri", 30)  # Variable for label font
rel = RAISED  # Variable for relief of buttons and title
pdx = 20 # Variable for x spacing of buttons
pdy = 5 # Variable for y spacing of buttons

MainMenu = Tk()  # Creates new window
MainMenu.config(background=bgcol)

TitleFrame = Frame(MainMenu, bg=bgcol, bd=5, relief=SUNKEN)  # Creates a frame for the title label
TitleFrame.grid(row=0, column=0, padx=50, pady=20)

MainMenuButtonFrame = Frame(MainMenu, bg=bgcol)  # Creates a frame for the buttons
MainMenuButtonFrame.grid(row=1, column=0, pady=20)

TitleLabel = Label(TitleFrame, text="Lights Out", font=lfont, width=15, height=2, bg=lcol, bd= 5, relief=SUNKEN)
TitleLabel.grid(row=0, column=0)

StartButton = Button(MainMenuButtonFrame, text="Play", command=start, height=h, width=w,
                     bd=brd, relief=rel, bg=bcol, font=bfont)
StartButton.grid(row=0, column=0, padx=pdx, pady=pdy)

SettingsButton = Button(MainMenuButtonFrame, text="Game Settings", command=settings, height=h, width=w,
                        bd=brd, relief=rel, bg=bcol, font=bfont)
SettingsButton.grid(row=1, column=0, padx=pdx, pady=pdy)

QuitButton = Button(MainMenuButtonFrame, text="Quit", command=quit, height=h, width=w,
                    bd=brd, relief=rel, bg=bcol, font=bfont)
QuitButton.grid(row=2, column=0, padx=pdx, pady=pdy)
MainMenu.mainloop()