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
                    self.board[coords] = [0,0]     # red player
                elif coords in [(5,0),(5,2),(5,4),(5,6),
                                (6,1),(6,3),(6,5),(6,7),
                                (7,0),(7,2),(7,4),(7,6)]:
                    self.board[coords] = [1,0]    # white player
                else:
                    self.board[coords] = None  # no checkers
        self.currentPlayer = 0  # red player starts
        self.pieceToMove = (0,0)    # tuple to store coords of piece to move
        self.isPiece = False       # bool to check if piece can be moved 
        self.becameKing = False 
        self.legalMoves = list(tuple())       # list with legal moves 
        self.legalJumps = list(tuple())      # list with legal jumps 
        self.notValid = False      # bool if move is not valid
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
        if (self.board[pieceToMove] is not None) and \
            (self.board[pieceToMove][0] == self.currentPlayer):
            print("what")
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
        print(self.board[coords][1])
        coord1, coord2, coord3, coord4 = (0,0), (0,0), (0,0), (0,0)
        if self.isPiece:   # if piece chosen is valid 
            while True:
                jumps = 0  # to check for multiple jumps 
                # loop over two (3 if king) possible directions 
                for player in [0,1]:
                    for dc in [-1,0,1]:
                        # red player
                        if player == thisPlayer and player == 0: rc, rc2 = 1, 2  
                        # white player 
                        elif player == thisPlayer and player == 1: rc, rc2 = -1, -2
                        else: continue       
                        # assign second square values 
                        if dc == -1: dc2 = -2
                        elif dc == 1: dc2 = 2
                        # assign first and second square 
                        if dc != 0:    # regular pieces can't go straight
                            coord1 = (coords[0]+rc,coords[1]+dc)
                            coord2 = (coords[0]+rc2,coords[1]+dc2)
                        if (self.board[coords][1] == 3 and dc == 0):    # king pieces can go straight 
                            print("why")
                            coord1 = (coords[0]+rc,coords[1]+dc)
                            coord2 = (coords[0]+rc2,coords[1]+dc2)
                        # check backwards for kings 
                        if self.board[coords][1] == 3:
                            coord3 = (coords[0]-rc,coords[1]+dc)   # backwards regular 
                            coord4 = (coords[0]-rc2,coords[1]+dc2) # backwards jump 
                        # for bordering checkers 
                        done = False 
                        for i in [0, 1]: 
                            if coord1[1] < 0 or coord1[1] > 7: done = True 
                            if coord1[0] < 0 or coord1[0] > 7: done = True
                        if done:
                            done = False 
                            break
                        # check if can move
                        for coord in [coord1, coord3]:
                            if coord == coord1 or (coord == coord3 and self.board[coords][1] == 3):
                                if self.board[coord] is None:
                                    self.legalMoves.append(coord)
                                    continue
                                # for bordering checkers 
                                for i in [0, 1]: 
                                    if coord2[1] < 0 or coord2[1] > 7: done = True 
                                    if coord2[0] < 0 or coord2[0] > 7: done = True  
                                if done:
                                    break
                                # assign second coords 
                                if coord == coord1: c2 = coord2     
                                else: c2 = coord4
                                # check if can jump
                                if self.board[coord] is not None and \
                                self.board[c2] is None and \
                                self.board[coord][0] == otherPlayer:
                                    jumps += 1
                                    self.legalJumps.append(c2) 
                                    break
                if jumps > -1:
                    break
        else:
            return  # do nothing 
        print(self.legalMoves)

    def has_moves(self):
        '''CheckerBoard.has_moves()
        Returns true if piece chosen can move'''
        if len(self.legalMoves) > 0:
            return True 

    def revert_data(self): 
        '''CheckerBoard.revert_data() 
        Reverts data to original values after each turn'''
        self.legalMoves.clear()
        self.legalJumps.clear()
        self.isPiece = False  
        self.becameKing = False 
        
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
            self.board[placeToMove] = [thisPlayer,0]
            self.isPiece = False  # revert bool for valid piece to be used again 
            # find removed piece 
            if thisPlayer == 0: # red player 
                if self.pieceToMove[1] - placeToMove[1] < 0:
                    removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]+1)
                else:
                   removedPiece = (self.pieceToMove[0]+1,self.pieceToMove[1]-1) 
            if thisPlayer == 1: # white player 
                if self.pieceToMove[1] - placeToMove[1] < 0:
                    removedPiece = (self.pieceToMove[0]-1,self.pieceToMove[1]+1)
                else:
                    removedPiece = (self.pieceToMove[0]-1,self.pieceToMove[1]-1) 
            # remove piece from board 
            self.board[removedPiece] = None 
            self.next_player()        # go to next player 
        # if can't jump, go to moves 
        elif placeToMove in self.legalMoves:
            # check if at end of board 
            if placeToMove[0] == 0 or placeToMove[0] == 7:
                self.becameKing = True
                self.board[placeToMove] = [thisPlayer,3]
            else:
                self.board[placeToMove] = [thisPlayer,0]
            # adjust board 
            self.board[self.pieceToMove] = None
            self.next_player()        # go to next player 
        else: 
            self.notValid = True 

    def get_pieceToMove(self): 
        '''CheckerBoard.get_pieceToMove() 
        Returns coords of pieceToMove ''' 
        return self.pieceToMove

    def has_jumps(self): 
        '''CheckerBoard.has_jumps() 
        Returns true if piece can jump'''
        if len(self.legalJumps) > 0: 
            return True 

    def not_valid_move(self): 
        '''CheckerBoard.valid_move()
        Returns true if move was valid'''
        return self.notValid

    def valid_piece(self): 
        '''CheckerBoard.not_valid_piece()
        Returns true if piece is valid, false if not'''
        return self.isPiece 

    def revert_valid_move(self):
        '''CheckerBoard.rever_valid_move()
        Changes valid_move bool to false'''
        self.notValid = False

                    
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
        self.clicks = 0
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
        self.create_text(27,32,text="*",font="Times 35 italic bold")

    def get_color(self):
        '''CheckerSquare.get_color()
        returns color associated with checker square'''
        return self.color 

    def is_king(self):
        '''CheckerSquare.is_king() 
        returns True if has checker and is a king, False if not'''
        return self.isKing

    def remove_color(self):
        '''CheckerSquare.remove_color(coords)
        removes oval from square'''
        self.delete("all")

