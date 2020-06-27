from tkinter import *

class CheckerBoard:
    '''Represents a board of checkers'''

    def __init__(self):
        '''CheckerBoard()
        creates a CheckerBoard in starting position'''
        self.board = {} # dict to store checker positions
        # create positions
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if coords in [(0,1),(0,3),(0,5),(0,7),
                              (1,0),(1,2),(1,4),(1,6),
                              (2,1),(2,3),(2,5),(2,7)]:
                    self.board[coords] = 0     # red player
                elif coords in [(5,0),(5,2),(5,4),(5,6),
                                (6,1),(6,3),(6,5),(6,7),
                                (7,0),(7,2),(7,4),(7,6)]:
                    self.board[coords] = 1     # white player
                else:
                    self.board[coords] = None  # no checkers
        self.currentPlayer = 0  # red player starts
        self.pieceToMove = None    # tuple to store coords of piece to move
        self.isPiece = False       # bool to check if piece can be moved 
        self.legalMoves = []       # list with legal moves 
        self.legalJumps = []       # list with legal jumps 
        self.endgame = None  # replace with string once game ends

    def get_checker(self,coords):
        '''CheckerBoard.get_checker(coords) -> int
        returns the checker at coords'''
        return self.board[coords]

    def get_endgame(self):
        '''CheckerBoard.get_endgame() -> None or str
        returns endgame state'''
        return self.endgame

    def get_player(self):
        '''CheckerBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def next_player(self):
        '''CheckerBoard.next_player()
        moves to next player'''
        self.currentPlayer = 1 - self.currentPlayer

    def choose_piece(self,pieceToMove):
        '''CheckerBoard.choose_piece(pieceToMove)
        sets isMovable to True if piece can be moved by curr player
        pieceToMove -> coords of the piece curr player wants to move'''
        if self.board[pieceToMove] is not None and \
            self.board[pieceToMove] == self.currentPlayer:
            self.pieceToMove = pieceToMove
            self.isPiece = True 

    def get_legal_moves(self):
        '''CheckerBoard.get_legal_moves(coords[checkingOnly])
        placeToMove -> where the curr player wants to move pieceToMove
        checkingOnly False removes piece if player can jump
        checkingOnly True only checks if can jump'''
        thisPlayer = self.currentPlayer
        otherPlayer = 1 - thisPlayer
        coords = self.pieceToMove  # assign coords 
        if self.isPiece:   # if piece chosen is valid 
            while True:
                jumps = 0  # to check for multiple jumps 
                # loop over two possible directions 
                for dc in [-1,1]:
                    # to check for the square after the adjacent square 
                    if dc == -1:
                        dc2 = -2
                    else:
                        dc2 = 2
                    # assign first and second square 
                    if thisPlayer == 0:  # for red player
                        (row,col) = (coords[0]+1,coords[1]+dc)
                        (row2,col2) = (coords[0]+2,coords[1]+dc2)
                    else:  # for white player 
                        (row,col) = (coords[0]-1,coords[1]+dc)
                        (row2,col2) = (coords[0]-2,coords[1]+dc2)
                    # check if can jump  
                    if self.board[(row,col)] is not None and \
                       self.board[(row2,col2)] is None and \
                       self.board[(row,col)] == otherPlayer:
                        jumps += 1
                        self.legalJumps.append((row2,col2))
                        if thisPlayer == 0:   # red player 
                            self.board[coords] = (coords[0]+2,coords[1]+dc2)
                        else:    # white player 
                            self.board[coords] = (coords[0]-2,coords[1]+dc2)
                        break
                    # check if can move
                    if self.board[(row,col)] is None:
                        self.legalMoves.append((row,col))
                '''if jumps >= 1: # if player has jumped, check if can jump again 
                    continue 
                else:  # otherwise, break'''
                if jumps > -1:
                    break
        else:
            return   # do nothing 

    def try_move(self,placeToMove):
        '''CheckerBoard.try_move(coords)
        places curr player's piece in given square if the
        square is empty + move is legal'''
        thisPlayer = self.currentPlayer
        otherPlayer = 1 - thisPlayer
        jumps = 0
        # check jumps first 
        if placeToMove in self.legalJumps:
            jumps += 1
            self.board[self.pieceToMove] = None 
            self.board[placeToMove] = thisPlayer
            self.isPiece = False  # revert bool for valid piece to be used again 
            self.next_player  # go to next player 
            # find removed piece 
            if thisPlayer == 0: # red player 
                if self.pieceToMove[1] - placeToMove[1] < 0:
                    removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]+1)
                else:
                   removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]-1) 
            if thisPlayer == 1: # white player 
                if self.pieceToMove[1] - placeToMove[1] < 0:
                    removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]+1)
                else:
                   removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]-1) 
            # remove piece from board 
            self.board.remove(removedPiece)
        # if can't jump, go to moves 
        if placeToMove in self.legalMoves:
            self.board[placeToMove] = thisPlayer 
            self.board[self.pieceToMove] = None
            self.isPiece = False  # revert bool for valid piece to be used again 
            self.next_player  # go to next player 

    def bloop (self):
        '''blah blah blah'''
        if self.board[self.pieceToMove] == None: 
            print('something is more wrong priyanka')
            print('yeah no shit')
            print(self.pieceToMove)
        else: 
            print('something is wrong priyanka')
                    
class CheckerSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c,color):
        '''CheckerSquare(master,r,c)
        creates a new blank Checker square at given coordinate (r,c)'''
        # attributes
        self.color = color
        self.position = (r,c)
        self.isKing = False 
        # create + locate widget
        Canvas.__init__(self,master,width=50,height=50,bg=self.color)
        self.create_text(100,10,fill="black",font="Times 20 italic bold",
                                text="*")
        self.grid(row=r,column=c)
        # bind button to click to move checker
        self.clicks = 1
        self.bind('<Button>',master.get_click)      

    def switch_clicks(self,master):
        '''CheckerSquare.switch_clicks() 
        switches from first click to second click and vice versa'''
        self.clicks = 1 - self.clicks 
        if self.clicks == 0:
            self.bind('<Button>',master.get_click)
        else: 
            self.bind('<Button>',master.get_second_click)

    def get_position(self):
        '''CheckerSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def make_color(self,color):
        '''CheckerSquare.make_color(color)
        makes color of checker on square to specified color'''
        self.create_oval(10,10,44,44,fill=color)

    def make_king(self):
        '''CheckerSquare.make_king()
        adds star to stop of checker''' 
        self.isKing = True

    def get_color(self):
        '''CheckerSquare.get_color()
        returns color associated with checker square'''
        return self.color 

    def is_king(self):
        '''CheckerSquare.is_king() 
        returns True if has checker and is a king, False if not'''
        return self.isKing

class CheckersGame(Frame):
    '''Represents a game of Checkers'''
    
    def __init__(self,master):
        '''CheckersGame(master)
        creates a new Checkers game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # data
        self.colors = ('red','white')  # players colors
        # create board in starting position
        self.board = CheckerBoard()
        self.squares = {}  # stores CheckerSquares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                if ((column % 2) == 0 and (row % 2 == 0)) or ((column % 2) > 0 and (row % 2) > 0):  # for tan squares 
                    self.squares[rc] = CheckerSquare(self,row,column,'blanched almond')
                else:   # for green squares
                    self.squares[rc] = CheckerSquare(self,row,column,'dark green')
        # set up status marker
        self.rowconfigure(8,minsize=3)  # spacing
        self.turnSquare = CheckerSquare(self,9,3,'grey')
        self.turnSquare.make_color(self.colors[0])
        self.turnSquare.unbind('<Button>')
        self.turnLabel = Label(self,text='Turn:',font=('Arial',18))
        self.turnLabel.grid(row=9,column=2)
        self.update_display()

    '''def switch_clicks_two(self):
        CheckersGame.switch_clicks()
        switches between clicks
        for row in range(8):
            for col in range(8):
                rc = (row,col)
                self.squares[rc].switch_clicks(self)'''

    def get_click(self,event):
        '''CheckersGame.get_click(event)
        event hander for mouse click
        gets click data and selects piece to move'''
        pieceToMove = event.widget.get_position()
        # piece will select if valid, nothing if not 
        self.squares[pieceToMove]['highlightbackground'] = 'black'
        self.board.choose_piece(pieceToMove)
        self.board.get_legal_moves()
        self.update_display()

    def get_second_click(self,event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets second click data and tries to move selected piece'''
        placeToMove = event.widget.get_position()
        # piece will move if valid, nothing if not
        self.squares[placeToMove]['highlightbackground'] = 'blue'
        self.board.try_move(placeToMove)
        self.board.bloop()
        self.update_display() # update the display
        
    def update_display(self):
        '''CheckersGame.update_display()
        updates squares/checkers to match board'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                checker = self.board.get_checker(rc)
                if checker is not None:
                    self.squares[rc].make_color(self.colors[checker])
                self.squares[rc].switch_clicks(self)
        # update turn indicator 
        newPlayer = self.board.get_player()
        oldPlayer = 1 - self.board.get_player()
        self.turnSquare.make_color(self.colors[newPlayer])
        # if game over, show endgame message
        endgame = self.board.get_endgame()
        if endgame is not None:  # if game is over
            # make turn indicator show winner 
            self.turnSquare.make_color(self.colors[endgame])
            winner = self.colors[endgame]  # color of winner
            endgameMessage = '{} wins!'.format(winner.title())

def play_checkers():
    '''play_checkers()
    starts an new game of checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()

play_checkers()