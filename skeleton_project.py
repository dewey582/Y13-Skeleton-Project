
#Skeleton Program code for the AQA A Level Paper 1 Summer 2023 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

## possible questions
## 1.make the game not crash when incorrent inputs are given
## 2.display what each move does in the console
## 3.
## 4.
## 5.
##
##
##

import random

class Dastan:
    ## initilises all the variables needed to run the code
    ##R = row   C = column
    def __init__(self, R, C, NoOfPieces):
        self._Board = []
        ## array to store the current board layout
        self._Players = []
        self._MoveOptionOffer = []
        ##array for current move options 1,2,3
        self._Players.append(Player("Player One", 1))
        self._Players.append(Player("Player Two", -1))
        self.__CreateMoveOptions()

        self._NoOfRows = R
        self._NoOfColumns = C
        ##data about the board
        self._MoveOptionOfferPosition = 0
        self.__CreateMoveOptionOffer()
        self.__CreateBoard()
        self.__CreatePieces(NoOfPieces)
        self._CurrentPlayer = self._Players[0]
        ## hold which players turn it is 1,2

## print out board into console using ascii via multiple functions repeated at start of every turn
    def __DisplayBoard(self):
        print("\n" + "   ", end="")
        ##prints columns
        for Column in range(1, self._NoOfColumns + 1):
            print(str(Column) + "  ", end="")
            
        print("\n" + "  ", end="")
        for Count in range(1, self._NoOfColumns + 1):
            print("---", end="")
            
        print("-")
        ##print rows
        for Row in range(1, self._NoOfRows + 1):
            print(str(Row) + " ", end="")
            
            for Column in range(1, self._NoOfColumns + 1):
                Index = self.__GetIndexOfSquare(Row * 10 + Column)
                print("|" + self._Board[Index].GetSymbol(), end="")
                ##checks is there is a peice in each squre if not prints a blank
                PieceInSquare = self._Board[Index].GetPieceInSquare()
                if PieceInSquare is None:
                    print(" ", end="")    
                else:
                    print(PieceInSquare.GetSymbol(), end="")   
            print("|") 
        print("  -", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print("---", end="")    
        print()
        print()

    def __DisplayState(self):
        ##prints board
        self.__DisplayBoard()
        ##gives the move option to player
        print("Move option offer: " + self._MoveOptionOffer[self._MoveOptionOfferPosition])
        print()
        ##gives the player info of current player 
        print(self._CurrentPlayer.GetPlayerStateAsString())
        ##states which players turn it is
        print("Turn: " + self._CurrentPlayer.GetName())
        print()

    def __GetIndexOfSquare(self, SquareReference):
        ##uses player inupt to get the row and column from 1 number
        Row = SquareReference // 10
        Col = SquareReference % 10
        return (Row - 1) * self._NoOfColumns + (Col - 1)


    def __CheckSquareInBounds(self, SquareReference):
        ##checks to see if the chosen square is within the board
        Row = SquareReference // 10
        Col = SquareReference % 10
        if Row < 1 or Row > self._NoOfRows:
            return False
        elif Col < 1 or Col > self._NoOfColumns:
            return False
        else:
            return True

    ##runs other check square functions
    def __CheckSquareIsValid(self, SquareReference, StartSquare):
        if not self.__CheckSquareInBounds(SquareReference):
            return False
        PieceInSquare = self._Board[self.__GetIndexOfSquare(SquareReference)].GetPieceInSquare()
        if PieceInSquare is None:
            if StartSquare:
                return False
            else:
                return True
        elif self._CurrentPlayer.SameAs(PieceInSquare.GetBelongsTo()):
            if StartSquare:
                return True
            else:
                return False
        else:
            if StartSquare:
                return False
            else:
                return True

    ##checks if the conditions for game over is fufilled
    def __CheckIfGameOver(self):
        Player1HasMirza = False
        Player2HasMirza = False
        for S in self._Board:
            PieceInSquare = S.GetPieceInSquare()
            if PieceInSquare is not None:
                if S.ContainsKotla() and PieceInSquare.GetTypeOfPiece() == "mirza" and not PieceInSquare.GetBelongsTo().SameAs(S.GetBelongsTo()):
                    return True
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[0]):
                    Player1HasMirza = True
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[1]):
                    Player2HasMirza = True
        return not (Player1HasMirza and Player2HasMirza)

    def __GetSquareReference(self, Description):
        ##gets the square the player wants to move the peice 
        SelectedSquare = int(input("Enter the square " + Description + " (row number followed by column number): "))
        return SelectedSquare

    def __UseMoveOptionOffer(self):
        ##if player decides to take offer which spot in queue should it replace
        ReplaceChoice = int(input("Choose the move option from your queue to replace (1 to 5): "))
        self._CurrentPlayer.UpdateMoveOptionQueueWithOffer(ReplaceChoice - 1, self.__CreateMoveOption(self._MoveOptionOffer[self._MoveOptionOfferPosition], self._CurrentPlayer.GetDirection()))
        self._CurrentPlayer.ChangeScore(-(10 - (ReplaceChoice * 2)))
        ##removes points from current player score
        self._MoveOptionOfferPosition = random.randint(0, 4)
        ##replaces the old offer with a new one at random from the 5 moves


    def __GetPointsForOccupancyByPlayer(self, CurrentPlayer):
        ## adds points to the player depending on there position on the board
        ScoreAdjustment = 0
        for S in self._Board:
            ScoreAdjustment += (S.GetPointsForOccupancy(CurrentPlayer))
        return ScoreAdjustment

    def __UpdatePlayerScore(self, PointsForPieceCapture):
        ## updates the current player score
        self._CurrentPlayer.ChangeScore(self.__GetPointsForOccupancyByPlayer(self._CurrentPlayer) + PointsForPieceCapture)

    def __CalculatePieceCapturePoints(self, FinishSquareReference):
        ## calculates the points needed for a chnage in peices being capped
        if self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare() is not None:
            return self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare().GetPointsIfCaptured()
        return 0

    def PlayGame(self):
        ##runs at start of every loop of the game 
        GameOver = False
        while not GameOver:
            self.__DisplayState()
            SquareIsValid = False
            Choice = 0
            while Choice < 1 or Choice > 3:
                Choice = int(input("Choose move option to use from queue (1 to 3) or 9 to take the offer: "))
                if Choice == 9:
                    self.__UseMoveOptionOffer()
                    self.__DisplayState()
            ##checks if the position to move the peice to is part of the board 
            while not SquareIsValid:
                StartSquareReference = self.__GetSquareReference("containing the piece to move")
                SquareIsValid = self.__CheckSquareIsValid(StartSquareReference, True)
            SquareIsValid = False
            while not SquareIsValid:
                FinishSquareReference = self.__GetSquareReference("to move to")
                SquareIsValid = self.__CheckSquareIsValid(FinishSquareReference, False)
            ## runs a function to check if the position the player chose is a legal move
            MoveLegal = self._CurrentPlayer.CheckPlayerMove(Choice, StartSquareReference, FinishSquareReference)
            if MoveLegal:
                PointsForPieceCapture = self.__CalculatePieceCapturePoints(FinishSquareReference)
                self._CurrentPlayer.ChangeScore(-(Choice + (2 * (Choice - 1))))
                self._CurrentPlayer.UpdateQueueAfterMove(Choice)
                self.__UpdateBoard(StartSquareReference, FinishSquareReference)
                self.__UpdatePlayerScore(PointsForPieceCapture)
                print("New score: " + str(self._CurrentPlayer.GetScore()) + "\n")
            ##swaps which players turn it is
            if self._CurrentPlayer.SameAs(self._Players[0]):
                self._CurrentPlayer = self._Players[1]
            else:
                self._CurrentPlayer = self._Players[0]
            ## checks for game over
            GameOver = self.__CheckIfGameOver()
        ## prints board at end of turn
        self.__DisplayState()
        self.__DisplayFinalResult()

    def __UpdateBoard(self, StartSquareReference, FinishSquareReference):
        self._Board[self.__GetIndexOfSquare(FinishSquareReference)].SetPiece(self._Board[self.__GetIndexOfSquare(StartSquareReference)].RemovePiece())

    def __DisplayFinalResult(self):
        if self._Players[0].GetScore() == self._Players[1].GetScore():
            print("Draw!")
        ## if score is equel at the end draw
        elif self._Players[0].GetScore() > self._Players[1].GetScore():
            print(self._Players[0].GetName() + " is the winner!")
        else:
            print(self._Players[1].GetName() + " is the winner!")
        ## if one score is bigger thatn the other bigger score wins

    def __CreateBoard(self):
    ## creats the board withing the correct size
        for Row in range(1, self._NoOfRows + 1):
            for Column in range(1, self._NoOfColumns + 1):
                ## plcaces the Kotla on the board at start of game
                if Row == 1 and Column == self._NoOfColumns // 2:
                    S = Kotla(self._Players[0], "K")
                elif Row == self._NoOfRows and Column == self._NoOfColumns // 2 + 1:
                    S = Kotla(self._Players[1], "k")
                else:
                    S = Square()
                self._Board.append(S)

    def __CreatePieces(self, NoOfPieces):
        ##creates each sides peaices !for p1 " for p2
        ##also places the peices on each side of the board
        for Count in range(1, NoOfPieces + 1):
            CurrentPiece = Piece("piece", self._Players[0], 1, "!")
            self._Board[self.__GetIndexOfSquare(2 * 10 + Count + 1)].SetPiece(CurrentPiece)
        CurrentPiece = Piece("mirza", self._Players[0], 5, "1")
        self._Board[self.__GetIndexOfSquare(10 + self._NoOfColumns // 2)].SetPiece(CurrentPiece)
        for Count in range(1, NoOfPieces + 1):
            CurrentPiece = Piece("piece", self._Players[1], 1, '"')
            self._Board[self.__GetIndexOfSquare((self._NoOfRows - 1) * 10 + Count + 1)].SetPiece(CurrentPiece)
        CurrentPiece = Piece("mirza", self._Players[1], 5, "2")
        self._Board[self.__GetIndexOfSquare(self._NoOfRows * 10 + (self._NoOfColumns // 2 + 1))].SetPiece(CurrentPiece)

    def __CreateMoveOptionOffer(self):
        ## five options for a new move to add to the queue
        self._MoveOptionOffer.append("jazair")
        self._MoveOptionOffer.append("chowkidar")
        self._MoveOptionOffer.append("cuirassier")
        self._MoveOptionOffer.append("ryott")
        self._MoveOptionOffer.append("faujdar")

    def __CreateRyottMoveOption(self, Direction):
        ## gives the movement options for the ryott
        NewMoveOption = MoveOption("ryott")
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateFaujdarMoveOption(self, Direction):
        ## gives the movement options for the faujdar
        NewMoveOption = MoveOption("faujdar")
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateJazairMoveOption(self, Direction):
        ## gives the movement options for the jazair
        NewMoveOption = MoveOption("jazair")
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateCuirassierMoveOption(self, Direction):
        ## gives the movement options for the cuirassier
        NewMoveOption = MoveOption("cuirassier")
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateChowkidarMoveOption(self, Direction):
        ## gives the movement options for the ryott
        NewMoveOption = MoveOption("chowkidar")
        NewMove = Move(1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateMoveOption(self, Name, Direction):
        ## fetches the movement option
        if Name == "chowkidar":
            return self.__CreateChowkidarMoveOption(Direction)
        elif Name == "ryott":
            return self.__CreateRyottMoveOption(Direction)
        elif Name == "faujdar":
            return self.__CreateFaujdarMoveOption(Direction)
        elif Name == "jazair":
            return self.__CreateJazairMoveOption(Direction)
        else:
            return self.__CreateCuirassierMoveOption(Direction)

    def __CreateMoveOptions(self):
        ## cretes the movement option and orientantes it the correct way for each player
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", 1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", -1))

class Piece: ## creates each peice
    def __init__(self, T, B, P, S):
        self._TypeOfPiece = T
        self._BelongsTo = B     ## who the 
        self._PointsIfCaptured = P ##value of the peice
        self._Symbol = S

    def GetSymbol(self):
        ## returnts the symbol var
        return self._Symbol

    def GetTypeOfPiece(self):
        ## returns the peice type var
        return self._TypeOfPiece

    def GetBelongsTo(self):
        return self._BelongsTo

    def GetPointsIfCaptured(self):
        ## return point valuye of capped piece
        return self._PointsIfCaptured

class Square: ## creates each square as a objcet
    def __init__(self): ## statrts all the variables fopr each square created
        self._PieceInSquare = None
        self._BelongsTo = None
        self._Symbol = " "

    def SetPiece(self, P): ## if a peice in a square set var to P 
        self._PieceInSquare = P

    def RemovePiece(self): ## if peice not is square set vat to None
        PieceToReturn = self._PieceInSquare
        self._PieceInSquare = None
        return PieceToReturn

    def GetPieceInSquare(self): ## if peice on square then get name of peice
        return self._PieceInSquare

    def GetSymbol(self): ## get symbol in the square
        return self._Symbol

    def GetPointsForOccupancy(self, CurrentPlayer):
        return 0

    def GetBelongsTo(self):
        return self._BelongsTo

    def ContainsKotla(self): 
        ## if a kotla is in the square then assign symbol to the square
        if self._Symbol == "K" or self._Symbol == "k":
            return True
        else:
            return False

class Kotla(Square):
    ##creates the object Kotla 
    def __init__(self, P, S):
        super(Kotla, self).__init__()
        self._BelongsTo = P
        self._Symbol = S

    def GetPointsForOccupancy(self, CurrentPlayer):
        ## runs functions to get the points for differet position on the board
        if self._PieceInSquare is None:
            return 0
        elif self._BelongsTo.SameAs(CurrentPlayer):
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 5
            else:
                return 0
        else:
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 1
            else:
                return 0

class MoveOption:
    ## gets the player to select a move option and confirms it
    def __init__(self, N):
        self._Name = N
        self._PossibleMoves = []

    def AddToPossibleMoves(self, M):
        self._PossibleMoves.append(M)

    def GetName(self):
        return self._Name

    def CheckIfThereIsAMoveToSquare(self, StartSquareReference, FinishSquareReference):
        ## checks if a peice can get to square with any move avalible
        StartRow = StartSquareReference // 10
        StartColumn = StartSquareReference % 10
        FinishRow = FinishSquareReference // 10
        FinishColumn = FinishSquareReference % 10
        for M in self._PossibleMoves:
            if StartRow + M.GetRowChange() == FinishRow and StartColumn + M.GetColumnChange() == FinishColumn:
                return True
        return False

class Move:
    ## class to move the peice to the specified row
    def __init__(self, R, C):
        self._RowChange = R
        self._ColumnChange = C

    def GetRowChange(self):
        return self._RowChange

    def GetColumnChange(self):
        return self._ColumnChange

class MoveOptionQueue:
    ## class to move the que along when a move has been chosen
    def __init__(self):
        self.__Queue = []

    def GetQueueAsString(self):
        ## gets the que as a string for eiser handling
        QueueAsString = ""
        Count = 1
        for M in self.__Queue:
            QueueAsString += str(Count) + ". " + M.GetName() + "   "
            Count += 1
        return QueueAsString

    def Add(self, NewMoveOption):
        self.__Queue.append(NewMoveOption)

    def Replace(self, Position, NewMoveOption):
        self.__Queue[Position] = NewMoveOption

    def MoveItemToBack(self, Position):
        Temp = self.__Queue[Position]
        self.__Queue.pop(Position)
        self.__Queue.append(Temp)

    def GetMoveOptionInPosition(self, Pos):
        return self.__Queue[Pos]

class Player:
    ## method to create each player
    def __init__(self, N, D):
        self.__Score = 100
        self.__Name = N
        self.__Direction = D
        self.__Queue = MoveOptionQueue()

    def SameAs(self, APlayer):
        ## creates a player name 
        if APlayer is None:
            return False
        elif APlayer.GetName() == self.__Name:
            return True
        else:
            return False

    def GetPlayerStateAsString(self):
        return self.__Name + "\n" + "Score: " + str(self.__Score) + "\n" + "Move option queue: " + self.__Queue.GetQueueAsString() + "\n"

    def AddToMoveOptionQueue(self, NewMoveOption):
        self.__Queue.Add(NewMoveOption)

    def UpdateQueueAfterMove(self, Position):
        self.__Queue.MoveItemToBack(Position - 1)

    def UpdateMoveOptionQueueWithOffer(self, Position, NewMoveOption):
        self.__Queue.Replace(Position, NewMoveOption)

    def GetScore(self):
        ## return current player score
        return self.__Score

    def GetName(self):
        ## return current player name
        return self.__Name

    def GetDirection(self):
        ## return current player orientation
        return self.__Direction

    def ChangeScore(self, Amount):
        ## return the amount the score has ben changed of the current player
        self.__Score += Amount

    def CheckPlayerMove(self, Pos, StartSquareReference, FinishSquareReference):
        ## checks if the move and destitation matvh up
        Temp = self.__Queue.GetMoveOptionInPosition(Pos - 1)
        return Temp.CheckIfThereIsAMoveToSquare(StartSquareReference, FinishSquareReference)

def Main():
    ## the code that starts it all calls play game
    ThisGame = Dastan(6, 6, 4)
    ThisGame.PlayGame()
    print("Goodbye!")
    input()

if __name__ == "__main__":
    ## starts game
    Main()
