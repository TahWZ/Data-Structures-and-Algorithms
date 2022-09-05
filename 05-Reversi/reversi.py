#Name: Tah Wen Zhong
#StudentID: 29940672

#Assignment 1:
#Task 2:Reversi

#Board variables
import copy
board=[]
rows=[]
for number in range(1,9):
    rows.append(number)
#print(rows)

cols=[]
for letter in range(97,105):
    cols.append(chr(letter))
#print(cols)

Dcols=""

#e=0
#b=1
#w=2

#//A

#Resets the board
def new_board():
    board=[]
    for i in range(8):
        board.append([0]*8)
    board[3][3]=2
    board[4][3]=1
    board[3][4]=1
    board[4][4]=2
    '''board[3][6]=2
    board[3][7]=1
    board[2][5]=2
    board[1][5]=2
    board[0][5]=1'''
    return board

#Prints board configuration 
def print_board(board):
    '''
    How the game should be displayed:
                
        +---+---+---+
      8 | W | B | ● |
        +---+---+---+ ...
          a   b   c
    '''
    #Number to Color
    col_board=[]
    for i in range(len(board)):
        col_row=[]
        for j in range(len(board[0])):
            if board[i][j] == 0:
                col_row.append(" ")
            elif board[i][j] == 1:
                col_row.append("B")
            elif board[i][j] == 2:
                col_row.append("W")
        col_board.append(col_row)

    #Top layer
    setup="  "
    for i in range(8):
        setup+="+---"
    setup+="+"
    print(setup)

    #Mid layer
    for i in range(8):
        setup=""
        setup+=str(rows[i])+ " |"
        for j in range(8):
            display=col_board[i][j]
            setup+=" "+ str(display) +" |"    
        #col_board+="+"
        print(setup)
        setup="  "
        for k in range(8):
            setup+="+---"
        setup+="+"
        print(setup)

    #Bottom layer
    setup="    "
    for i in range(8):
        setup+=cols[i]+"   "
    print(setup)

#Returns s1 and s2 (Number of stones)
def score(board):
    s1=0
    s2=0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                s1+=1
            elif board[i][j] == 2:
                s2+=1
    return s1,s2

#//B

#Player 1 is black,Player 2 is white

#Directions Information:
##[0,1] is right,[0,-1] is left,[1,0] is down,[-1,0] is up
##[-1,1] is up right,[-1,-1] is up left
##[1,1] is down right,[1,-1] is down left

'''Tpos=[3,5]'''
'''directs=[[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
players=[1,2]
player=players[0]'''
#direct=[0]*2
#player=1
def enclosing(board,player,pos,direct):    
        if board[pos[0]][pos[1]] == 0:
            Apos=copy.deepcopy(pos)
            Apos[0]+=direct[0]
            Apos[1]+=direct[1]
            if Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8:
                if board[Apos[0]][Apos[1]]== player:
                    return False
                elif board[Apos[0]][Apos[1]] == 0:
                    return False
                else:
                    while Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8: 
                        Apos[0]+=direct[0]
                        Apos[1]+=direct[1]
                        if Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8:
                            if board[Apos[0]][Apos[1]] == 0:
                                return False
                                break
                            elif board[Apos[0]][Apos[1]] == player:
                                return True
                                break
                    return False
            
