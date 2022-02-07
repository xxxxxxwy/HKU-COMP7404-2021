#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util
import sys
import random
import time
from optparse import OptionParser


class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """

    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                       [False, False, False, False, False, False, False, False, False],
                       [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append(chr(b + ASCII_OF_A) + str(i))
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]:
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)


class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """

    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """

        # my code here
        '''
        0 1 2
        3 4 5
        6 7 8
        '''

        self.fp_dict = {
            '1': [
                [0],
                [1],
                [0, 1, 2],
                [0, 4, 8],
                [0, 5, 7],
                [1, 4, 7],
                [0, 1, 2, 3],
                [0, 1, 2, 4],
                [0, 1, 2, 6],
                [0, 1, 2, 7],
                [0, 1, 4, 7],
                [0, 1, 4, 8],
                [0, 2, 4, 6],
                [1, 3, 4, 5],
                [0, 1, 2, 3, 4],
                [0, 1, 2, 3, 5],
                [0, 1, 2, 3, 6],
                [0, 1, 4, 5, 7],
                [0, 1, 4, 5, 8],
                [0, 1, 4, 6, 7],
                [0, 1, 4, 6, 8],
                [0, 1, 4, 7, 8],
                [0, 2, 4, 6, 8],
                [1, 3, 4, 5, 7],
                [0, 1, 2, 3, 4, 5],
                [0, 1, 2, 3, 4, 6],
                [0, 1, 2, 3, 4, 7],
                [0, 1, 2, 3, 4, 8],
                [0, 1, 2, 3, 5, 6],
                [0, 1, 2, 3, 5, 7],
                [0, 1, 2, 3, 6, 8],
                [0, 1, 2, 3, 7, 8],
                [0, 1, 2, 4, 6, 7],
                [0, 1, 2, 4, 6, 8],
                [0, 1, 2, 6, 7, 8],
                [0, 1, 3, 4, 5, 8],
                [0, 1, 4, 5, 6, 7],
                [0, 1, 4, 5, 6, 8],
                [0, 1, 2, 3, 4, 5, 6],
                [0, 1, 2, 3, 4, 5, 7],
                [0, 1, 2, 3, 4, 6, 8],
                [0, 1, 2, 3, 4, 7, 8],
                [0, 1, 2, 3, 5, 6, 7],
                [0, 1, 2, 3, 5, 6, 8],
                [0, 1, 2, 4, 6, 7, 8],
                [0, 1, 3, 4, 5, 7, 8],
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0, 1, 2, 3, 4, 5, 6, 8],
                [0, 1, 2, 3, 5, 6, 7, 8],
                [0, 1, 2, 3, 4, 5, 6, 7, 8]
            ],
            'a': [
                [0, 8],
                [1, 3],
                [1, 7],
                [0, 1, 6],
                [0, 2, 4],
                [0, 2, 7],
                [0, 4, 5],
                [0, 1, 3, 4],
                [0, 1, 3, 5],
                [0, 1, 3, 8],
                [0, 1, 7, 8],
                [0, 2, 6, 8],
                [1, 3, 5, 7],
                [0, 1, 4, 5, 6],
                [0, 1, 5, 6, 7],
                [0, 1, 5, 6, 8],
                [0, 1, 3, 5, 7, 8]
            ],
            'b': [
                [0, 2],
                [0, 4],
                [0, 5],
                [1, 4],
                [0, 1, 3],
                [1, 3, 5],
                [0, 1, 4, 5],
                [0, 1, 4, 6],
                [0, 1, 5, 6],
                [0, 1, 6, 7],
                [0, 1, 6, 8],
                [0, 2, 4, 7],
                [0, 4, 5, 7],
                [0, 1, 3, 5, 8],
                [0, 1, 3, 5, 7]
            ],
            'c': [
                []
            ],
            'd': [
                [0, 1, 5],
                [0, 1, 7],
                [0, 1, 8]
            ],
            'cc': [
                [4]
            ],
            'ad': [
                [0, 1]
            ],
            'ab': [
                [0, 1, 4],
                [0, 2, 6],
                [1, 3, 4],
                [0, 1, 5, 7],
                [0, 1, 5, 8]
            ]
        }

        self.goal_fp_list = ['cc', 'a', 'bb', 'bc', 'cb']

    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            # check every row
            row = i * 3
            if board[row] and board[row + 1] and board[row + 2]:
                return True
            # check every column
            if board[i] and board[i + 3] and board[i + 6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

    # my code here
    def get_fp_key(self, board):
        # board: [true, false,true.......]
        for key in self.fp_dict:
            # get every board value for this key
            fp_value_list = self.fp_dict[key]
            for fp_value in fp_value_list:
                # check each board value
                for i in range(0, 4):
                    # check rotate
                    for j in range(0, 2):
                        # check reflect

                        board_value_arr = []
                        for index, value in enumerate(board):
                            if value == True:
                                board_value_arr.append(index)
                        # transform b to fp_value
                        if board_value_arr == fp_value:
                            return key

                        # reflect this board
                        b = board.copy()
                        b[0] = board[2]
                        b[2] = board[0]
                        b[3] = board[5]
                        b[5] = board[3]
                        b[8] = board[6]
                        b[6] = board[8]
                        board = b

                    # rotate this board
                    b = board.copy()
                    b[0] = board[6]
                    b[1] = board[3]
                    b[2] = board[0]
                    b[3] = board[7]
                    # b[4] = board[4]
                    b[5] = board[1]
                    b[6] = board[8]
                    b[7] = board[5]
                    b[8] = board[2]
                    board = b


class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """

    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    # my code here
    def getAction(self, gameState, gameRules):

        action_list = gameState.getLegalActions(gameRules)
        # print(action_list)
        action_value = []

        for action in action_list:
            action_state = gameState.generateSuccessor(action)

            value = self.get_value(action_state, gameRules)
            action_value.append(value)
        # already get action-value list

        max_value_action_list = []

        for index, value in enumerate(action_value):
            if value == max(action_value):
                max_value_action_list.append(action_list[index])

        action = random.choice(max_value_action_list)

        return action

    # my code here
    def get_value(self, gameState, gameRules):

        board_fp = []
        for board in gameState.boards:
            if gameRules.deadTest(board):
                continue
            board_fp.append(gameRules.get_fp_key(board))
        # already get every board fp key

        # cc a bb bc cb
        result = ''
        for fp in board_fp:
            if fp == '1':
                continue
            result += fp

        if result in gameRules.goal_fp_list:
            return 1

        return 0


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """

    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """

    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action


class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """

    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames = numOfGames
        self.muteOutput = muteOutput
        self.maxTimeOut = 30

        self.AIforHuman = AIforHuman
        self.gameRules = GameRules()
        self.AIPlayer = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0  # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0:
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (
                            agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i + 1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i + 1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    # random.seed(1)
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
