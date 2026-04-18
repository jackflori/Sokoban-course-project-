from cmu_graphics import *
import copy

'''
Feature List:
- Main Menu, Win/Lose Screen
- Basic Sokoban Controls/Rules
- 3 Levels of Increasing Difficulty
- Reset Level with Enter
- Toggle Hard/Timed Mode
- Move Counter Displayed After Win
- Looped Background Music with Play/Pause Button
- Level Completion Sound Effect
 
Grading Shortcuts:
0: Menu Screen
1: Level 1
2: Level 2
3: Level 3
4: Win Screen
5: Lose Screen (hard mode)
'''

class Level:
    def __init__(self, board, balls, player):
        self.board = copy.deepcopy(board)
        self.balls = copy.deepcopy(balls)
        self.player = copy.copy(player)
        
    def move(self, app, direction):
        directionMap = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        drow, dcol = directionMap[direction]
        newPlayerRow = self.player[0] + drow
        newPlayerCol = self.player[1] + dcol
        
        # don't move if there's a wall
        if self.board[newPlayerRow][newPlayerCol] == 1:
            return
        
        # check if moving into a ball
        ballIndex = None
        for i in range(len(self.balls)):
            if self.balls[i] == [newPlayerRow, newPlayerCol]:
                ballIndex = i
                newBallRow = self.balls[i][0] + drow
                newBallCol = self.balls[i][1] + dcol
                break
        
        # move ball if possible
        if ballIndex != None:
            if self.board[newBallRow][newBallCol] == 1 or [newBallRow, newBallCol] in self.balls:
                return
            self.balls[ballIndex][0] = newBallRow
            self.balls[ballIndex][1] = newBallCol
        
        # move player
        self.player[0] = newPlayerRow
        self.player[1] = newPlayerCol
        app.moves += 1
    
    def checkWin(self):
        greenSpaces = self.findGreenSpaces()
        for coord in self.balls:
            if coord not in greenSpaces:
                return False
        return True
    
    def findGreenSpaces(self):
        greenSpaces = []
        rows = len(self.board)
        cols = len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 3:
                    greenSpaces.append([row, col])
        return greenSpaces

