# Class creating the GUI for the Lights Out Game
from Lights_Out_Color_Schemes import *
from Lights_Out_Board import *
from MatrixRing import *
from PrimeField import *
from IntegerTools import *
import tkinter

class MainMenuWindow(tkinter.Tk):
    def __init__(self, lightboarddata=None, lightboardtheme=None):
        super().__init__()

        if lightboarddata is None:
            self.lightboarddata = LightBoardAttributes()
        else:
            self.lightboarddata = lightboarddata
        if lightboardtheme is None:
            self.lightboardtheme = LightsOutTheme(num_colors=self.lightboarddata.num_states)
        else:
            self.lightboardtheme = lightboardtheme

        # Config variables for brevity
        mmwbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        mmwpadx = self.lightboardtheme.themebackgroundconfig.get("mmpadx")
        mmwpady = self.lightboardtheme.themebackgroundconfig.get("pady")

        self.config(background=mmwbg)

        # Creates a frame for the title
        mmtitleframe = Frame(self, bg=mmwbg, bd=5, relief=SUNKEN)
        mmtitleframe.grid(row=0, column=0, padx=mmwpadx, pady=mmwpady)

        # Commands for main menu buttons:
        def start():
            gamewindow = GameWindow(master=self,
                                    lightboarddata=self.lightboarddata,
                                    lightboardtheme=self.lightboardtheme)
            self.withdraw()
            gamewindow.mainloop()
            
        def settings():
            settingswindow = SettingsWindow(master=self,
                                            num_rows=self.lightboarddata.num_rows,
                                            num_cols=self.lightboarddata.num_cols,
                                            num_states=self.lightboarddata.num_states,
                                            board_states=self.lightboarddata.board_states,
                                            board_rule=self.lightboarddata.board_rule,
                                            lightboardtheme=self.lightboardtheme)
            self.withdraw()
            settingswindow.mainloop()

        # Creates a frame for the main menu buttons
        mmbuttonframe = Frame(self, bg=mmwbg)
        mmbuttonframe.grid(row=1, column=0)

        # Label for title of game with large font
        mmtitle = self.lightboardtheme.themelabel(parent=mmtitleframe, t="Lights Out", size="l")
        mmtitle.config(bd=0, relief=FLAT)
        mmtitle.grid(row=0, column=0)

        mmstart = self.lightboardtheme.themebutton(parent=mmbuttonframe, t="Play", c=start)
        mmstart.grid(row=0, column=0, padx=mmwpadx, pady=mmwpady)

        mmsettings = self.lightboardtheme.themebutton(parent=mmbuttonframe, t="Game Settings", c=settings)
        mmsettings.grid(row=1, column=0, padx=mmwpadx, pady=mmwpady)

        mmquit = self.lightboardtheme.themebutton(parent=mmbuttonframe, t="Quit", c=quit)
        mmquit.grid(row=2, column=0, padx=mmwpadx, pady=mmwpady)

