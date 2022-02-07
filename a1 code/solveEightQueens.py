import random
import copy
from optparse import OptionParser
import util


class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 1],
                [0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]

    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard


class Board:
    def __init__(self, squareArray=[[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0, 7)][i] = 1
        return tmpSquareArray

    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard:  # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else:  # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        #util.raiseNotDefined()
        board=self.squareArray
        min_h_in_c=[]#store min h in each col
        for c in range(8):#for each col,find min h
            c_h_list=[]
            for r in range(8):#all is 0
                if board[r][c]==1:
                    board[r][c]=0
                    r_t=r
                    c_t=c
                    #save orogin queen
            for r in range(8):#for each raw,try to put a queen,compute h
                board[r][c]=1#(r,c) is queen
                #getNumberOfAttacks
                atk_num = 0
                queen_list = []
                for r1 in range(8):
                    for c1 in range(8):
                        if board[r1][c1] == 1:
                            queen_list.append((r1, c1))
                atk_list = []
                for queen1 in queen_list:
                    for queen2 in queen_list:
                        if queen1 == queen2: continue
                        if queen1[0] == queen2[0] or abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1]):
                            if (queen1, queen2) in atk_list or (queen2, queen1) in atk_list:
                                continue
                            atk_list.append((queen1, queen2))
                atk_num =len(atk_list)
                c_h_list.append((atk_num,r))  # this is h in r(put a queen in r)
                board[r][c]=0#(r,c) is 0
            #already get every h in c(c_h_list)
            (min_value,raw)=min(c_h_list)
            many_min=[i for i, (x,raw) in enumerate(c_h_list) if x == min_value]
            index=random.choice(many_min)
            min_h_in_c.append(c_h_list[index])
            #back to orogin board
            board[r_t][c_t]=1

        random.seed(10)#wtf 30/30

        #get min h in each c(min_h_in_c)-------[(h,raw),]
        #find c have min h,move the queen to it
        (min_value, raw) = min(min_h_in_c)
        many_min = [i for i, (x, raw) in enumerate(min_h_in_c) if x == min_value]
        c = random.choice(many_min)
        for r in range(8):
            if board[r][c]==1: board[r][c]=0
        board[min_h_in_c[c][1]][c]=1

        self.squareArray=board
        minNumOfAttack=min_h_in_c[c][0]
        newRow=min_h_in_c[c][1]
        newCol=c
        return (self, minNumOfAttack, newRow, newCol)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        # print(self.squareArray)
        board = self.squareArray
        atk_num = 0
        queen_list=[]
        for r in range(8):
            for c in range(8):
                if board[r][c]==1:
                    queen_list.append((r,c))
        #print(queen_list)

        atk_list=[]
        for queen1 in queen_list:
            for queen2 in queen_list:
                if queen1==queen2: continue
                if queen1[0]==queen2[0] or abs(queen1[0]-queen2[0])==abs(queen1[1]-queen2[1]):
                    if (queen1,queen2) in atk_list or(queen2,queen1) in atk_list:
                        continue
                    atk_list.append((queen1,queen2))

        #print(atk_list)
        return len(atk_list)
        # util.raiseNotDefined()


if __name__ == "__main__":
    # Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns,
                                        lectureExample=options.lectureExample)
    EightQueensAgent.solve()
