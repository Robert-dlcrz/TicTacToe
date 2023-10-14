from tkinter import *
from PIL import ImageTk, Image

X_JPG = r'iron_man.jpg'
Y_JPG = r'batman.jpg'
AVATAR_SIZE = (100, 100)
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
        self.board = [[(-1,-1), (-1,-1), (-1,-1)],
                      [(-1,-1), (-1,-1), (-1,-1)], 
                      [(-1,-1), (-1,-1), (-1,-1)]]

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

    def inputMove(self, x, y, player):
        self.board[x][y] = player

    def getTileValue(self, x, y):
        return self.board[x][y] 

    def isValidMove(self, x, y): 
        if self.getTileValue(x, y)[0] == -1:
            return True
        else:
            return False  

    def winnerExists(self):
        # returns True if a winner exists (from the 8 winning combos)

        def allEqual(list_):
            firstItem = list_[0]
            for item in list_[1:]:
                if item != firstItem:
                    return False
                if item == -1: # unfilled
                    return False
            return True   

        for combo in WINNING_COMBOS:
            tilesOfInterest = [] 
            for coordinate in combo:
                coordinates = COORDINATES[coordinate]  
                x = coordinates[0] 
                y = coordinates[1]  
                tile = self.getTileValue(x, y)
                tilesOfInterest.append(tile)
            tileValues = [t[0] for t in tilesOfInterest]
            if allEqual(tileValues):
                return tilesOfInterest
        return False 
    
    def tieGame(self):
        # returns True if all tiles are filled but no winner
        allTiles = []
        for row in self.board:
            allTiles.extend([t[0] for t in row])
        return -1 not in allTiles 

    def reset(self):
        self.__init__()