class GameWindow(tkinter.Toplevel):
    def __init__(self, master, lightboarddata, lightboardtheme):
        # Assign instance variables
        super().__init__(master)
        self.lightboarddata = lightboarddata
        self.lightboardtheme = lightboardtheme

        # Config variables for brevity
        gwbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        gwbpadx = self.lightboardtheme.themebackgroundconfig.get("owpadx")
        gwbpady = self.lightboardtheme.themebackgroundconfig.get("pady")
        gwwpadx = self.lightboardtheme.themewidgetconfig.get("padx")
        gwwpady = self.lightboardtheme.themewidgetconfig.get("pady")

        self.config(bg=gwbg)

        # Frame containing all the lights
        gwlightsframe = Frame(self, bg=gwbg, padx=gwbpadx, pady=gwbpady)
        gwlightsframe.grid(row=0, column=0, sticky="NS")

        # Creating the buttons for the lights out grid
        gwlightgrid = [] # 2D List containing all the buttons
        for r in range(self.lightboarddata.num_rows):
            gwlightgridrow = [] # 1D list containing a row of buttons
            for c in range(self.lightboarddata.num_cols):
                gwlightgridrow.append(self.lightboardtheme.themelightbutton(parent=gwlightsframe, 
                                                                            bg=self.lightboardtheme.lightcolors[self.lightboarddata.board_states.entries[r][c]]))
            gwlightgrid.append(gwlightgridrow)

        # Command to check if game is won abd creates a game won window if the game was won
        def isgamewon():
            brddata=self.lightboarddata
            if Matrix.equals(brddata.board_states, Matrix.const(brddata.num_rows, brddata.num_cols, brddata.field, 0)):
                gamewonwindow = GameWonWindow(master=self)
                gamewonwindow.grab_set()

        # Command to update colors of lights
        def updatelights():
            brddata = self.lightboarddata
            gmovescountlabel["text"] = f"Moves: {brddata.num_moves}"
            for i in range(brddata.num_rows):
                for j in range(brddata.num_cols):
                    gwlightgrid[i][j].configure(bg=self.lightboardtheme.lightcolors[brddata.board_states.entries[i][j]])
                    if brddata.board_solution.entries[i][j] != 0 and brddata.show_solution:
                        gwlightgrid[i][j].configure(bg=self.lightboardtheme.solcolors[brddata.board_solution.entries[i][j]])

        # Command which is assigned to each light in the board of lights:
        def updategamestates(r, c):
            def changegamestates():
                brddata = self.lightboarddata
                brddata.num_moves += 1
                brddata.board_states = Matrix.add(brddata.board_states, brddata.board_rule[r][c])
                brddata.board_solution.entries[r][c] = brddata.field.add(brddata.board_solution.entries[r][c], -1)
                updatelights()
            return changegamestates

        # Assigns commands to each button in the board of lights
        for r in range(self.lightboarddata.num_rows):
            for c in range(self.lightboarddata.num_cols):
                gwlightgrid[r][c]["command"] = updategamestates(r, c)
                gwlightgrid[r][c].grid(row=r, column=c)

        # Commands for buttons in game menu
        def restart():  # Restarts game to original states
            self.lightboarddata.num_moves = 0
            self.lightboarddata.board_states = Matrix(self.lightboarddata.original_board_states.entries, self.lightboarddata.field)
            self.lightboarddata.board_solution = Matrix(self.lightboarddata.original_board_solution.entries, self.lightboarddata.field)
            updatelights() # Changes colors of lights to original colors

        def randomize():
            self.lightboarddata.randomizestates()
            self.lightboarddata.num_moves = 0
            updatelights()

        def showsolution():
            self.lightboarddata.show_solution = not self.lightboarddata.show_solution
            if self.lightboarddata.show_solution:
                gshowsolutionbutton.configure(text="Hide Solution")
            else:
                gshowsolutionbutton.configure(text="Show Solution")
            updatelights()

        def returntomenu():
            self.destroy()
            self.master.deiconify()

        # Frame containing game menu and number of moves
        gwmenuframe = Frame(self, bg=gwbg, padx=gwbpadx, pady=gwbpady)
        gwmenuframe.grid(row=0, column=1, sticky="NS")

        # Label displaying number of moves player has performed
        gmovescountlabel = self.lightboardtheme.themelabel(parent=gwmenuframe, t=f"Moves: {self.lightboarddata.num_moves}")
        gmovescountlabel.grid(row=0, column=0, padx=gwwpadx, pady=gwwpady)

        # Button allowing player to randomize the board
        grandomizebutton = self.lightboardtheme.themebutton(parent=gwmenuframe, t="Randomize Board", c=randomize)
        grandomizebutton.grid(row=1, column=0, padx=gwwpadx, pady=gwwpady)

        # Button allowing player to restart the game
        grestartbutton = self.lightboardtheme.themebutton(parent=gwmenuframe, t="Restart Game", c=restart)
        grestartbutton.grid(row=2, column=0, padx=gwwpadx, pady=gwwpady)

        # Button allowing player to view the solution
        gshowsolutionbutton = self.lightboardtheme.themebutton(parent=gwmenuframe, t="Show Solution", c=showsolution)
        gshowsolutionbutton.grid(row=3, column=0, padx=gwwpadx, pady=gwwpady)

        # Button allowing player to return to main menu
        greturntomenubutton = self.lightboardtheme.themebutton(parent=gwmenuframe, t="Return to Menu", c=returntomenu)
        greturntomenubutton.grid(row=4, column=0, padx=gwwpadx, pady=gwwpady)

        # Button allowing player to quit the game
        gquitbutton = self.lightboardtheme.themebutton(parent=gwmenuframe, t="Quit Game", c=quit)
        gquitbutton.grid(row=5, column=0, padx=gwwpadx, pady=gwwpady)

