'''
CSE Honors Project 1
"Dots and Boxes"

Algorithm:
    class Board:
        init
        str
        display_board:
            data structure to display the board of any size
        check_for_boxes:
            check how many boxes each move creates on the grid
        is_valid_move:
            check if the given input move is valid
        update_board:
            update the lists keeping track of data of the board
        win:
            return true if the game is won by either player
    class Random_Player:
        __init__
        __str__
        play_move:
            generate a random valid move for the player
        score:
            return current score of the player
        add_point:
            add number of new boxes created to the player score
    class Game:
        __inti__
        single_player:
            Play a single game with and output data to a file
        multiple_player:
            Play multiple games and output data to a file
        coin_flip:
            choose p1 or p2 using random choice command
    main:
        display welcome message
        prompt for grid size, random seed, and number of muliple games
        create files for output
        create new game object and call single and multi-play functions
        display ending message
                                    
'''


import random


class Board(object):
    '''
    Create a board to save current game data
    '''

    def __init__(self, size):
        '''
        Initialize board size and make 3 lists that save data for displaying
        the board and keep score
        '''
        self.size = int(size)
        self.ver_lst = [' ']*(size*(size-1))    #Store '|' character
        self.hor_lst = [' ']*(size*(size-1))    #Store '-' character
        self.score_lst = [' ']*((size-1)**2)    #Store A or B character
        self.master = [self.ver_lst, self.hor_lst, self.score_lst]
        self.moves_lst = [] #Store played moves

    def __str__(self):
        '''
        Display board size, score list and master list with vertical and 
        horizontal lines
        '''
        return "Board(size:{}, score list:{}, master list:{})".\
            format(self.size, self.score_lst, self.master)
    
    def display_board(self, fp):
        '''
        display board as the current state using the lists containing
        horizonal and vertical lines and the scores
        '''
        padding = len(str(((self.size**2)-1)))  #padding to allign the board

        vindex = 0
        hindex = 0
        sindex = 0
        
        #Print the board using the 3 lists in proper format
        for i in range(self.size**2):
            if ((i+1)%self.size)!=0:
                print('{:>{pad}}'.format(i, pad=padding), ' ', end='', file=fp)
                print(self.hor_lst[hindex], '', end='', file=fp)
                hindex +=1
            else:
                print('{:>{pad}}'.format(i, pad=padding), file=fp)
                if (i<(self.size*(self.size-1))):
                    for j in range(self.size):
                        if j<(self.size-1):
                            print('{:>{pad}s}'.format(self.ver_lst[vindex],\
                                    pad=padding), '', self.score_lst[sindex],\
                                  '', end='', file=fp)
                            vindex += 1
                            sindex += 1
                        else:
                            print('{:>{pad}s}'.format(self.ver_lst[vindex],\
                                                      pad=padding), file=fp)
                            vindex+= 1

                  
    def check_for_box(self, move, moves_lst, player_code): 
        '''
        check for the number of new boxes completed after a new move is made
        if the move is a vertical line, check for the boxes to the right and
        left of the new line
        if the move is a horizontal line, check for the boxes above and below
        the new line
        check less boxes if the new move is a line on the edge
        Also updated the score list keeping a track of A or B letters on the 
        board
        return: number of new boxes created
        '''
        #check if the move made was vertical or horizontal
        if (move[1]-move[0])==1:
            is_vert = False
        else:
            is_vert = True
            
        complete_box = 0
        
        if not is_vert:
            if move[0]<self.size:
                #check box below the horizontal line
                if [move[0], move[0]+self.size] in moves_lst and\
                    [move[1], move[1]+self.size] in moves_lst and\
                        [move[0]+self.size, move[1]+self.size] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)] = player_code
                    
            elif move[0]>=(self.size*(self.size-1)):
                #check box above the horizontal line
                if [move[0]-self.size, move[0]] in moves_lst and\
                    [move[1]-self.size, move[1]] in moves_lst and\
                        [move[0]-self.size, move[1]-self.size] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-self.size-(move[0]//self.size)+1]\
                        = player_code
            else:
                #check box above the horizontal line
                if [move[0]-self.size, move[0]] in moves_lst and\
                    [move[1]-self.size, move[1]] in moves_lst and\
                        [move[0]-self.size, move[1]-self.size] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-self.size-(move[0]//self.size)+1]\
                        = player_code
                    
                #check box below the horizontal line
                if [move[0], move[0]+self.size] in moves_lst and\
                    [move[1], move[1]+self.size] in moves_lst and\
                        [move[0]+self.size, move[1]+self.size] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)] = player_code
                    
        if is_vert:
            if move[0]%self.size == 0:
                #check box to the right of the vertical line
                if [move[0], move[0]+1] in moves_lst and\
                    [move[1], move[1]+1] in moves_lst and\
                        [move[0]+1, move[1]+1] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)] = player_code
                    
            elif (move[0]+1)%self.size == 0:
                #check box to the left of the vertical line
                if [move[0]-1, move[0]] in moves_lst and\
                    [move[1]-1, move[1]] in moves_lst and\
                        [move[0]-1, move[1]-1] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)-1]\
                        = player_code
            else:
                #check box to the right of the vertical line
                if [move[0], move[0]+1] in moves_lst and\
                    [move[1], move[1]+1] in moves_lst and\
                        [move[0]+1, move[1]+1] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)] = player_code
                    
                #check box to the left of the vertical line
                if [move[0]-1, move[0]] in moves_lst and\
                    [move[1]-1, move[1]] in moves_lst and\
                        [move[0]-1, move[1]-1] in moves_lst:
                    complete_box += 1
                    self.score_lst[move[0]-(move[0]//self.size)-1]\
                        = player_code
                    
        return complete_box     #return number of new boxes completed
            
            
    def is_valid_move(self, move, moves):
        '''
        Checks if a move is valid.
        '''
        
        if move in moves:
            return False
        
        #if both numbers are inside limits of the grid
        if 0<=move[0]<=self.size**2-1 and 0<=move[1]<=self.size**2-1:
            #if two number differ in 1 (like 12 and 13)
            if move[1]==move[0]+1:
                #if the 2nd divided by grid not equals zero
                # (means the 2nd is not on the next line)
                if move[1]%self.size!=0:
                    return True
                else:
                    return False
            #if the 1st+grid equals the 2nd
            elif move[1]==move[0]+self.size:
                return True
            else:
                return False
        else:
            return False
    
    def update_board(self, move):
        '''
        Update the lists keeping the data for the horizontal and 
        vertical lines 
        '''
        #Check if the new move was vertical or horizontal
        if (move[1]-move[0])==1:
            is_vert = False
        else:
            is_vert = True
            
        if is_vert:
            self.ver_lst[move[0]] = '|'
        else:
            self.hor_lst[move[0]-(move[0]//self.size)] = '-'
            
    def win(self):
        '''
        Check if the game is won
        '''
        
        w=" "
        if w in self.score_lst :
            return False
        else:
            return True
  
        
class RandomPlayer(object):
    '''
    Create a Player to play random valid moves
    '''
    
    def __init__(self, size, code):
        '''
        Initialize the player with board size, score = 0 and code(A or B)
        '''
        self.player_score = 0
        self.size = size
        self.code = code
        
    def __str__(self):
        '''
        return a string containing players score, board size and players code
        '''
        
        return "Player(score:{}, size:{}, code:{})"\
            .format(self.player_score, self.size, self.code)
    
    def play_move(self, moves_list, brd):
        '''
        create a new random valid move and play the move by updating the 
        board
        '''
        
        num = (brd.size**2)-1
        while True:
            rand1 = random.randint(0, num)
            rand_lst = [rand1-1, rand1+1, rand1-brd.size, rand1+brd.size]
            rand2 = random.choice(rand_lst)
            new_move = [rand1, rand2]
            if brd.is_valid_move(new_move, moves_list):
                brd.update_board(new_move)  #Update the board if move is valid
                return new_move
                
            else:
                continue
          
    def score(self): 
        '''
        return the score for the specific player
        '''
        
        return self.player_score


    def add_point(self, move, moves_lst, brd): 
        '''
        check number of new boxed created and add that as points to the 
        player score
        '''
        
        self.player_score += brd.check_for_box(move, moves_lst, self.code)
        

class Game(object): 
    '''
    create a game object to play single and multiple games
    '''
    
    def __init__(self, size):
        '''
        initialize the size of the board
        '''
        
        self.size = size
    
    def single_play(self, fp):
        '''
        Play a single game with two random players. Output state of the board
        at every turn with the scores of both players.
        '''
        
        print("Single play mode data: \n", file = fp)
        
        p1 = RandomPlayer(self.size, 'A')   #Initialize player 1
        p2 = RandomPlayer(self.size, 'B')   #Initialize player 2
        
        turn = Game.coin_flip(self, p1, p2) #Coin flip
        print("Coin-flip won by player: ", turn.code, file=fp)
        
        b = Board(self.size)    #create a board for the game
        
        while not b.win():  #Itterate till a player wins the game
            print("Current Board:", file=fp)
            b.display_board(fp)
            
            print("score of player A: ", p1.score(), file=fp)
            print("score of player B: ", p2.score(), file=fp)
            print("Turn of player: ", turn.code, file=fp)
            
            move = turn.play_move(b.moves_lst, b) #Make a valid random move
            #check how many new boxes were created
            box = b.check_for_box(move, b.moves_lst, turn.code)
            
            print("Board after move by player ", turn.code, file=fp)
            b.display_board(fp)
            
            print("Boxes completed by player", turn.code,": ", box, file=fp)
            
            print('---------------------------------------------\n', file=fp)
            
            #Add points to respective player
            turn.add_point(move, b.moves_lst, b)
            b.moves_lst.append(move)    #Add the move to the moves list
            
            #Change player turn if no new box was made
            if box != 0:
                continue
            else:
                if turn is p1:
                    turn = p2
                else:
                    turn = p1
                    
        print("FINAL BOARD", file=fp)
        print("Final score of player A:",p1.score(), file=fp)
        print("Final score of player B:",p2.score(), file=fp)
        b.display_board(fp)
        
        #Display who won the game
        if p1.score() > p2.score():
            print("\nPlayer A won!!!", file=fp)
        elif p2.score() > p1.score():
            print("\nPlayer B won!!!", file=fp)
        else:
            print("\nIt was a tie!!!", file=fp)
    
    def multiple_play(self, fp, no_of_games):
        '''
        Play a given number of games with two random players and return 
        analyzed data from all the games for both players.
        '''
        
        print("Multiple Play mode data: ", file = fp)
        
        A_scores = []
        B_scores = []
        a_start = 0
        b_start = 0
        won_a = 0
        won_b = 0
        tie = 0
    
        for i in range(no_of_games):

            p1 = RandomPlayer(self.size, 'A')   #Initialize player 1
            p2 = RandomPlayer(self.size, 'B')   #Initialize player 2
            
            turn = Game.coin_flip(self, p1, p2) #Coin flip
            if turn is p1:
                a_start += 1
            else:
                b_start += 1
            
            b = Board(self.size)    #create a board for the game
            
            while not b.win():  #Itterate till a player wins the game
                move = turn.play_move(b.moves_lst, b)
                box = b.check_for_box(move, b.moves_lst, turn.code)
                turn.add_point(move, b.moves_lst, b)
                b.moves_lst.append(move)
                
                #Change player turn if no new box was made
                if box != 0:
                    continue
                else:
                    if turn is p1:
                        turn = p2
                    else:
                        turn = p1
            
            #Create lists of scores of A and B for every game
            A_scores.append(p1.score())
            B_scores.append(p2.score())
            
            if p1.score() > p2.score():
                won_a += 1
            elif p2.score() > p1.score():
                won_b += 1
            else:
                tie += 1
            
        avg_score_a = sum(A_scores)/no_of_games
        avg_score_b = sum(B_scores)/no_of_games
        avg_overall = ((sum(A_scores)+sum(B_scores))/no_of_games)
        
        A_scores.sort()
        B_scores.sort()
        
        median_A = A_scores[no_of_games//2]
        median_B = B_scores[no_of_games//2]
        all_list = A_scores + B_scores
        all_list.sort()
        median_overall = all_list[(2*no_of_games)//2]
        
        high_A = A_scores[-1]
        high_B = B_scores[-1]
        low_A = A_scores[0]
        low_B = B_scores[0]
        
        print("Number of games played:", no_of_games, file=fp)
        print(file=fp)
        
        print("Average score of Player A:", avg_score_a, file=fp)
        print("Average score of Player B:", avg_score_b, file=fp)
        print("Average overall score:", avg_overall, file=fp)
        print(file=fp)
        
        print("Median score for Player A:", median_A, file=fp)
        print("Median score for Player B:", median_B, file=fp)
        print("Median overall score:", median_overall, file=fp)
        print(file=fp)
        
        print("Highest score for Player A:", high_A, file=fp)
        print("Highest score for Player B:", high_B, file=fp)
        print("Lowest score for Player A:", low_A, file=fp)
        print("Lowest score for Player B:", low_B, file=fp)
        print(file=fp)
        
        print("A started", a_start, "times.", file=fp)
        print("B started", b_start, "times.", file=fp)
        print(file=fp)
        
        print("A won {} games, B won {} games and {} games ended in a tie."\
              .format(won_a, won_b, tie), file=fp)
        
    def coin_flip(self, ch1, ch2): 
        '''
        flip a coin to choose if A or B goes first
        '''
        
        return random.choice([ch1, ch2])


def main():
    
    print("Welcome to Dots and Boxes!!\n")
    
    grid_size = int(input("Enter grid size for the games: "))
    rand_seed = int(input("Enter a random seed integer: "))
    mult_play = int(input("Enter number of multiple games to be played: "))
    
    print("Please wait while the output is generated.")
    print("This will take a few seconds.....")
    
    file_single = open('single_play.txt', 'w')
    file_multiple = open('multiple_play.txt', 'w')
    
    random.seed(rand_seed)
    
    new_game = Game(grid_size)
    new_game.single_play(file_single)
    new_game.multiple_play(file_multiple, mult_play)
    
    print("\nGame result outputs have been created in the same directory"+ \
          " as this python file.")
    
if __name__ == "__main__": 
    main()