def valid_moves(board,player):
    valid = None
    valid_pos=[]
    directs=[[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    direct=[]
    for i in range(len(board)):
        for j in range(len(board[0])):
            Allpos=[]
            Allpos.append(i)
            Allpos.append(j)
            for UD,LR in directs:
                direct.insert(0,UD)
                direct.insert(1,LR)
                valid=enclosing(board,player,Allpos,direct)
                if valid == True:
                    valid_pos.append(Allpos)
                    break
    return valid_pos
    
def next_state(board,player,pos):
    directs=[[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    next_board=copy.deepcopy(board)
    next_player=0
    conv=[]
    for UD,LR in directs:
        cap=[]
        Apos=copy.deepcopy(pos)
        Apos[0]+=UD
        Apos[1]+=LR
        if Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8:
            cap.append(copy.deepcopy(Apos))
            if board[Apos[0]][Apos[1]] != player and board[Apos[0]][Apos[1]] != 0:
                while Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8:
                    Apos[0]+=UD
                    Apos[1]+=LR
                    if Apos[0]>-1 and Apos[0]<8 and Apos[1]>-1 and Apos[1]<8:
                        if board[Apos[0]][Apos[1]] == 0:
                            cap=[]
                            break
                        elif board[Apos[0]][Apos[1]] == player:
                            conv.extend(copy.deepcopy(cap))
                            break
                        cap.append(copy.deepcopy(Apos))
    for row,col in conv:
        next_board[row][col]=player
    next_board[pos[0]][pos[1]]=player
    players = [1,2,0]
    if player == players[0]:
        next_player = players[1]
    elif player == players[1]:
        next_player = players[0]
    if valid_moves(board,1)==[]:
        if valid_moves(board,2)==[]:
            next_player = players[2]
    return next_board,next_player

#//C

def position(string):
    cols=[]
    for letter in range(97,105):
        cols.append(chr(letter))
    rows=[]
    for number in range(1,9):
        rows.append(str(number))
    valid_pos=[]
    if len(string) != 2:
        return None
    elif string[0] not in cols:
        return None
    elif string[1] not in rows:
        return None
    else:
        for i in range(len(rows)):
            if rows[i]==string[1]:
                valid_pos.append(i)
        for i in range(len(cols)):
            if cols[i]==string[0]:
                valid_pos.append(i)
        return valid_pos

def run_two_players():
    board=new_board()
    print_board(board)
    player=1
    players=[1,2]
    while player != 0:
        if valid_moves(board,player) == []:
            print("No valid moves, Player " + str(player) + " skips a turn")
            if player == players[0]:
                player = players[1]
            elif player == players[1]:
                player = players[0]
        print("Player "+str(player)+"'s turn")
        valid_pos=False
        validation=False
        user_input=input("Please enter board position: ")
        if user_input == "q":
            quit()
        valid_pos=position(user_input)
        while validation==False:
            if valid_pos in valid_moves(board,player):
                validation=True
            else:
                user_input=input("Please enter valid board position: ")
                valid_pos=position(user_input)
                if user_input == "q":
                    quit()
        board=next_state(board,player,valid_pos)[0]
        player=next_state(board,player,valid_pos)[1]
        print_board(board)
    print("Game has ended,")
    print("Player 1's score:" + str(score(board)[0]))
    print("Player 2's score:" + str(score(board)[1]))

def run_single_player():
    board=new_board()
    print_board(board)
    player=1
    players=[1,2]
    while player != 0:
        if valid_moves(board,player) == []:
            print("No valid moves, Player " + str(player) + " skips a turn")
            if player == players[0]:
                player = players[1]
            elif player == players[1]:
                player = players[0]
        if player == 1:
            print("Player "+str(player)+"'s turn")
            valid_pos=False
            validation=False
            user_input=input("Please enter board position: ")
            if user_input == "q":
                quit()
            valid_pos=position(user_input)
            while validation==False:
                if valid_pos in valid_moves(board,player):
                    validation=True
                else:
                    user_input=input("Please enter valid board position: ")
                    if user_input == "q":
                        quit()
                    valid_pos=position(user_input)
        if player == 2:
            print("Player "+str(player)+"'s turn")
            Mscore=[]
            Mscore=valid_moves(board,player)[0]
            for i in range(len(valid_moves(board,player))):
                C_state=next_state(board,player,Mscore)[0]
                Current=score(C_state)[1]
                Nstate=next_state(board,player,valid_moves(board,player)[i])[0]
                New=score(Nstate)[1]
                if Current<New:
                    Mscore=valid_moves(board,player)[i]
            valid_pos=Mscore
        board=next_state(board,player,valid_pos)[0]
        player=next_state(board,player,valid_pos)[1]
        print_board(board)
    print("Game has ended,")
    print("Player 1's score:" + str(score(board)[0]))
    print("Player 2's score:" + str(score(board)[1]))

#///FOR FUN TESTS!!! xD (No player mode runs an EXTREMELY fast game between AI's which can help to check for errors MUCH FASTER!!!)
    
##def run_no_player():
##    board=new_board()
##    print_board(board)
##    player=1
##    players=[1,2]
##    while player != 0:
##        if valid_moves(board,player) == []:
##            print("No valid moves, Player " + str(player) + " skips a turn")
##            if player == players[0]:
##                player = players[1]
##            elif player == players[1]:
##                player = players[0]
##        if player == 1:
##            print("Player "+str(player)+"'s turn")
##            Mscore=[]
##            Mscore=valid_moves(board,player)[0]
##            for i in range(len(valid_moves(board,player))):
##                C_state=next_state(board,player,Mscore)[0]
##                Current=score(C_state)[0]
##                Nstate=next_state(board,player,valid_moves(board,player)[i])[0]
##                New=score(Nstate)[0]
##                if Current<New:
##                    Mscore=valid_moves(board,player)[i]
##            valid_pos=Mscore
##        if player == 2:
##            print("Player "+str(player)+"'s turn")
##            Mscore=[]
##            Mscore=valid_moves(board,player)[0]
##            for i in range(len(valid_moves(board,player))):
##                C_state=next_state(board,player,Mscore)[0]
##                Current=score(C_state)[1]
##                Nstate=next_state(board,player,valid_moves(board,player)[i])[0]
##                New=score(Nstate)[1]
##                if Current<New:
##                    Mscore=valid_moves(board,player)[i]
##            valid_pos=Mscore
##        board=next_state(board,player,valid_pos)[0]
##        player=next_state(board,player,valid_pos)[1]
##        print_board(board)
##    print("Game has ended,")
##    print("Player 1's score:" + str(score(board)[0]))
##    print("Player 2's score:" + str(score(board)[1]))


def select_game_mode():
    gamemode=[0,1] #,2]
    user_select=int(input("Please enter, \n0 for Two players \n1 for Single player \nSelection:")) # \n2 for No player
    while user_select not in gamemode:
        user_select=int(input("Please enter a valid input(0,1): "))
    if user_select == 0:
        print("\n(Enter 'q' to quit the application anytime)")
        run_two_players()
    elif user_select == 1:
        print("\n(Enter 'q' to quit the application anytime)")
        run_single_player()
##    elif user_select == 2: #//Faster testing technique
##        run_no_player()
        
select_game_mode()


