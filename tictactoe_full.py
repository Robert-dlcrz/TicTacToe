# Example of what we are currently trying to biuld: 

# players X and O have started the game
# Here is the board:
# _ | _ | _
# _ | _ | _
# _ | _ | _
# Player x, what do you want to play? upper right
# here is the board:
# _ | _ | X
# _ | _ | _
# _ | _ | _
# Player O, what do you want to play? upper right
# Invalid piece, try again: bottom left
# _ | _ | X
# _ | _ | _ 
# O | _ | _

# https://github.com/ganeshramg/Tkinter-TicTacToe/blob/master/tictactoe.py

from tkinter import *

WINNING_COMBOS = [
    ['UL', 'UM', 'UR'], 
    ['UL', 'ML', 'BL'], 
    ['UL', 'MM', 'BR'],
    ['UM', 'MM', 'BM'],
    ['UR', 'MM', 'BL'], 
    ['UR', 'MR', 'BR'],
    ['MR', 'MM', 'ML'],
    ['BR', 'BM', 'BL']
] 

COORDINATES = {             
    'UL': [0,0], # upper left
    'UM': [0,1],
    'UR': [0,2],
    'ML': [1,0],
    'MM': [1,1],
    'MR': [1,2],
    'BL': [2,0],
    'BM': [2,1],
    'BR': [2,2]
}

GUI_COORDINATES = {
    'UL': ( range(0, 100),   range(0, 100)   ), 
    'UM': ( range(100, 200), range(0, 100)   ),  
    'UR': ( range(200, 300), range(0, 100)   ), 
    'ML': ( range(0, 100),   range(100, 200) ),
    'MM': ( range(100, 200), range(100, 200) ),
    'MR': ( range(200, 300), range(100, 200) ),
    'BL': ( range(0, 100),   range(200, 300) ),
    'BM': ( range(100, 200), range(200, 300) ),
    'BR': ( range(200, 300), range(200, 300) )
}

class Gameboard:

    def __init__(self):
        self.board = [[-1, -1, -1],
                      [-1, -1, -1], 
                      [-1, -1, -1]]

    def __str__(self):
        def parsePiece(piece):
            if piece == -1:
                return '_'
            else:
                return piece
        boardStr = ''
        for row in self.board:
            boardStr += f'{parsePiece(row[0])} | {parsePiece(row[1])} | {parsePiece(row[2])}\n'
        return boardStr

    def input_move(self, x, y, player):
        self.board[x][y] = player

    def get_tile_value(self, x, y):
        return self.board[x][y]  

    def winner_exists(self):

        def all_equal(list_):
            first_item = list_[0]
            for item in list_[1:]:
                if item != first_item:
                    return False
                if item == -1: # unfilled
                    return False
            return True   

        for combo in WINNING_COMBOS:
            tiles_of_interest = [] 
            for coordinate in combo:
                coordinates = COORDINATES[coordinate]  
                x = coordinates[0] 
                y = coordinates[1]  
                tile = self.get_tile_value(x, y)
                tiles_of_interest.append(tile)
            if all_equal(tiles_of_interest):
                return True
        return False 
    
def player_move(event):
    x = event.x
    y = event.y
    tile = None
    for alias, coordinates in GUI_COORDINATES.items():
        if x in coordinates[0] and y in coordinates[1]:
            tile = alias
    print(tile)
    assert tile is not None, f'Tile is None, coordinates are x: {x} and y: {y}'

if __name__ == '__main__':
    root = Tk()
    root.geometry('600x300')
    # root.minsize(300, 300)
    root.title('Tic Tac Toe')
    # root.resizable(0, 0)

    # tic tac toe
    gameFrame = Frame(root, width=300, height=300, bg='red')
    gameFrame.grid(rowspan=2, column=0) # rowspan is not 0 based
    canvas = Canvas(gameFrame, height=300, width=300, bd=0)
    canvas.pack(anchor=CENTER)
    canvas.create_line(100, 0, 100, 300, width=5)
    canvas.create_line(200, 0, 200, 300, width=5)
    canvas.create_line(0, 100, 300, 100, width=5)
    canvas.create_line(0, 200, 300, 200, width=5)
    canvas.bind("<Button-1>", player_move)    

    # title
    titleFrame = Frame(root, width=300, height=100, bg='blue')
    titleFrame.grid(row=0, column=1)

    # score
    scoreFrame = Frame(root, width=300, height=200, bg='pink')
    scoreFrame.grid(row=1, column=1)

    gameName = Label(titleFrame, text='Tic Tac Toe', font='Times 20 bold')
    gameName.pack()

    scoreX = Label(scoreFrame, text='X: 0', font='Times 20 bold')
    scoreX.grid(row=0, column=0)
    scoreY = Label(scoreFrame, text='Y: 0', font='Times 20 bold')
    scoreY.grid(row=1, column=0)

    root.mainloop()