class SettingsWindow(tkinter.Toplevel):
    def __init__(self, master, num_rows, num_cols, num_states, board_states, board_rule, lightboardtheme):
        # Assign instance variables
        super().__init__(master)
        self.num_rows = num_rows
        self.original_num_rows = self.num_rows
        self.num_cols = num_cols
        self.original_num_cols = self.num_cols
        self.num_states = num_states
        self.original_num_states = self.num_states
        self.board_states = board_states
        self.board_rule = board_rule
        self.lightboardtheme = lightboardtheme
        self.expandable_rule = False
        self.field = PrimeField(num_states)
        # Variable existing purely if player changes number of states after he changes board rule
        self.isrulemodified = False
        # Variable indicating whether the player wishes to proceed after such a change
        self.wishtoproceed = True

        # Config variables for readability
        swbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        swbpadx = self.lightboardtheme.themebackgroundconfig.get("owpadx")
        swbpady = self.lightboardtheme.themebackgroundconfig.get("pady")
        swwpadx = self.lightboardtheme.themewidgetconfig.get("padx")
        swwpady = self.lightboardtheme.themewidgetconfig.get("pady")

        self.config(bg=swbg)
        # Frame for settings window containing the title of the window
        swtitleframe = Frame(self, bg=swbg, bd=5, relief=SUNKEN)
        swtitleframe.grid(row=0, column=0, padx=swbpadx, pady=swbpady)

        # Label containing the title of the window
        swtitle = self.lightboardtheme.themelabel(parent=swtitleframe, t="Settings", size="l")
        swtitle.config(bd=0, relief=FLAT)
        swtitle.grid(row=0, column=0)

        # Command which returns an error message and changes the colors of the fields where there
        # is an error present. Otherwise, the command returns an empty string.
        def errormessage():
            errormsg = ""  # A variable displaying the user's error message if invalid inputs have
            # Color of widget when user enters an valid input
            validinputcolor = self.lightboardtheme.themewidgetconfig.get("bg")
            # Color of widget when user enters an invalid input
            invalidinputcolor = self.lightboardtheme.themewidgetconfig.get("ebg")
            # been provided. If the error message has length zero, there are no errors.

            # Checks if user has provided a valid number of rows and adds to error message otherwise
            if smrowentry.get().isdigit():
                smrowentry.configure(bg=validinputcolor)
                self.num_rows = int(smrowentry.get())
            else:
                smrowentry.configure(bg=invalidinputcolor)
                errormsg = errormsg + "Invalid number of rows\n"
            # Checks if user has provided a valid number of columns and adds to error message otherwise
            if smcolentry.get().isdigit():
                smcolentry.configure(bg=validinputcolor)
                self.num_cols = int(smcolentry.get())
            else:
                smcolentry.configure(bg=invalidinputcolor)
                errormsg = errormsg + "Invalid number of columns\n"

            # Checks if user has provided a valid number of columns (which must also be prime)
            # and adds to error message otherwise
            if smstatesentry.get().isdigit():
                if isprime(int(smstatesentry.get())):
                    smstatesentry.configure(bg=validinputcolor)
                    self.num_states = int(smstatesentry.get())
                    self.field = PrimeField(self.num_states)
                    self.lightboardtheme = LightsOutTheme(self.num_states)
                else:
                    smstatesentry.configure(bg=invalidinputcolor)
                    errormsg = errormsg + "Number of states must be prime\n"
            else:
                smstatesentry.configure(bg=invalidinputcolor)
                errormsg = errormsg + "Invalid number of states\n"

            # Returns the error message
            return errormsg

        # Commands for buttons in settings window
        def editalllightrules():
            self.wishtoproceed = False
            errormsg = errormessage()
            if len(errormsg) == 0:
                copyrulewindow = CopyRuleWindow(master=self)
                copyrulewindow.grab_set()

            else:
                errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                errorwindow.grab_set()

        def editeachlightrule():
            self.wishtoproceed = False
            errormsg = errormessage()
            if len(errormsg) == 0:
                individualrulewindow = IndividualRuleWindow(master=self)
                individualrulewindow.grab_set()

            else:
                errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                errorwindow.grab_set()

        def changestartingboard():
            self.wishtoproceed = False
            errormsg = errormessage()
            if len(errormsg) == 0:
                setboardwindow = SetBoardWindow(master=self)
                setboardwindow.grab_set()

            else:
                errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                errorwindow.grab_set()

        def applydefaultrule():
            errormsg = errormessage()
            if len(errormsg) == 0:
                self.board_rule = LightBoardAttributes.defaultrule(self.num_rows, self.num_cols, self.field)
            else:
                errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                errorwindow.grab_set()

        def returntomenu():
            # If player decides to change states after changing rule, board and rule are reset to defaults.
            errormsg = errormessage()
            if (self.original_num_rows != self.num_rows or self.original_num_cols != self.num_cols) and self.wishtoproceed:
                self.board_rule = LightBoardAttributes.defaultrule(self.num_rows, self.num_cols, self.field)
                self.board_states = Matrix.const(self.num_rows, self.num_cols, self.field, self.num_states-1)
            # Warns player that states and rule will be changed to defaults
            else:
                warningwindow = WarningWindow(master=self,
                                              warningmsg="You have changed the number of rows and columns before specifying a new rule or board. Both will be set to defaults, would you still like to proceed?")
                warningwindow.grab_set()
            # If the error message is empty, a new light board will be created
            if len(errormsg) == 0:
                newlightboard = LightBoardAttributes(num_rows=self.num_rows,
                                                     num_cols=self.num_cols,
                                                     num_states=self.num_states,
                                                     board_states=self.board_states,
                                                     board_rule=LightBoardAttributes.switchrulefield(self.board_rule, PrimeField(self.num_states)))

                # Checks if new light board has a solution. If not, player is required to provide
                # different parameters
                if newlightboard.has_solution:
                    if self.original_num_states == self.num_states or not self.isrulemodified or self.wishtoproceed:
                        self.master.lightboarddata = newlightboard
                        self.master.lightboardtheme = self.lightboardtheme
                        self.destroy()
                        self.destroy()
                        self.master.deiconify()
                    else:
                        warningwindow = WarningWindow(master=self,
                                                      warningmsg="You have changed the number of states of the game after you changed the default rule which may lead to different results. Do you still wish to proceed?")
                        warningwindow.grab_set()
                else:
                    errormsg = "Board does not have solution!"
                    errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                    errorwindow.grab_set()
            else:
                errorwindow = ErrorWindow(master=self, errormsg=errormsg)
                errorwindow.grab_set()

        # Frame for settings window containing all widgets of the window
        swsettingsframe = Frame(self, bg=swbg, padx=swbpadx, pady=swbpady)
        swsettingsframe.grid(row=1, column=0)

        # Label stating that the entry to the right indicates the number of rows requested
        smrowlabel = self.lightboardtheme.themelabel(parent=swsettingsframe, t="Number of rows")
        smrowlabel.grid(row=0, column=0, padx=swwpadx, pady=swwpady)

        # Entry box allowing player to input the number of rows wanted
        smrowentry = self.lightboardtheme.themeentry(parent=swsettingsframe)
        smrowentry.insert(0,f"{self.master.lightboarddata.num_rows}")
        smrowentry.grid(row=0, column=1, padx=swwpadx, pady=swwpady)

        # Label stating that the entry to the right indicates the number of columns requested
        smcollabel = self.lightboardtheme.themelabel(parent=swsettingsframe, t="Number of columns")
        smcollabel.grid(row=1, column=0, padx=swwpadx, pady=swwpady)

        # Entry box allowing player to input the number of columns wanted
        smcolentry = self.lightboardtheme.themeentry(parent=swsettingsframe)
        smcolentry.insert(0, f"{self.master.lightboarddata.num_cols}")
        smcolentry.grid(row=1, column=1, padx=swwpadx, pady=swwpady)

        # Label stating that the entry to the right indicates the number of states requested
        smstateslabel = self.lightboardtheme.themelabel(parent=swsettingsframe, t="Number of states")
        smstateslabel.grid(row=2, column=0, padx=swwpadx, pady=swwpady)

        # Entry box allowing player to input the number of states wanted
        smstatesentry = self.lightboardtheme.themeentry(parent=swsettingsframe)
        smstatesentry.insert(0, f"{self.master.lightboarddata.num_states}")
        smstatesentry.grid(row=2, column=1, padx=swwpadx, pady=swwpady)

        # Button allowing player to edit the rule of the game by specifying a rule to be copied to all lights
        # via the default copy rule function.
        smeditallrulesbutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Edit all light rules", c=editalllightrules)
        smeditallrulesbutton.grid(row=3, column=0, padx=swwpadx, pady=swwpady)

        # Button allowing player to edit each light's rule individually
        smediteachrulebutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Edit each light rule", c=editeachlightrule)
        smediteachrulebutton.grid(row=3, column=1, padx=swwpadx, pady=swwpady)

        # Button allowing player to change the starting board
        smchangeboardbutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Change board", c=changestartingboard)
        smchangeboardbutton.grid(row=4, column=0, padx=swwpadx, pady=swwpady)

        # Button allowing player to apply default rule to board
        smediteachrulebutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Apply default rule", c=applydefaultrule)
        smediteachrulebutton.grid(row=4, column=1, padx=swwpadx, pady=swwpady)

        # Button saving player's settings and closing settings window
        smreturnbutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Return to menu", c=returntomenu)
        smreturnbutton.grid(row=5, column=0, padx=swwpadx, pady=swwpady)

        # Button allowing player to quit the game
        smquitbutton = self.lightboardtheme.themebutton(parent=swsettingsframe, t="Quit", c=quit)
        smquitbutton.grid(row=5, column=1, padx=swwpadx, pady=swwpady)

