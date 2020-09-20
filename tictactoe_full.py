from tkinter import *
from PIL import Image

X_JPG = r'iron_man.jpg'
TEMP_IMAGES = []

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

    def is_valid_move(self, x, y): 
        if self.get_tile_value(x, y) == -1:
            return True
        else:
            return False  

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

class Gameboard_GUI:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x300')
        # root.minsize(300, 300)
        self.root.title('Tic Tac Toe')
        # root.resizable(0, 0)

        # tic tac toe
        self.gameFrame = Frame(self.root, width=300, height=300, bg='red')
        self.gameFrame.grid(rowspan=2, column=0) # rowspan is not 0 based
        self.canvas = Canvas(self.gameFrame, height=300, width=300, bd=0)
        self.canvas.pack(anchor=CENTER)
        self.canvas.create_line(100, 0, 100, 300, width=5)
        self.canvas.create_line(200, 0, 200, 300, width=5)
        self.canvas.create_line(0, 100, 300, 100, width=5)
        self.canvas.create_line(0, 200, 300, 200, width=5)
        self.canvas.bind("<Button-1>", self.execute_player_move)    

        # title
        self.titleFrame = Frame(self.root, width=300, height=100, bg='blue')
        self.titleFrame.grid(row=0, column=1)

        # score
        self.scoreFrame = Frame(self.root, width=300, height=200, bg='pink')
        self.scoreFrame.grid(row=1, column=1)

        self.gameName = Label(self.titleFrame, text='Tic Tac Toe', font='Times 20 bold')
        self.gameName.pack()

        self.scoreX = Label(self.scoreFrame, text='X: 0', font='Times 20 bold')
        self.scoreX.grid(row=0, column=0)
        self.scoreY = Label(self.scoreFrame, text='Y: 0', font='Times 20 bold')
        self.scoreY.grid(row=1, column=0)

        self.turn = 1
        self.avatar_1 = PhotoImage(file='avatar2.gif')

        self.backend = Gameboard()

    def find_tile(self, x, y):
        for alias, coordinates in GUI_COORDINATES.items():
            if x in coordinates[0] and y in coordinates[1]:
                return alias
    
    def update_backend(self, tile):
        self.backend.input_move(*COORDINATES[tile], self.turn)
        return self.backend.winner_exists()

    def valid_move(self, tile):
        return self.backend.is_valid_move(*COORDINATES[tile])

    def execute_player_move(self, event):
        x = event.x
        y = event.y
        tile = self.find_tile(x, y)
        assert tile is not None, f'Tile is None, coordinates are x: {x} and y: {y}'
        if self.valid_move(tile):
            player_image = self.avatar_1 if self.turn == 1 else None # change later
            NW_x = GUI_COORDINATES[tile][0][0]
            NW_y = GUI_COORDINATES[tile][1][0]
            self.canvas.create_image(NW_x, NW_y, image=player_image, anchor=NW)
            winner_exists = self.update_backend(tile)
            print(winner_exists)

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    Gameboard_GUI().start()