def onAppStart(app):
    # images
    app.menuPicURL = 'https://static01.nyt.com/images/2018/10/19/sports/19lakers1/merlin_145505325_b7cfbc30-21d7-4042-be42-0673bfeebcec-superJumbo.jpg'
    app.menuPicWidth, app.menuPicHeight = getImageSize(app.menuPicURL)
    app.playerURL = 'https://graphics.wsj.com/six-degrees-of-lebron-james/img/LeBron_head.jpg'
    app.playerWidth, app.playerHeight = getImageSize(app.playerURL)
    app.ballURL = 'https://www.citypng.com/public/uploads/preview/download-hd-basketball-ball-png-704081694878797nkckgheyr0.png'
    app.ballWidth, app.ballHeight = getImageSize(app.ballURL)
    app.winPicURL = 'https://i.pinimg.com/736x/13/09/9d/13099d4f2452b3f3b5d3422ea932cb6c.jpg'
    app.winPicWidth, app.winPicHeight = getImageSize(app.winPicURL)
    app.losePicURL = 'https://i.insider.com/5c000abbdde8676422780723?width=800&format=jpeg&auto=webp'
    app.losePicWidth, app.losePicHeight = getImageSize(app.losePicURL)
    
    # sounds
    app.winEffect = Sound('https://github.com/jflori-ctrl/112-project/raw/refs/heads/main/cash-register-kaching-376867.mp3')
    app.bgMusic = Sound('https://github.com/jflori-ctrl/112-project/raw/refs/heads/main/Alan%20Parsons%20Project%20-%20Sirius%20Instrumental%20-%20Eye%20in%20the%20Sky.mp3')
    app.bgMusic.play(loop=True)
    app.playing = True
    
    # draw board
    app.rows = app.cols = 11
    app.boardLeft = 50
    app.boardTop = 70
    app.boardWidth = 300
    app.boardHeight = 300
    app.colors = {1: 'lightGray', 2: 'white', 3: 'lightGreen'}
    app.button = False
    app.buttonColor = 'lightGray'
    
    # game data
    boardOne = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
        [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    boardTwo = [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [1, 3, 2, 2, 2, 2, 2, 2, 2, 1, 0],
        [1, 1, 1, 2, 2, 2, 2, 2, 3, 1, 0],
        [1, 3, 1, 1, 1, 2, 2, 2, 2, 1, 0],
        [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
        [1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 1, 3, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    boardThree = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 3, 2, 2, 2, 2, 2, 2, 2, 3, 1],
        [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
        [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
        [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
        [1, 3, 2, 2, 2, 2, 2, 2, 2, 3, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
    ballsOne = [[8, 1], [8, 2]]
    ballsTwo = [[2, 3], [3, 5], [4, 5], [7, 1], [8, 3]]
    ballsThree = [[5, 2], [5, 8], [2, 7], [5, 4]]
    playerOne = [9, 9]
    playerTwo = [2, 2]
    playerThree = [5, 5]
    app.levels = {1: Level(boardOne, ballsOne, playerOne), 2: Level(boardTwo, ballsTwo, playerTwo), 3: Level(boardThree, ballsThree, playerThree)}
    app.level = 0
    app.hardMode = False
    app.timer = 60
    app.stepsPerSecond = 1
    app.moves = 0
    
    # save inital states to reset board
    app.boards = {1: boardOne, 2: boardTwo, 3: boardThree}
    app.balls = {1: copy.deepcopy(ballsOne), 2: copy.deepcopy(ballsTwo), 3: copy.deepcopy(ballsThree)}
    app.players = {1: copy.copy(playerOne), 2: copy.copy(playerTwo), 3: copy.copy(playerThree)}
    
def redrawAll(app):
    drawRect(0, 0, 400, 400, fill='lightYellow')
    if app.playing:
        drawLine(15, 10, 15, 30)
        drawLine(25, 10, 25, 30)
        drawLabel('Playing', 22, 40, italic=True)
    if not app.playing:
        drawPolygon(14, 10, 14, 30, 34, 20)
        drawLabel('Paused', 22, 40, italic=True)
    if app.level == 0:
        drawLabel('Welcome to Sokoban!', 200, 50, size=36, font='grenze', bold=True)
        drawImage(app.menuPicURL, 200, 180, align='center', width=app.menuPicWidth//10, height=app.menuPicHeight//10)
        drawRect(200, 315, 100, 30, fill='red' if app.hardMode == False else 'green', border='black', align='center')
        drawLabel('Hard Mode', 200, 315, size=16, italic=True, bold=True)
        drawRect(200, 350, 100, 30, fill=app.buttonColor, border='black', align='center')
        drawLabel('Play Now', 200, 350, size=16, italic=True, bold=True)
    elif app.level == 4:
        drawLabel('You Win!', 200, 50, size=36, font='grenze', bold=True)
        drawLabel(f'Moves: {app.moves}', 200, 85, size=16, italic=True, bold=True)
        drawImage(app.winPicURL, 200, 200, align='center', width=app.winPicWidth//3, height=app.winPicHeight//3)
        drawRect(200, 350, 100, 30, fill=app.buttonColor, border='black', align='center')
        drawLabel('Main Menu', 200, 350, size=16, italic=True, bold=True)
    elif app.level == 5:
        drawLabel('You Lose!', 200, 50, size=36, font='grenze', bold=True)
        drawImage(app.losePicURL, 200, 200, align='center', width=app.losePicWidth//3, height=app.losePicHeight//3)
        drawRect(200, 350, 100, 30, fill=app.buttonColor, border='black', align='center')
        drawLabel('Main Menu', 200, 350, size=16, italic=True, bold=True)
    else:
        if app.hardMode:
            drawLabel(f'Time Remaining: {app.timer}s', 200, 55, bold=True, italic=True)
        drawLabel(f'Level {app.level}', 200, 20, size=24, font='grenze', bold=True)
        drawLabel('Press Enter to Reset', 200, 40, bold=True, italic=True)
        drawBoard(app)

def drawBoard(app):
    level = app.levels[app.level]
    for row in range(app.rows):
        for col in range(app.cols):
            if level.board[row][col] != 0:
                colorIndex = level.board[row][col]
                ball = True if [row, col] in level.balls else False
                player = True if [row, col] == level.player else False
                drawCell(app, row, col, app.colors[colorIndex], ball, player)

def drawCell(app, row, col, color, ball, player):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=color, border='gray' if color!='lightGreen' else 'darkGreen')
    if ball:
        drawImage(app.ballURL, cellLeft + (cellWidth/2), cellTop + (cellHeight/2), align='center', width=app.ballWidth//34, height=app.ballHeight//34)
    if player:
        drawImage(app.playerURL, cellLeft + (cellWidth/2), cellTop + (cellHeight/2), align='center', width=app.playerWidth//30, height=app.playerHeight//30)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def onKeyPress(app, key):
    if key == 'enter':
        reset(app)
    if key in ['up', 'down', 'left', 'right'] and 0<app.level<4:
        level = app.levels[app.level]
        level.move(app, key)
        if level.checkWin():
            app.winEffect.play()
            app.level += 1
    
    # grading shortcuts
    if key in ['0', '1', '2', '3', '4', '5']:
        reset(app)
        app.level = int(key)
            
def onMousePress(app, mx, my):
    if (app.level in [0, 4, 5]) and pointInRect(app, 200, 350, mx, my, False):
        app.buttonColor = 'gray'
        app.button = True
    if (app.level == 0) and pointInRect(app, 200, 315, mx, my, False):
        app.hardMode = not app.hardMode
    if pointInRect(app, 22, 20, mx, my, True):
        if app.playing:
            app.bgMusic.pause()
            app.playing = False
        else:
            app.bgMusic.play(loop=True)
            app.playing = True
        
def onMouseRelease(app, mx, my):
    if app.button == True:
        if app.level in [4, 5]:
            reset(app)
            app.level = 0
        else:
            app.level = 1
        app.timer = 60
        app.moves = 0
        app.button = False
        app.buttonColor = 'lightGray'
        
def onStep(app):
    if (app.hardMode == True) and (0<app.level<4):
        app.timer -= 1
        if app.timer < 0:
            app.level = 5
    
def reset(app):
    for i in range(1, 4):
        app.levels[i] = Level(app.boards[i], app.balls[i], app.players[i])
        
def pointInRect(app, cx, cy, mx, my, sound):
    if sound:
        return cx-15<=mx<=cx+15 and cy-20<=my<=cy+15
    else:
        return cx-50<=mx<=cx+50 and cy-15<=my<=cy+15

def main():
    runApp()

main()