class ErrorWindow(tkinter.Toplevel):
    def __init__(self, master, errormsg):
        super().__init__(master)
        self.errormsg = errormsg

        # Config variables for readability
        errortheme = self.master.lightboardtheme
        ebg = errortheme.themebackgroundconfig.get("bg")
        ebpadx = errortheme.themebackgroundconfig.get("owpadx")
        ebpady = errortheme.themebackgroundconfig.get("pady")
        ewpadx = errortheme.themewidgetconfig.get("padx")
        ewpady = errortheme.themewidgetconfig.get("pady")

        self.config(bg=ebg)
        # Frame for error window containing the title of the window
        etitleframe = Frame(self, bg=ebg, bd=5, relief=SUNKEN)
        etitleframe.grid(row=0, column=0, padx=ebpadx, pady=ebpady)

        # Label containing the title of the window
        etitle = errortheme.themelabel(parent=etitleframe, t="Error!", size="l")
        etitle.config(bd=0, relief=FLAT)
        etitle.grid(row=0, column=0)

        # Frame containing the error message and exit button
        emessageframe = Frame(self, bg=ebg, padx=ebpadx, pady=ebpady)
        emessageframe.grid(row=1, column=0, sticky="EW")

        # Textbox containing the error message and exit button
        emessagetext = errortheme.themetextbox(parent=emessageframe)
        emessagetext.grid(row=0, column=0, pady=ewpady, sticky="NS")
        self.errormsg = "Your inputs have the following issues:\n\n" + self.errormsg
        emessagetext.insert(tkinter.END, self.errormsg)

        # Commands for buttons below:

        # Button allowing player to exit the error window
        emessagebutton = errortheme.themebutton(parent=emessageframe, t="Exit", c=lambda:self.destroy())
        emessagebutton.grid(row=1, column=0, pady=ewpady, sticky="NS")

