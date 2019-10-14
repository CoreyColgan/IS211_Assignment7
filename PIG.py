#!/usr/bin/env python
# coding: utf-8

# In[9]:


#The rules of Pig are simple. The game features two players, whose goal is to reach 100 points first. Each
#turn, a player repeatedly rolls a die until either a 1 is rolled or the player holds and scores the sum of the
#rolls (i.e. the turn total)

#!user/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import os
import argparse

# Create a class named "Player" for storing player's info 
class Player(object):
    
    def __init__(self):
        self.score = 0
        self.turn = False
        self.name = input('Enter a player name please: ').strip()

    def returnScore(self):
        return self.score

    def setScore(self, points):
        self.score += points

    def returnName(self):
        return self.name

    def setTurn(self, turn):
        self.turn = turn

    def returnTurn(self):
        return self.turn
    
# Create a class for storing dice details
class Dice(object):
   
    def __init__(self):
        self.value = random.seed(0)

    def roll(self):
        # Die values (1 thru 6)
        self.value = random.randint(1, 6)
        return self.value

    def returnCurrentRoll(self):
        return self.value

# Create a class for holding player objects and their variables
class Game(object):

    def __init__(self):
        self.pendingPoints = 0
        self.activePlayer = 0
        self.turns = 0
        self.dice = Dice()
        self.scoreData = {}
        self.gameData = []

    def addPlayer(self, index):
        self.gameData.append(Player())
        self.scoreData[self.gameData[index].returnName()] = self.gameData[index].returnScore()

    def addPlayersToGame(self, players):
        for player in range(players):
            self.addPlayer(player)

    def returnActivePlayer(self):
        return self.gameData[self.activePlayer]

    def returnPendingPoints(self):
        return self.pendingPoints

    def returnWinState(self):
        for player in self.gameData:
            if player.returnScore() >= 100:
                return True
        return False

    def returnGameStatus(self):
        os.system('cls')
        print ('Pig\n')
        print ('{:15} : {:>6}\n'.format('Player', 'Score'))
        for player in self.gameData:
            print ('{:15} : {:6} \n'.format(player.returnName(), player.returnScore()))
        print ('It is {}\'s turn'.format(self.returnActivePlayer().returnName()))
        if self.dice.returnCurrentRoll() == 1:
            print ('Last score was {}, next player\'s turn!'.format(self.dice.returnCurrentRoll()))
        else:
            print ('Last score was {}'.format(self.dice.returnCurrentRoll()))
        print ('Pending Points: {:>10}'.format(self.returnPendingPoints()))

# Function for taking user input - asks for roll or hold ('r' / 'h' respectively) - If a player rolls 1 exit and move 
# to next player - if a player goes over 100 total, exit and go to next player

    def playerTurn(self, player):
        player.setTurn(True)
        while player.returnTurn() and not self.returnWinState():
            self.returnGameStatus()
            self.returnPendingPoints()
            playerChoice = input(
                "Please enter a choice - [h] to hold, or [r] to roll: ").strip()
            if playerChoice.lower() == 'h':
                player.setScore(self.returnPendingPoints())
                self.pendingPoints = 0
                player.setTurn(False)
            elif playerChoice.lower() == 'r':
                roll = self.dice.roll()
                if roll == 1:
                    self.pendingPoints = 0
                    player.setTurn(False)
                else:
                    self.pendingPoints += roll
                    continue
            else:
                input("Invalid - please enter [h] for hold or [r] for roll")
                continue

# Function for creating user players and handles game processes

    def gameLoop(self, players=2):
        for player in range(players):
            self.addPlayer(player)

        while not self.returnWinState():
            for player in self.gameData:
                self.activePlayer = (self.turns % len(self.gameData))
                self.playerTurn(player)
                self.turns += 1
        for player in self.gameData:
            if player.returnScore() >= 100:
                print ('\nThe winner is {} who scored {} points'.format(
                    player.returnName(), player.returnScore()))
        newGame = input("\nWould you like to play again? [y] for YES | [n] for NO : ")
        if newGame == 'y':
            try:
                newGamePlayers = int(input("\nEnter number of players: "))
            except ValueError:
                print ('Invalid - default 2 players will be chosen')
            else:
                self.resetGame()
                self.gameLoop(newGamePlayers)
            finally:
                self.resetGame()
                self.gameLoop()
        elif newGame == 'n':
            print ('Thank you for playing')
            sys.exit()
        else:
            print ('Invalid entry - application will close')
            sys.exit()
            
# Function to reset game variables when starting new game 
    def resetGame(self):
        
        self.pendingPoints = 0
        self.activePlayer = 0
        self.turns = 0
        self.dice = Dice()
        self.scoreData = {}
        self.gameData = []

# Main method to run game
def main():
    newGame = Game()
    parser = argparse.ArgumentParser()
    parser.add_argument('--numPlayers',
                        help='Number of selected players for game',
                        type=int, required=False)
    args = parser.parse_args()
    if args.numPlayers:
        newGame.gameLoop(args.numPlayers)
    else:
        newGame.gameLoop()


if __name__ == '__main__':
    main()


# In[ ]:




