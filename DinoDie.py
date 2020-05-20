import random

class Die:
    '''Die class'''

    def __init__(self,sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides,int):
            self.numSides = sides
            self.sides = list(range(1,sides+1))
        else:  # use the list/tuple provided 
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+'-sided die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value

### end Die class ###

class DinoDie(Die):
    '''implements one die for Dino Hunt'''

    def __init__(self, color, sides):
        '''DinoDie()
        Creates a die with given color and options'''
        self.color = str(color)         # color of die: green, red, yellow
        # no num of sides since dino die
        self.numSides = len(sides)      
        self.sides = list(sides)
        # roll to get random top 
        self.roll()
            
    def __str__(self):
        '''str(DinoDie) -> str
        Represents str of DinoDie'''
        return 'A '+str(self.color)+' DinoDie with '+\
               str(self.get_top())+' on top'

    def get_color(self):
        '''DinoDie.get_color() -> str
        Returns color of DinoDie'''
        return self.color 

class DinoPlayer:
    '''implements a player of Dino Hunt'''

    def __init__(self, name, score=0):
        '''DinoPlayer()
        Creates a Dino Hunt player with given name and score'''
        self.name = str(name)
        self.score = score 

    def __str__(self):
        '''str(DinoPlayer) -> str
        String representation of DinoPlayer'''
        return self.name + ' has ' + str(self.score) + ' points.'

    def get_score(self):
        '''DinoPlayer.get_score()
        Returns player's score'''
        return str(self.score)

    def get_name(self):
        '''DinoPlayer.get_name()
        Returns players name'''
        return str(self.name) 

    def take_turn(self, DinoDie):
        '''DinoPlayer.take_turn(DinoDie)
        Simulates a turn in Dino Hunt
        DinoDie: one of the 13 dies'''
        # create 13 dies 
        dies = []
        diesColors = []
        for num in range(6):
            diesColors.append('green')
            dies.append(DinoDie('green', ['Dino', 'Dino', 'Dino', 'leaf', 'leaf', 'foot']))
        for num in range(4):
            diesColors.append('yellow')
            dies.append(DinoDie('yellow', ['Dino', 'Dino', 'leaf', 'leaf', 'foot', 'foot']))
        for num in range(3):
            diesColors.append('red')
            dies.append(DinoDie('red', ['Dino', 'leaf', 'leaf', 'foot', 'foot', 'foot']))
        # start turn 
        print(self.name + ", it's your turn!")
        print('You have ' + str(len(dies)) + ' dice remaining.')
        print(str(diesColors.count('green')) + ' green, ' + str(diesColors.count('yellow')) + ' yellow, '+str(diesColors.count('red'))+' red')
        # create a var for num of feet + dinos
        numFeet = 0
        numDinos = 0
        currScore = 0
        while True:
            input('Press enter to select dice and roll.')
            dieTops = []
            # select dies and roll
            if len(dies) >= 3:
                for x in range(3):
                    die = random.choice(dies)   # roll selected die
                    die.roll()
                    dieTops.append(die.get_top())            # get top
                    if die.get_top() == 'Dino' or die.get_top() == 'foot':
                        dies.remove(die)      # remove that die from dies
                        diesColors.remove(die.get_color())
                    print('    ' + str(die))
            else:
                for x in range(len(dies)):
                    die = random.choice(dies)   # roll selected die
                    die.roll()
                    dieTops.append(die.get_top())            # get top
                    if die.get_top() == 'Dino' or die.get_top() == 'foot':
                        dies.remove(die)      # remove that die from dies
                        diesColors.remove(die.get_color())
                    print('    ' + str(die))
            # check if player got stomped
            numFeet += dieTops.count('foot')
            numDinos += dieTops.count('Dino')
            if numFeet >= 3:             
                print('Too bad -- you got stomped!')
                numDinos = 0
                currScore = 0
                break
            # update score
            currScore += dieTops.count('Dino')
            print('This turn so far: '+str(numDinos)+" Dinos and "+str(numFeet)+' feet.')
            print('You have ' + str(len(dies)) + ' dice remaining.')
            print(str(diesColors.count('green')) + ' green, ' + str(diesColors.count('yellow')) + ' yellow, '+str(diesColors.count('red'))+' red') 
            if input('Do you want to roll again? (y/n) ') == 'n':
                break
        self.score += currScore 

def play_dino_hunt(numPlayers,numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
    # get player names
    playerList = []
    scores = []
    currentPlayerNum = 0
    for player in range(numPlayers):
        name = input('Player '+str(player+1)+', enter your name: ')
        playerList.append(DinoPlayer(name))
        scores.append(playerList[currentPlayerNum].get_score())
    print('------------')
    # start a round 
    for rnd in range(1, numRounds+1):
        print('ROUND ' + str(rnd))
        print(' ')
        for player in range(numPlayers): 
            playerList[currentPlayerNum].take_turn(DinoDie)
            # update score 
            scores[player] = playerList[currentPlayerNum].get_score()
            print('------------')
            for player in playerList:
                print(player)
            print('------------')
            # go to next player 
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
    # check which player has highest score
    highestScore = max(scores)
    for player in playerList:
        if player.get_score() == highestScore:
            print(player.get_name() + ' has won!')

play_dino_hunt(2,2)