class WarningWindow(tkinter.Toplevel):
    def __init__(self, master, warningmsg):
        super().__init__(master)
        self.warningmsg = warningmsg

        # Config variables for readability
        warningtheme = self.master.lightboardtheme
        wbg = warningtheme.themebackgroundconfig.get("bg")
        wbpadx = warningtheme.themebackgroundconfig.get("owpadx")
        wbpady = warningtheme.themebackgroundconfig.get("pady")
        wwpadx = warningtheme.themewidgetconfig.get("padx")
        wwpady = warningtheme.themewidgetconfig.get("pady")

        self.config(bg=wbg)
        # Frame for error window containing the title of the window
        wtitleframe = Frame(self, bg=wbg, bd=5, relief=SUNKEN)
        wtitleframe.grid(row=0, column=0, padx=wbpadx, pady=wbpady)

        # Label containing the title of the window
        wtitle = warningtheme.themelabel(parent=wtitleframe, t="Warning!", size="l")
        wtitle.config(bd=0, relief=FLAT)
        wtitle.grid(row=0, column=0)

        # Frame containing the error message and exit button
        wmessageframe = Frame(self, bg=wbg, padx=wbpadx, pady=wbpady)
        wmessageframe.grid(row=1, column=0, sticky="EW")

        # Textbox containing the error message and exit button
        wmessagetext = warningtheme.themetextbox(parent=wmessageframe)
        wmessagetext.grid(row=0, column=0, pady=wwpady, sticky="NS")
        wmessagetext.insert(tkinter.END, self.warningmsg)

        # Commands for buttons in Warning Window:
        def wishtoproceed():
            self.grab_release()
            self.destroy()
            self.master.wishtoproceed = True

        def wishnottoproceed():
            self.grab_release()
            self.destroy()
            self.master.wishtoproceed = False

        # Button allowing player to proceed without changing anything
        wyesbutton = warningtheme.themebutton(parent=wmessageframe, t="Yes", c=wishtoproceed)
        wyesbutton.grid(row=1, column=0, pady=wwpady, sticky="NS")

        # Button allowing player to change attributes before proceeding again
        wnobutton = warningtheme.themebutton(parent=wmessageframe, t="No", c=wishnottoproceed)
        wnobutton.grid(row=2, column=0, pady=wwpady, sticky="NS")

class GameWonWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Config variables for readability
        gamewontheme = self.master.lightboardtheme
        gwbg = gamewontheme.themebackgroundconfig.get("bg")
        gwbpadx = gamewontheme.themebackgroundconfig.get("owpadx")
        gwbpady = gamewontheme.themebackgroundconfig.get("pady")
        gwwpadx = gamewontheme.themewidgetconfig.get("padx")
        gwwpady = gamewontheme.themewidgetconfig.get("pady")

        self.config(bg=gwbg)
        # Frame for game won window
        gwtitleframe = Frame(self, bg=gwbg, bd=5, relief=SUNKEN)
        gwtitleframe.grid(row=0, column=0, padx=gwbpadx, pady=gwbpady)

        # Label containing the title of the window
        gwtitle = gamewontheme.themelabel(parent=gwtitleframe, t="You won!", size="l")
        gwtitle.config(bd=0, relief=FLAT)
        gwtitle.grid(row=0, column=0)

        # Frame containing the error message and exit button
        gwmessageframe = Frame(self, bg=gwbg, padx=gwbpadx, pady=gwbpady)
        gwmessageframe.grid(row=1, column=0, sticky="EW")

        # Textbox containing the error message and exit button
        gwmessagetext = gamewontheme.themetextbox(parent=gwmessageframe)
        gwmessagetext.grid(row=0, column=0, pady=gwwpady, sticky="NS")
        gwmessagetext.insert(tkinter.END, "You win! Would you like to retry with the same board, use a new random board or return to the main menu?")

        # Commands for buttons in Warning Window:
        def retry():
            self.grab_release()
            self.destroy()

        def randomizeboard():
            self.grab_release()
            self.destroy()

        def returntomenu():
            self.grab_release()
            self.master.destroy()
            self.master.master.deiconify()

        # Frame containing options for game won window
        gwbuttonsframe = Frame(self, bg=gwbg, padx=gwbpadx, pady=gwbpady)
        gwbuttonsframe.grid(row=2, column=0, sticky="EW")

        # Button allowing player to retry game with same board
        gwretrybutton = gamewontheme.themebutton(parent=gwbuttonsframe, t="Retry", c=retry)
        gwretrybutton.grid(row=0, column=0, pady=gwwpady, sticky="NS")

        # Button allowing player to play again with random board
        gwrandomizebutton = gamewontheme.themebutton(parent=gwbuttonsframe, t="Randomize Board", c=randomizeboard)
        gwrandomizebutton.grid(row=1, column=0, pady=gwwpady, sticky="NS")

        # Button allowing player to return to main menu
        gwrandomizebutton = gamewontheme.themebutton(parent=gwbuttonsframe, t="Return to menu", c=returntomenu)
        gwrandomizebutton.grid(row=2, column=0, pady=gwwpady, sticky="NS")

class CopyRuleWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        rows = 2*self.master.num_rows-1
        cols = 2*self.master.num_rows-1
        self.field = self.master.field
        self.lightboardtheme = self.master.lightboardtheme
        self.rulestates = Matrix.const(rows, cols, self.field, 0)

        # Config variables for readability
        crwbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        crwbpadx = self.lightboardtheme.themebackgroundconfig.get("owpadx")
        crwbpady = self.lightboardtheme.themebackgroundconfig.get("pady")
        crwwpadx = self.lightboardtheme.themewidgetconfig.get("padx")
        crwwpady = self.lightboardtheme.themewidgetconfig.get("pady")

        # Frame containing all the lights
        crwlightsframe = Frame(self, bg=crwbg, padx=crwbpadx, pady=crwbpady)
        crwlightsframe.grid(row=1, column=0, sticky="EW")

        # Creating the buttons for the settings lights grid
        crwlightgrid = []  # 2D List containing all the buttons
        for r in range(rows):
            crwlightgridrow = []  # 1D list containing a row of buttons
            for c in range(cols):
                crwlightgridrow.append(self.lightboardtheme.themelightbutton(parent=crwlightsframe,
                                                                             bg=self.lightboardtheme.lightcolors[self.rulestates.entries[r][c]]))
            crwlightgrid.append(crwlightgridrow)
        crwlightgrid[int((rows-1)/2)][int((cols-1)/2)].config(text="X")

        # Creating command for each button in settings lights grid
        def updatebuttonstate(r, c):
            def changerulestates():
                self.rulestates.entries[r][c] = self.field.add(self.rulestates.entries[r][c], 1)
                crwlightgrid[r][c].config(bg=self.lightboardtheme.lightcolors[self.rulestates.entries[r][c]])
            return changerulestates

        # Assigns command to each button and places each in the window
        for r in range(rows):
            for c in range(cols):
                crwlightgrid[r][c]["command"] = updatebuttonstate(r, c)
                crwlightgrid[r][c].grid(row=r, column=c)

        # Frame for settings menu:
        crwmenuframe = Frame(self, bg=crwbg, padx=crwbpadx, pady=crwbpady)
        crwmenuframe.grid(row=0, column=0, sticky="EW")

        # Creating command for closing with saving over old rule
        def saveandexit():
            self.master.isrulemodified = True
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.master.board_rule = LightBoardAttributes.copyrule(self.rulestates)
            self.destroy()

        # Creating command for exiting without saving over old rule.
        def exitwithoutsaving():
            self.master.isrulemodified = False
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.destroy()

        crwsaveandexitbutton = self.lightboardtheme.themebutton(parent=crwmenuframe,
                                                         t="Save and exit",
                                                         c=saveandexit)
        crwsaveandexitbutton.grid(row=0, column=0, padx=crwwpadx, pady=crwwpady)

        crwexitwithoutsavingbutton = self.lightboardtheme.themebutton(parent=crwmenuframe,
                                                                      t="Exit without saving",
                                                                      c=exitwithoutsaving)
        crwexitwithoutsavingbutton.grid(row=0, column=1, padx=crwwpadx, pady=crwwpady)

class IndividualRuleWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.num_rows = self.master.num_rows
        self.num_cols = self.master.num_cols
        self.field = self.master.field
        self.lightboardtheme = self.master.lightboardtheme
        self.board_rule = self.master.board_rule
        self.focusrow = 0  # row of element whose rule is being changed
        self.focuscolumn = 0 # column of element whose rule is being changed
        self.focusruleentry = None # current entry of rule being changed
        self.changedstates = Matrix.const(self.num_rows, self.num_cols, self.field, 0)

        # Config variables for readability
        irwbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        irwbpadx = self.lightboardtheme.themebackgroundconfig.get("owpadx")
        irwbpady = self.lightboardtheme.themebackgroundconfig.get("pady")
        irwwpadx = self.lightboardtheme.themewidgetconfig.get("padx")
        irwwpady = self.lightboardtheme.themewidgetconfig.get("pady")

        self.config(bg=irwbg)
        # Frame for header of window
        irwheaderframe = Frame(self, bg=irwbg, bd=5, relief=SUNKEN)
        irwheaderframe.grid(row=0, column=0, padx=irwbpadx, pady=irwbpady, sticky="EW")

        # Label containing the header of the window
        irwheader = self.lightboardtheme.themelabel(parent=irwheaderframe,
                                                   t="Select a button whose rule you wish to change",
                                                   size="l")
        irwheader.config(bd=0, relief=FLAT, width=40)
        irwheader.grid(row=0, column=0)

        # Frame containing all the lights
        irwlightsframe = Frame(self, bg=irwbg, padx=irwbpadx, pady=irwbpady)
        irwlightsframe.grid(row=1, column=0, sticky="NS")

        # Creating the buttons for the settings lights grid
        irwlightgrid = []  # 2D List containing all the buttons
        for r in range(self.num_rows):
            irwlightgridrow = []  # 1D list containing a row of buttons
            for c in range(self.num_cols):
                irwlightgridrow.append(self.lightboardtheme.themelightbutton(parent=irwlightsframe,
                                                                             bg=self.lightboardtheme.themewidgetconfig.get("bg")))
            irwlightgrid.append(irwlightgridrow)

        # Command to be given to each button when treated as an individual light
        def updatelightrulestate(r, c):
            def changelightrulestates():
                self.board_rule[self.focusrow][self.focuscolumn].entries[r][c] = self.field.add(self.board_rule[self.focusrow][self.focuscolumn].entries[r][c], 1)
                irwlightgrid[r][c].config(bg=self.lightboardtheme.lightcolors[self.board_rule[self.focusrow][self.focuscolumn].entries[r][c]])
            return changelightrulestates

        # Command to be given to each button when treated as a widget
        def updatelightwidgetstates(r, c):
            def changewidgetstates():
                self.focusrow = r
                self.focuscolumn = c
                for i in range(self.num_rows):
                    for j in range(self.num_cols):
                        irwlightgrid[i][j]["command"] = updatelightrulestate(i, j)
                        irwlightgrid[i][j].config(bg=self.lightboardtheme.lightcolors[self.board_rule[r][c].entries[i][j]],
                                                  text="")
                irwbackbutton.configure(state="active")
            return changewidgetstates

        # Assigning commands to each button
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                irwlightgrid[r][c]["command"] = updatelightwidgetstates(r,c)
                irwlightgrid[r][c].grid(row=r, column=c, sticky="NEWS")

        # Frame containing the menu of the window
        irwmenuframe = Frame(self, bg=irwbg, padx=irwbpadx, pady=irwbpady)
        irwmenuframe.grid(row=2, column=0, sticky="NS")

        # Commands for button in above frame
        def goback():
            self.changedstates.entries[self.focusrow][self.focuscolumn] = self.field.one()
            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    irwlightgrid[r][c]["command"] = updatelightwidgetstates(r, c)
                    irwlightgrid[r][c].config(bg=self.lightboardtheme.themewidgetconfig.get("bg"))
                    if self.changedstates.entries[r][c] == self.field.one():
                        irwlightgrid[r][c].config(text="X")
            irwbackbutton.configure(state="disabled")


        def saveandexit():
            self.master.isrulemodified = True
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.master.board_rule = self.board_rule
            self.destroy()

        def exitwithoutsaving():
            self.master.isrulemodified = False
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.destroy()

        # Button allowing player to switch to a different light
        irwbackbutton = self.lightboardtheme.themebutton(parent=irwmenuframe,
                                                         t="Go back",
                                                         c=goback)
        irwbackbutton.config(state="disabled")
        irwbackbutton.grid(row=0, column=0, padx=irwwpadx, pady=irwwpady)
        # Button allowing player to save his rule and go back to the menu
        irwsaveandquit = self.lightboardtheme.themebutton(parent=irwmenuframe,
                                                          t="Save and exit",
                                                          c=saveandexit)
        irwsaveandquit.grid(row=0, column=1, padx=irwwpadx, pady=irwwpady)

        # Button allowing player to discard his rule and continue with the original rule
        irwexitwithoutsaving = self.lightboardtheme.themebutton(parent=irwmenuframe,
                                                                t="Exit without saving",
                                                                c=exitwithoutsaving)
        irwexitwithoutsaving.grid(row=0, column=2, padx=irwwpadx, pady=irwwpady)

class SetBoardWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.num_rows = self.master.num_rows
        self.num_cols = self.master.num_cols
        self.num_states = self.master.num_states
        self.field = self.master.field
        self.lightboardtheme = self.master.lightboardtheme
        self.board_states = Matrix.const(self.num_rows, self.num_cols, self.field, self.num_states-1)

        # Config variables for readability
        sbwbg = self.lightboardtheme.themebackgroundconfig.get("bg")
        sbwbpadx = self.lightboardtheme.themebackgroundconfig.get("owpadx")
        sbwbpady = self.lightboardtheme.themebackgroundconfig.get("pady")
        sbwwpadx = self.lightboardtheme.themewidgetconfig.get("padx")
        sbwwpady = self.lightboardtheme.themewidgetconfig.get("pady")

        # Frame containing all the lights
        sbwlightsframe = Frame(self, bg=sbwbg, padx=sbwbpadx, pady=sbwbpady)
        sbwlightsframe.grid(row=0, column=0, sticky="EW")

        # Creating the buttons for the settings lights grid
        sbwlightgrid = []  # 2D List containing all the buttons
        for r in range(self.num_rows):
            sbwlightgridrow = []  # 1D list containing a row of buttons
            for c in range(self.num_cols):
                sbwlightgridrow.append(self.lightboardtheme.themelightbutton(parent=sbwlightsframe,
                                                                             bg=self.lightboardtheme.lightcolors[self.board_states.entries[r][c]]))
            sbwlightgrid.append(sbwlightgridrow)

        # Creating command for each button in settings lights grid
        def updatebuttonstate(r, c):
            def changerulestates():
                self.board_states.entries[r][c] = self.field.add(self.board_states.entries[r][c], 1)
                sbwlightgrid[r][c].config(bg=self.lightboardtheme.lightcolors[self.board_states.entries[r][c]])
            return changerulestates

        # Assigns command to each button and places each in the window
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                sbwlightgrid[r][c]["command"] = updatebuttonstate(r, c)
                sbwlightgrid[r][c].grid(row=r, column=c, sticky="EW")

        # Frame for settings menu:
        sbwmenuframe = Frame(self, bg=sbwbg, padx=sbwbpadx, pady=sbwbpady)
        sbwmenuframe.grid(row=1, column=0, sticky="EW")

        # Creating command for closing with saving over old rule
        def saveandexit():
            self.master.isrulemodified = True
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.master.board_states = self.board_states
            self.destroy()

        # Creating command for exiting without saving over old rule.
        def exitwithoutsaving():
            self.master.isrulemodified = False
            self.master.original_num_rows = self.master.num_rows
            self.master.original_num_cols = self.master.num_cols
            self.master.original_num_states = self.master.num_states
            self.destroy()

        sbwsaveandexitbutton = self.lightboardtheme.themebutton(parent=sbwmenuframe,
                                                         t="Save and exit",
                                                         c=saveandexit)
        sbwsaveandexitbutton.grid(row=0, column=0, padx=sbwwpadx, pady=sbwwpady)

        sbwexitwithoutsavingbutton = self.lightboardtheme.themebutton(parent=sbwmenuframe,
                                                                      t="Exit without saving",
                                                                      c=exitwithoutsaving)
        sbwexitwithoutsavingbutton.grid(row=0, column=1, padx=sbwwpadx, pady=sbwwpady)