from flask import Flask
from flask import request
import requests
import random
import ast

board = {}
board['A1'] = '    '
board['A2'] = '    '
board['A3'] = '    '
board['B1'] = '    '
board['B2'] = '    '
board['B3'] = '    '
board['C1'] = '    '
board['C2'] = '    '
board['C3'] = '    '

def clearboard(board):
 board['A1'] = '    '
 board['A2'] = '    '
 board['A3'] = '    '
 board['B1'] = '    '
 board['B2'] = '    '
 board['B3'] = '    '
 board['C1'] = '    '
 board['C2'] = '    '
 board['C3'] = '    '


def printboard(board):
 print('             ')
 print('      1   2   3 ')
 print('                   ')
 print(' A ' + board['A1'] + '|' + board['A2'] + '|' + board['A3'])
 print('     ----------')
 print(' B ' + board['B1'] + '|' + board['B2'] + '|' + board['B3'])
 print('     ----------')
 print(' C ' + board['C1'] + '|' + board['C2'] + '|' + board['C3'])
 print('                   ')

#Checks if the move given is invalid
def invalid_move(move, board):
 if move == 'A1' or 'A2' or 'A3' or 'B1' or 'B2' or 'B3' or 'C1' or 'C2' or 'C3':
     if board[move] == '    ':
         return False
     else:
         return True
 else:
     return True


def game_result(board):
 combinations = [['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'], ['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3'], ['A1', 'B2', 'C3'], ['C1', 'B2', 'A3']]
 for combo in combinations:
    if board[combo[0]] == board[combo[1]] == board[combo[2]] == ' X ':
       return (True, ' X ')
    if board[combo[0]] == board[combo[1]] == board[combo[2]] == ' O ':
       return (True, ' O ')
 keys = board.keys()
 for key in keys:
    if board[key] != '    ':
       return False
 return (True, 'Draw')

#Checks if the player or bot has a winning move
#If the player has the winning move, the bot will put its marker there
def winning_move(board, marker):
 keys = list(board.keys())
 for key in keys:
     if board[key] == '    ':
         board[key] = marker
         win = game_result(board)
         if win == (True, marker):
             board[key] = '    '
             return key
         else:
             board[key] = '    '
 return False

#Finds a random move for the bot if no other move is beneficial
def random_move(board, moves):
 clear_moves = []
 for move in moves:
     if board[move] == '    ':
         clear_moves.append(move)
 if len(clear_moves) != 0:
     clear_move = random.choice(clear_moves)
     return clear_move
 else:
     return None

#Asks the user for a move
def player_move(board, player_marker):
    if player_marker == ' X ':
        marker = 'X'
    else:
        marker = 'O'
    move = input(marker + ', ' + "Please enter a move:")
    check = invalid_move(move, board)
    if check == True:
        move = input("Invalid move: Enter a different move:")
    board[move] = player_marker

def bot_move(board, bot_marker, player_marker):
    if board['B2'] == '    ':
        board['B2'] = bot_marker
        return 'B2'
    else:
         result = winning_move(board, bot_marker)
         if result != False:
             board[result] = bot_marker
             return result
         else:
             result = winning_move(board, player_marker)
             if result != False:
                 board[result] = bot_marker
                 return result
             else:
                move = random_move(board, list(board.keys()))
                board[move] = bot_marker
                return move

def winner(board):
    result = game_result(board)
    if result == (True, ' X '):
        print("X is the winner.")
        game_over = True
        return game_over
    if result == (True, ' O '):
        print("O has won.")
        game_over = True
        return game_over
    if result == (True, 'Draw'):
        print("The game is a draw.")
        game_over = True
        return game_over
    if result == False:
        game_over = False
        return game_over

def replay():
    choice = input("Would you like to play another game? (yes,no)")
    if choice == 'yes':
        return "replay"
    else:
        return "over"

app = Flask("server")

def run_client(board, player_marker):
    url = "http://127.0.0.1:5000/command"
    move = input("Please enter a move:")
    check = invalid_move(move, board)
    if check == True:
        move = input("That move is invalid. Please enter a different move:")
    dict = {}
    dict['message'] = 'move'
    dict['marker'] = player_marker
    dict['move'] = move
    board[move] = player_marker
    response = requests.post(url, dict)
    print(response.text)
    bot_dict = ast.literal_eval(response.text)
    bot_move = bot_dict["move"]
    bot_marker = bot_dict["marker"]
    board[bot_move] = bot_marker
    printboard(board)


@app.route('/command', methods=["POST"])
def command():
    player_dict = request.form
    print(request.form)
    marker = ' O '
    player_move = player_dict['move']
    player_marker = player_dict['marker']
    board[player_move] = player_marker
    move = bot_move(board, marker, player_dict['marker'])
    printboard(board)
    dict = {}
    dict['message'] = 'move'
    dict['marker'] = marker
    dict['move'] = move
    result = game_result(board)
    return dict

choice = input("Would you like to play against the bot(c)? Against another player(p)? Or against a bot using server and client(s)?:")

if choice == 'c':
 player_marker = input("Would you like to be X or O:")
 if player_marker == 'X':
     bot_marker = ' O '
     player_marker = ' X '
     player_move(board, ' X ')
 else:
     bot_marker = ' X '
     player_marker = ' O '

if choice == 'c':
    printboard(board)
    result = game_result(board)
    if result == False:
        while(True):
          bot_move(board,bot_marker,player_marker)
          player_move(board, player_marker)
          printboard(board)
          result = game_result(board)
          if result == True:
              result = replay()
              if result != 'replay':
                  break
              else:
                clearboard(board)
                printboard(board)

if choice == 's':
    printboard(board)
    repeat = 'yes'
    flask_choice = input("Server or client?:")
    while (True):
        while (True):
            if flask_choice == 'client':
             run_client( board, " X " )
             result = winner(board)
             if result == True:
                 break
            if flask_choice == 'server':
             app.run()
             result = winner(board)
             if result == True:
                 resetboard(board)
                 printboard(board)
                 break
        result = replay()
        if result != 'replay':
            break
        else:
            resetboard(board)
            printboard(board)

if choice == 'p':
 while (True):
     player_move(board, ' X ')
     printboard(board)
     result = winner(board)
     if result == True:
         result = replay()
         if result != 'replay':
             break
         else:
             clearboard(board)
             printboard(board)
     player_move(board, ' O ')
     printboard(board)
     result = winner(board)
     if result == True:
         result = replay()
         if result != 'replay':
             break
         else:
             clearboard(board)
             printboard(board)