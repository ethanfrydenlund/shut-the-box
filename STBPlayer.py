import random
import copy
import re
import sys
import time


class STBPlayer:
    BOARDSIZE = 9
    DICESIDES = 6
    board = ['u' for i in range(BOARDSIZE)]
              

    def remake_board(self):
        self.board = ['u' for i in range(self.BOARDSIZE)]

    def print_board(self):
        #19 for boardsize 8 so perhaps boardsize*2 + 1????
        spacers = '-'*((self.BOARDSIZE*2)+1)
        if (self.BOARDSIZE > 10):
            spacers+= '-'*(self.BOARDSIZE -9)

        print(spacers)
        
        for i in range(self.BOARDSIZE):
            if self.board[i] == 'u':
                print('|' + str(i+1), end='')
            elif i<9:
                print('| ', end='')
            else:
                print('|  ', end ='')
        print('|')

        print(spacers)

        for i in range(self.BOARDSIZE):
            if self.board[i] == 'd':
                print('|' + str(i+1), end='')
            elif i<9:
                print('| ', end='')
            else:
                print('|  ', end='')
        print('|')

        print(spacers)

    def game_value(self, roll):
        #return 1 = win; return -1 = loss;
        upCount = 0
        for tile in self.board:
            if tile == 'u':
                upCount = upCount + 1

        if upCount  == 0:
            return 1
        return 0

    def get_move(self, roll):
        move=""
        available = []
        for x in reversed(range(self.BOARDSIZE)):
            if self.board[x] == 'u':
                available.append(x+1)

        # we have list of numbers in play and roll now what?
        available.sort(reverse=True)
        for i in range(len(available)):
            count = roll
            position = i
            while(count!=0):
                best = self.get_move_helper(available, position, count)
                if best == -1:
                    break;
                count -= available[best]
                position = best + 1
                move+= str(available[best]) + " "

            if count == 0:
                return move
            move=""

        return move
                    
    def get_move_helper(self, avail, index, val):
        best = -1;
        for i in range(index,len(avail)):
            if avail[i] <= val:
                best = i
                break;

        return best
        
    def make_move(self, move, roll):
        total = 0 
        moves = re.findall(r'\d+', move)
        used = [0] * (self.BOARDSIZE + 1)
        for indiv in moves:
            indiv = int(indiv)
            if indiv > self.BOARDSIZE:
                return False

            if used[indiv] == 1:
                return False
            used[int(indiv)] = 1

            total+= indiv
            if self.board[int(indiv)-1] == 'd':
                return False
        if total != roll:
            return False
        for indiv in moves:
            self.board[int(indiv)-1] = 'd'
        return True

def main():
    ai = STBPlayer()
    print('--------------------------------------')
    print('--------------------------------------')
    print('Welcome to AI assisted Shut The Box!!!')
    print('--------------------------------------')
    print('--------------------------------------')
    
    
    recSetting = input('Would you like to play with AI reccomendations? (y/n) ')
    while (not(recSetting == 'y' or recSetting == 'n')):
        recSetting = input('Please answer with y or n: ')

    if recSetting == 'y':
        recSetting = True
    else:
        recSetting = False

    mode = input('Would you like to play classic or custom? ')
    while (not(mode == 'classic' or mode == 'custom')):
        mode = input('Try choosing a mode again by typing it exactly as written : ')

    if (mode == 'custom'):
        ds  = input('What sided dice would you like to play with? (max 20): ')
        while (not(ds.isnumeric() and int(ds) <= 20 and int(ds) > 0)):
            ds = input('Please enter a valid number: ')
        bs  = input('What size of game board would you like to play with? (max 30): ')
        while (not(bs.isnumeric() and int(bs) <= 30 and int(bs) > 0)):
            bs = input('Please enter a valid number: ')

        ai.DICESIDES = int(ds)
        ai.BOARDSIZE = int(bs)

    ai.remake_board()

    dice1 = random.randint(1,ai.DICESIDES)
    dice2 = random.randint(1,ai.DICESIDES)
    playing = True
    while (playing):
        while ai.game_value(dice1+dice2) == 0:
            ai.print_board()

            for i in range(20):
                if (i!=19):
                    print("\rYour Roll: " + str(random.randint(1,9)) + " " + str(random.randint(1,9)), end='')
                    sys.stdout.flush()
                    time.sleep(0.1)
                else:
                    print("\rYour Roll:", dice1, dice2)

            aiMove = ai.get_move(dice1+dice2)
            if aiMove =="":
                break;
            if recSetting:
                print('AI Reccomendation:', aiMove)
            move = input('Enter your move: ')
            while ai.make_move(move, (dice1 + dice2)) == False:
                move = input('Invalid input please try again: ')
            print()

            dice1 = random.randint(1,ai.DICESIDES)
            dice2 = random.randint(1,ai.DICESIDES)

        if ai.game_value(dice1 + dice2)==1:
            print('You Win!')
        else:
            print('You Lose :(')
        print()
        answer = input('Would you like to play again? (y/n) ')
        while not(answer == 'y' or answer == 'n'):
            answer = input('Please answer y or n ')
        if answer == 'n':
            playing = False
        ai.remake_board()

if __name__ == "__main__":
    main()