class GameboardGUI:

    # Initialization functions ---------------------------------------------------------------------------

    def initializeWindow(self):
        self.root = Tk()
        self.root.geometry('600x300')
        # root.minsize(300, 300)
        self.root.title('Tic Tac Toe')
        # root.resizable(0, 0)
        
    def initializeGameFrame(self):
        self.gameFrame = Frame(self.root, width=300, height=300)
        self.gameFrame.grid(rowspan=3, column=0) # rowspan is not 0 based
        self.canvas = Canvas(self.gameFrame, height=300, width=300, bd=0)
        self.canvas.pack(anchor=CENTER)
        self.canvas.create_line(100, 0, 100, 300, width=5)
        self.canvas.create_line(200, 0, 200, 300, width=5)
        self.canvas.create_line(0, 100, 300, 100, width=5)
        self.canvas.create_line(0, 200, 300, 200, width=5)
        self.canvas.bind("<Button-1>", self.executePlayerMove) 

    def initializeTitleFrame(self):
        self.titleFrame = Frame(self.root, width=300, height=100, bg='blue')
        self.titleFrame.grid(row=0, column=1)
        self.gameName = Label(self.titleFrame, text='Tic Tac Toe', font='Times 20 bold')
        self.gameName.pack()

    def initializeScoreFrame(self):
        
        def createScore(playerName):
            score = StringVar()
            score.set(f'{playerName}: 0')
            return score

        self.p1Score = createScore(self.player1Name)
        self.p2Score = createScore(self.player2Name) 
        self.scoreFrame = Frame(self.root, width=300, height=100)
        self.scoreFrame.grid(row=1, column=1)
        self.scoreX = Label(self.scoreFrame, textvariable=self.p1Score, font='Times 20 bold')
        self.scoreX.grid(row=0, column=0)
        self.scoreY = Label(self.scoreFrame, textvariable=self.p2Score, font='Times 20 bold')
        self.scoreY.grid(row=1, column=0)

    def initializeRestartFrame(self):
        self.restartFrame = Frame(self.root, width=300, height=100)
        self.restartFrame.grid(row=2, column=1)
        self.restartButton = Button(self.restartFrame, text="Restart", fg="red", command=self.restartGame)
        self.restartButton.grid(row=0, column=0)
    
    def initializeAvatars(self):
        
        def initializeAvatar(path):
            avatar = Image.open(path)
            avatar = avatar.resize(AVATAR_SIZE)
            avatarTK = ImageTk.PhotoImage(avatar)
            return avatarTK 
        
        self.avatar1 = initializeAvatar(X_JPG)
        self.avatar2 = initializeAvatar(Y_JPG) 

    # ----------------------------------------------------------------------------------------------------

    def __init__(self):
        self.player1Name = 'X'
        self.player2Name = 'Y'
        self.backend = Gameboard()
        self.initializeWindow()
        self.initializeGameFrame() 
        self.initializeTitleFrame()
        self.initializeScoreFrame()
        self.initializeRestartFrame()
        self.initializeAvatars() 
        self.turn = 1
        self.blink = False
        self.gameOver = False

    def toggleTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def findTile(self, x, y):
        for alias, coordinates in GUI_COORDINATES.items():
            if x in coordinates[0] and y in coordinates[1]:
                return alias
    
    def updateBackend(self, tile, imgID):
        self.backend.inputMove(*COORDINATES[tile], (self.turn, imgID, tile))
        # print(self.backend.winnerExists())

    def updateScoreFrame(self):
        
        def updateScore(pScore):
            base = "".join(pScore.get().split(' ')[0:-1])
            points = int(pScore.get().split(' ')[-1])
            points += 1
            pScore.set(f'{base} {points}')

        if self.turn == 1:
            updateScore(self.p1Score)
        else:
            updateScore(self.p2Score)

    def validMove(self, tile): 
        return self.backend.isValidMove(*COORDINATES[tile])

    def blinkShowTile(self, tile):
        if not self.blink:
            return
        playerImage = self.avatar1 if self.turn == 1 else self.avatar2
        NW_x = GUI_COORDINATES[tile[2]][0][0]
        NW_y = GUI_COORDINATES[tile[2]][1][0]
        imgID = self.canvas.create_image(NW_x, NW_y, image=playerImage, anchor=NW, tags=('avatarImage'))
        tile[1] = imgID
        self.root.after(300, self.blinkHideTile, tile)

    def blinkHideTile(self, tile):
        if not self.blink:
            return
        self.canvas.delete(tile[1])
        self.root.after(300, self.blinkShowTile, tile) 

    def blinkTiles(self, tileIDs):
        self.blink = True
        tile = list(tileIDs[0])
        for tile in tileIDs:
            tile = list(tile)
            self.blinkHideTile(tile)

    def executePlayerMove(self, event):
        if self.gameOver:
            return 
        x = event.x
        y = event.y
        tile = self.findTile(x, y)
        assert tile is not None, f'Tile is None, coordinates are x: {x} and y: {y}'
        if self.validMove(tile):
            playerImage = self.avatar1 if self.turn == 1 else self.avatar2
            NW_x = GUI_COORDINATES[tile][0][0]
            NW_y = GUI_COORDINATES[tile][1][0]
            imgID = self.canvas.create_image(NW_x, NW_y, image=playerImage, anchor=NW, tags=('avatarImage'))
            self.updateBackend(tile, imgID)
            winnerTiles = self.backend.winnerExists()
            tie = self.backend.tieGame()
            if not winnerTiles and not tie:
                # if no winner exists and tiles still are open to play
                self.toggleTurn()
            else: 
                # when a winner exists or (a tied) game is over
                self.gameOver = True
                self.backend.reset()
                if winnerTiles:
                    # if someone actually WON the game ...
                    # this is what initiates the blinking of the 3 tiles 
                    self.updateScoreFrame()
                    self.root.after(450, self.blinkTiles, winnerTiles)
    
    def restartGame(self):
        self.gameOver = False
        self.blink = False
        self.backend.reset()
        self.canvas.delete('avatarImage')

    def start(self):
        self.root.mainloop()

if __name__ == '__main__':
    GameboardGUI().start()