class CheckersGame(Frame):
    '''Represents a game of Checkers'''
    
    def __init__(self,master):
        '''CheckersGame(master)
        creates a new Checkers game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # data
        self.colors = ['red','white']  # players colors
        self.pieceToMove = None
        self.placeToMove = (0,0)
        self.click = 0
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
        self.moveLabel = Label(self,font=('Arial',13))
        self.turnLabel.grid(row=9,column=2)
        self.moveLabel.grid(row=9,column=4,columnspan=5)
        self.update_display()

    def get_click(self,event):
        '''CheckersGame.get_click(event)
        event hander for mouse click
        gets click data and selects piece to move'''
        self.click = 1
        self.pieceToMove = event.widget.get_position()
        # piece will select if valid, nothing if not 
        self.board.choose_piece(self.pieceToMove)
        if not self.board.valid_piece():
            self.moveLabel['text'] = 'Please choose a valid piece!'
            self.squares[self.pieceToMove]['highlightbackground'] = 'white'
        else: 
            self.moveLabel['text'] = ''
        self.board.get_legal_moves()
        self.update_display()

    def get_second_click(self,event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets second click data and tries to move selected piece'''
        self.click = 2
        self.placeToMove = event.widget.get_position()
        # piece will move if valid, nothing if not
        self.board.try_move(self.placeToMove)
        if self.moveLabel['text'] != 'Please choose a valid piece!':
            if (self.board.not_valid_move()) and (self.board.has_jumps()):
                self.moveLabel['text'] = 'You have to jump!'
            elif self.board.not_valid_move():
                self.moveLabel['text'] = 'Please choose a valid move!'
        self.update_display() # update the display
        self.board.revert_data()   # revert data for next move 
        
    def update_display(self):
        '''CheckersGame.update_display()
        updates squares/checkers to match board'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                checker = self.board.get_checker(rc)
                # revert all the squares to white bg 
                self.squares[rc]['highlightbackground'] = 'white'
                if checker is None: 
                    self.squares[rc].remove_color()     
                if checker is not None:
                    self.squares[rc].make_color(self.colors[checker[0]])
                    # check if checker is king 
                    if checker[1] == 3:
                        self.squares[rc].make_king()
                # revert square highlights
                if self.click == 1:
                    self.squares[self.pieceToMove]['highlightbackground'] = 'black'
                    if self.moveLabel['text'] != 'Please choose a valid piece!':
                        self.moveLabel['text'] = ''
                        self.squares[rc].switch_clicks(self)
                if self.click == 2:
                    self.squares[self.placeToMove]['highlightbackground'] = 'black'
                    self.squares[rc].switch_clicks(self)
        # update turn indicator 
        newPlayer = self.board.get_player()
        oldPlayer = 1 - self.board.get_player()
        self.turnSquare.make_color(self.colors[newPlayer])
        # revert valid move variable if needed 
        self.board.revert_valid_move()
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