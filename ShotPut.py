from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class ShotPutFrame(Frame):
    '''Frame for a game of Shot Put'''

    def __init__(self, master, name):
        '''ShotPutFrame(self,master,name) -> ShotPutFrame
        creates a new Shot Put game
        name is the name of the player'''
        Frame.__init__(self,master)
        self.grid()
        # player name label
        Label(self,text=name).grid(columnspan=3,sticky=W)
        # game data 
        self.score = 0
        self.highscore = 0
        self.attempts = 1
        self.dicenum = 0
        # score + attempts labels
        self.attemptScoreLabel = Label(self,text='Attempt #1 Score = 0')
        self.attemptScoreLabel.grid(row=0,column=3,columnspan=2)
        self.highscoreLabel = Label(self,text='High Score: 0')
        self.highscoreLabel.grid(row=0, column=6, columnspan=3)
        # dice
        self.dice = []
        for die in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5))
            self.dice[die].grid(row=1,column=die)
        # buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=3)

    def roll(self):
        '''ShotPutFrame(self).roll()
        handler method to roll the die'''
        if self.dicenum < 9:
            # roll the die
            self.dice[self.dicenum].roll()
            # enable the stop button
            self.stopButton['state'] = ACTIVE
            self.rollButton['state'] = ACTIVE
            # check if player rolled a 1
            if self.dice[self.dicenum].get_top() == 1:
                self.rollButton['state'] == DISABLED
                self.stopButton['text'] = 'FOUL'
                self.score = 0
                self.attemptScoreLabel['text'] = 'FOULED ATTEMPT'
            else:
                self.score += self.dice[self.dicenum].get_top()
                self.attemptScoreLabel['text']='Attempt #'+str(self.attempts)+' Score = '+str(self.score)
                self.dicenum += 1
                self.rollButton.grid(row=2,column=self.dicenum,columnspan=1)
                self.stopButton.grid(row=3,column=self.dicenum,columnspan=1)
        else:
            self.stop()

    def stop(self):
        '''ShotPutFrame(self).stop()
        handler method to move to next die/turn'''
        self.stopButton['text'] = 'Stop'
        if self.attempts < 3:
            if self.score > self.highscore:
                self.highscoreLabel['text'] = 'High Score: '+str(self.score)
            else:
                self.highscoreLabel['text'] = 'High Score: '+str(self.highscore)
            self.stopButton['state'] = DISABLED
            # clear old dice + make new set 
            self.dice.clear()
            for die in range(8):
                self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5))
                self.dice[die].grid(row=1,column=die)
            # revert data to 0 + move to next attempt 
            self.score = 0
            self.dicenum = 0
            self.attempts += 1
            # move buttons
            self.rollButton.grid(row=2,column=self.dicenum,columnspan=2)
            self.stopButton.grid(row=3,column=self.dicenum,columnspan=2)
        else:
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()
            self.attemptScoreLabel['text'] = 'Game Over'
            

# play the game
name = input("Enter your name: ")
root = Tk()
root.title('Shot Put')
game = ShotPutFrame(root,name)
game.mainloop()