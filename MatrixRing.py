class Matrix:
    def __init__(self, entries, field):
        self.rows = len(entries)
        self.cols = len(entries[0])
        self.field = field
        self.entries = []

        temprow = []

        for i in range(len(entries)):
            for j in range(len(entries[0])):
                temprow.append(field.identify(entries[i][j]))
            self.entries.append(temprow)
            temprow = []

    # Instance Methods
    def identify(self, f):  # Changes the field of a matrix via identification. Right now, this works best for matrices
        # between two prime fields
        if self.field.type != f.type:
            for r in range(len(self.entries)):
                for c in range(len(self.entries[0])):
                    self.entries[r][c] = f.identify(self.entries[r][c])
            self.field = f
        
    # Elementary Row Operations

    def switchrows(self, i, j):  # Switches row i and row j
        temp = self.entries[i]
        self.entries[i] = self.entries[j]
        self.entries[j] = temp

    def addrow(self, i, j, c):  # Adds c times row i to row j:
        for k in range(len(self.entries[0])):
            self.entries[j][k] = self.field.add(self.field.multiply(self.entries[i][k], c), self.entries[j][k])

    def multiplyrow(self, i, c):  # Multiplies row i by c
        for j in range(len(self.entries[0])):
            self.entries[i][j] = self.field.multiply(self.entries[i][j], c)

    # Important Methods

    @staticmethod
    def RREF(m, s):  # Returns a matrix with entries in reduced row echelon form.
        # via Gauss-Jordan Elimination
        m1 = Matrix(m.entries, m.field)
        numpivots = 0  # Variable declaring the number of pivots that have been found.
        ispivotcol = False  # Boolean variable telling if a specific column is a pivot column or not.
        pivotrow = 0  # integer representing the row of the pivot found
        for c in range(0, s):
            ispivotcol = False  # Resets conditional pivot column variable to False.
            for r in range(numpivots, m1.rows):  # Loop used to find a nonzero element in column i
                if m1.entries[r][c] != m1.field.zero():  # Checks if a nonzero element in column is found
                    numpivots += 1  # Increases number of pivots by 1
                    ispivotcol = True  # Indicates that current column is a pivot column
                    pivotrow = r  # Sets placeholder of current row to be switched later
                    break
            # If no nonzero elements are found, we proceed to the next column with no changes.
            if ispivotcol:  # Checks whether current column is a pivot column or not
                m1.switchrows(numpivots-1, pivotrow)  # moves pivot row to correct location
                # changes first element of row to 1
                m1.multiplyrow(numpivots-1, m1.field.multinv(m1.entries[numpivots-1][c]))
                for r1 in range(0, m.rows):  # Loops through column to remove nonzero elements
                    # Checks for other nonzero elements in pivot column
                    if m1.entries[r1][c] != m1.field.zero() and r1 != numpivots-1:
                        # Removes other nonzero elements in pivot column
                        m1.addrow(numpivots-1, r1, m1.field.addinv(m1.entries[r1][c]))
        return m1

    @staticmethod
    def det(m):  # Returns the determinant of a matrix if it is square and None otherwise.
        # Code is copied from above method except with variable
        if m.rows != m.cols:
            return None
        m1 = Matrix(m.entries, m.field)
        numpivots = 0
        ispivotcol = False
        pivotrow = 0
        determinant = m1.field.one()  # determinant variable that is calculated through row reduction
        for c in range(0, m1.cols):
            ispivotcol = False
            for r in range(numpivots, m1.rows):
                if m1.entries[r][c] != m1.field.zero():
                    numpivots += 1
                    ispivotcol = True
                    pivotrow = r
                    break
            if ispivotcol:
                determinant = m1.field.multiply(determinant, m1.entries[pivotrow][c])
                m1.switchrows(numpivots - 1, pivotrow)
                m1.multiplyrow(numpivots - 1, m1.field.multinv(m1.entries[numpivots - 1][c]))
                for r1 in range(0, m1.rows):
                    if m1.entries[r1][c] != m1.field.zero() and r1 != numpivots - 1:
                        m1.addrow(numpivots - 1, r1, m1.field.addinv(m1.entries[r1][c]))

        if numpivots == m1.cols:  # If the number of pivots is the same as the number of the number
            # of columns, the RREF of the given matrix is the identity and the determinant is as we
            # found through row reduction
            return determinant
        else:  # In this case, there is a zero row so, the determinant is zero.
            return m.field.zero()

    @staticmethod
    def equals(m1, m2):  # Returns whether two matrices are equal
        return (m1.entries == m2.entries) and (m1.field.type() == m2.field.type())
    
    @staticmethod
    def add(m1, m2):  # Adds matrices m1 and m2
        # Checks if matrices have different dimensions or different fields in which case, None is returned
        if m1.rows != m2.rows or m1.cols != m2.cols or m1.field.type() != m2.field.type():
            # in which case, no matrix is returned
            return None
        m3row = []  # Row of m1+m2
        m3entries = []  # Matrix m1+m2 to be returned.
        for r in range(m1.rows):
            for c in range(m1.cols):
                # Adds corresponding entries of m1 and m2 and appends the result to m3row.
                m3row.append(m1.field.add(m1.entries[r][c], m2.entries[r][c]))
            m3entries.append(m3row)
            m3row = []
        return Matrix(m3entries, m1.field)

    @staticmethod
    def scale(m, s):  # Multiplies a matrix m by s and returns the result
        m1 = Matrix(m.entries, m.field)
        if m1.field.identify(s) == m1.field.one():
            return m
        s1 = m1.field.identify(s)
        for r in range(m1.rows):
            for c in range(m1.cols):
                m1.entries[r][c] = m1.field.multiply(m1.entries[r][c], s1)
        return m1


    @staticmethod
    def transpose(m):  # Inputs a matrix m and returns a matrix which is its transpose.
        tentries = []
        trow = []
        for c in range(m.cols):
            for r in range(m.rows):
                trow.append(m.entries[r][c])
            tentries.append(trow)
            trow = []
        return Matrix(tentries, m.field)

    @staticmethod
    def submatrix(m, rs, cs, rf, cf):  # Returns the sub-matrix formed between rows rs and rf
        # and columns cs, cf both inclusive
        if rs < 1 or cs < 1 or rf > m.rows or cf > m.cols or cf < cs or rf < rs:
            return None
        srow = []
        sentries = []
        for r in range(rs-1, rf):
            for c in range(cs-1, cf):
                srow.append(m.entries[r][c])
            sentries.append(srow)
            srow = []
        return Matrix(sentries, m.field)

    @staticmethod
    def hjoin(m1, m2):  # Returns the block matrix [m1, m2] if m1 and m2 have the same number of
        # rows and field and None otherwise.
        if m1.rows != m2.rows or m1.field.type() != m2.field.type():
            return None
        hjentries = []
        hjrow = []
        for r in range(m1.rows):
            for c in range(m1.cols):
                hjrow.append(m1.entries[r][c])
            for c in range(m2.cols):
                hjrow.append(m2.entries[r][c])
            hjentries.append(hjrow)
            hjrow = []
        return Matrix(hjentries, m1.field)

    @staticmethod
    def vjoin(m1, m2):  # Returns the block matrix [[m1], [m2]] if m1 and m2 have the same number of
        # columns and field and None otherwise.
        if m1.cols != m2.cols or m1.field.type() != m2.field.type():
            return None
        vjentries = []
        for r in range(m1.rows):
            vjentries.append(m1.entries[r])
        for r in range(m2.rows):
            vjentries.append(m2.entries[r])
        return Matrix(vjentries, m1.field)

    @staticmethod
    def matrixtorowvector(m):  # Matrix returned by joining all the rows of the given matrix m
        rowentries = []  # Variable containing entries of row vector to be returned
        for r in range(m.rows):
            for c in range(m.cols):
                rowentries.append(m.entries[r][c])
        return Matrix([rowentries], m.field)

    @staticmethod
    def matrixtocolvector(m):  # Matrix returned by joining all the columns of the given matrix m
        colentries = []  # Variable containing entries of column vector to be returned
        for c in range (m.cols):
            for r in range (m.rows):
                colentries.append([m.entries[r][c]])
        return  Matrix(colentries, m.field)

    @staticmethod
    def rowvectortomatrix(rv, r, c):  # Changes a row vector into an r by c by joining sections
        # of c consecutive terms of rv
        if r * c != len(rv.entries) or rv.rows != 1:  # Checks if cv is a column vector with r*c entries
            return None
        matrixentries = []
        matrixrowentries = []
        for i in range(r):
            for j in range(c):
                matrixrowentries.append(cv.entries[0][i*r+j])
            matrixentries.append(matrixrowentries)
            matrixrowentries = []
        return Matrix(matrixentries, rv.field)

    @staticmethod
    def colvectortomatrix(cv, r, c):  # Changes a column vector into an r by c by joining sections
        # of r consecutive terms of cv
        if r*c != len(cv.entries) or cv.cols != 1:  # Checks if cv is a column vector with r*c entries
            return None
        matrixentries = []
        matrixrowentries = []
        for i in range(r):
            for j in range(c):
                matrixrowentries.append(cv.entries[r*j+i][0])
            matrixentries.append(matrixrowentries)
            matrixrowentries = []
        return Matrix(matrixentries, cv.field)
        
    @staticmethod
    def pivotcols(m):  # Inputs a matrix m, reduces it to RREF and outputs a list of all columns
        # which are pivot columns
        m1 = Matrix.RREF(m, m.cols)
        pivotcollist = []
        currentrow = 0  # Index of row being examined. As soon as a pivot is found, current row
        # is incremented and we continue searching for pivots.
        for c in range(m1.cols):
            if m1.entries[currentrow][c] == m1.field.one():  # Checks if a pivot was found
                pivotcollist.append(c)  # Adds column index to list of pivot columns
                currentrow += 1  # Move to next row
            if currentrow >= m1.rows:  # This happens when all pivots have been found and, we must
                # leave the loop
                break
        return pivotcollist

    @staticmethod
    def freecols(m): # Inputs a matrix m, reduces it to RREF and outputs a list of all columns
        # which are not pivot columns.
        m1 = Matrix.RREF(m, m.cols)
        freecollist = []
        currentrow = 0  # Index of row being examined. As soon as a pivot is found, current row
        # is incremented and we continue searching for pivots.
        for c in range(m.cols):
            if m.entries[currentrow][c] == m.field.one():  # Checks if a pivot has been found
                currentrow += 1  # Move to next row without modifying
            else: # In this case, the column is not a pivot column, and we add the column index
                # to the list of free columns.
                freecollist.append(c)
            if currentrow >= m.rows:  # This happens when all pivots have been found and, we must
                # leave the loop
                break
        return freecollist

    @staticmethod
    def numzerorows(m):  # Inputs a matrix m and outputs the number of zero rows it has. This
        # method is primarily used for those matrices already in RREF
        zerorows = 0
        iszerorow = True
        for r in range(m.rows):
            iszerorow = True
            for c in range(m.cols):
                if m.entries[r][c] != m.field.zero():
                    iszerorow = False
                    break
            if iszerorow:
                zerorows += 1
        return zerorows

    @staticmethod
    def solve(A, b):  # Solves a system Ax = b for a matrix A, a column vector b and a vector of
        # variables x via row reducing (A | tp(b)). If there is more than one solution, the
        # method outputs one of the solutions by setting all free variables to zero. If on
        # the other hand, there are no solutions, the method outputs None
        pivotList = Matrix.pivotcols(A)  # List of all locations of pivots in A
        numFreeVariables = A.cols-len(pivotList)
        if A.rows != b.rows:  # Checks for incorrect number of inputs
            return None
        # Reduced augmented matrix for system
        sysmatrix = Matrix.RREF(Matrix.hjoin(A, b), A.cols)
        # Searches for 0 = 1 equations in reduced system matrix
        for i in range(b.rows-numFreeVariables, b.rows):
            if sysmatrix.entries[i][sysmatrix.cols-1] != sysmatrix.field.zero():
                return None
        # If we cleared the for loop, the solution has at least one solution
        sol = []  # solution of system that will be returned.
        for i in range(A.cols):  # Initialize a list with as many terms as there are columns in A
            sol.append([sysmatrix.field.zero()])
        # Assigns values to each pivot variable assuming each free variable is zero. In this
        # case, the value of the ith pivot variable is the value of the ith element
        for i in range(len(pivotList)):
            sol[pivotList[i]][0] = sysmatrix.entries[i][sysmatrix.cols-1]
        return Matrix(sol, sysmatrix.field)

    @staticmethod
    def const(r, c, f, const):  # Returns the zero matrix with r rows and c columns for the field f
        const = f.identify(const)
        crow = []
        centries = []
        for r1 in range(r):
            for c1 in range(c):
                crow.append(const)
            centries.append(crow)
            crow = []
        return Matrix(centries, f)

    @staticmethod
    def identity(n, f):  # Returns the n by n identity matrix for the field f
        idrow = []
        identries = []
        for r in range(n):
            for c in range(n):
                if r == c:
                    idrow.append(f.one())
                else:
                    idrow.append(f.zero())
            identries.append(idrow)
            idrow = []
        return Matrix(identries, f)

    # Methods used for testing and analysis

    @staticmethod
    def randommatrix(r, c, n, f):  # Generates a random matrix with r rows, c columns and with entries
        # from 1 through n in the field f
        rentries = []
        row = []
        for i in range(r):
            for j in range(c):
                row.append(random.randint(0, n))
            rentries.append(row)
            row = []
        return Matrix(rentries, f)

    def printentries(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{self.field.tostring(self.entries[i][j])}, ", end="")
            print()