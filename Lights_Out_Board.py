from PrimeField import *
from MatrixRing import *
import random

class LightBoardAttributes:
    def __init__(self, num_rows=10,
                 num_cols=10,
                 num_states=2,
                 board_states=None,
                 board_rule=None,
                 board_solution=None,
                 has_solution=False,
                 expandable_rule=True):
        self.num_rows = num_rows  # Number of rows in a board
        self.num_cols = num_cols  # Number of columns in a board
        self.num_states = num_states  # Number of states of a board
        self.field = PrimeField(num_states)  # Field for entries of board_states, board_rule
        # States of board modulo num_states as a matrix with dimensions num_rows, num_cols
        if board_states is None:
            self.board_states = Matrix.const(self.num_rows, self.num_cols, PrimeField(self.num_states), self.num_states-1)
        else:
            self.board_states = board_states
        self.original_board_states = self.board_states  # States of board before player changes them
        if board_rule is None:
            self.board_rule = LightBoardAttributes.defaultrule(self.num_rows, self.num_cols, self.field)
        else:
            self.board_rule = board_rule  # Rule of board modulo num_states
        self.board_solution = board_solution  # Solution of lights out board. The solution will be updated
        # later depending on if a solution can be found or not
        if self.board_solution is not None:
            # Original board solution before player has modified it
            self.original_board_solution = Matrix(self.board_solution.entries, self.field)
        else:
            self.original_board_solution = None
        self.has_solution = has_solution # Variable checking if a board has a solution or not
        self.show_solution = False # Indicates whether player wishes to see solution or not. By
        # default, this is set to false
        self.num_moves = 0  # Variable indicating the number of moves the player has performed.
        self.expandable_rule = False  # Indicates if a rule can be interpolated to other
        # squares when dimensions of board are changed.
        self.updatesol()  # Updates solution if one has not been specified.

    def statestocolvector(self): # Returns the states of the lights out board as a column vector
        return Matrix.matrixtocolvector(self.board_states)

    def ruletomatrix(self):  # Returns the rule as a single matrix
        rulematrix = []
        for c in range(len(self.board_rule[0])):
            for r in range(len(self.board_rule)):
                if r == 0 and c == 0:  # For the first term, convert the matrix in the upper left
                    # corner of rule to a column vector
                    rulematrix = Matrix.matrixtocolvector(self.board_rule[0][0])
                # For the rest of the terms, repeatedly join together entries of rule proceeding
                # down the columns first and then to the right after converting them to column
                # vectors.
                else:
                    rulematrix = Matrix.hjoin(rulematrix, Matrix.matrixtocolvector(self.board_rule[r][c]))
        return rulematrix

    def updatesol(self):  # Updates the solution for a lights out board once the other attributes
        # have been initialized. It also updates the has_solution variable to True if a solution
        # was found and keeps it as false otherwise.
        # Uses Gaussian elimination to find a solution if one has not already been specified.
        if not self.has_solution:
            board_sol = Matrix.solve(self.ruletomatrix(), self.statestocolvector())
            if board_sol is not None:
                board_sol = Matrix.colvectortomatrix(board_sol, self.num_rows, self.num_cols)
                self.has_solution = True
                self.board_solution = Matrix.scale(board_sol, -1)
                self.original_board_solution = Matrix(board_sol.entries, self.field)
    
    @staticmethod
    def copyrule(ruletocopy):  # If there are m rows and n columns, ruletocopy is a 2m-1 x 2n-1 matrix of
        # elements of the finite field F_p where p is the number of states. To form the rule R for the lights out
        # board, the i, j entry of R is the submatrix of r ending at (2m-2-i, 2n-2-j) and starting at
        # (m-1-i, n-1-j).
        m = int((len(ruletocopy.entries) + 1) / 2)  # Variable representing the number of rows of the returned rule
        n = int((len(ruletocopy.entries[0]) + 1) / 2)  # Variable representing the number of columns of the returned rule
        rule = []  # Rule we wish to return
        rowrule = []  # A temporary placeholder which collects all matrices in a row of rule
        # Creates the rule
        for r in range(m):
            for c in range(n):
                # Adding rule at light with indices (r,c) to rowrule.
                rowrule.append(Matrix.submatrix(ruletocopy, m-r, n-c, 2*m-1-r, 2*n-1-c))
            rule.append(rowrule)  # Adding rowrule to rule
            rowrule = []
        return rule  # Returns the required rule

    @staticmethod
    def defaultrule(m, n, f):  # Returns the default rule when there are m rows and n columns
        m1 = 2*m-1
        n1 = 2*n-1
        defruletocopyrow = []  # A row of the rule which will be copied to all lights
        defruletocopyentries = []  # The rule which will be copied to all lights
        for r in range(m1):
            for c in range(n1):
                # These are the locations of the three, four, or five lights whose states will be changed
                if ([r, c] == [m-2, n-1] or [r, c] == [m-1, n-2] or [r, c] == [m-1, n-1] 
                        or [r, c] == [m, n-1] or [r, c] == [m - 1, n]):
                    defruletocopyrow.append(1)
                else:
                    defruletocopyrow.append(0)
            defruletocopyentries.append(defruletocopyrow)
            defruletocopyrow = []
        defruletocopy = Matrix(defruletocopyentries, f)  # Creates matrix which will be
        # copied to create the default rule
        defrule = LightBoardAttributes.copyrule(defruletocopy)  # Creates the default rule to be returned.
        return defrule
        
    def randomizestates(self):
        self.board_states = Matrix.const(self.num_rows, self.num_cols, self.field, 0)
        self.board_solution = Matrix.const(self.num_rows, self.num_cols, self.field, 0)
        r = 0
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                r = random.randint(0, self.num_states-1)
                self.board_solution.entries[i][j] = self.field.addinv(r)
                if r != 0:
                    self.board_states = Matrix.add(self.board_states, Matrix.scale(self.board_rule[i][j], r))
        self.original_board_states = Matrix(self.board_states.entries, self.field)
        self.original_board_solution = Matrix(self.board_solution.entries, self.field)
        
    @staticmethod
    def switchrulefield(rule, f):  # Switches field of rule via identification
        if rule[0][0].field.type() == f.type():
            return rule
        else:
            for r in range(len(rule)):
                for c in range(len(rule[0])):
                    rule[r][c].identify(f)
            return rule