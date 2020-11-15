import pyglet

class GUI:
    def __init__(self, gameManager, width, height):
        self.highScoresNumber = 5
        self.scoreLabels = []
        self.game = True
        self.gameManager = gameManager
        self.pointsLabel = pyglet.text.Label('Points',
                                font_name='Times New Roman',
                                font_size=36,
                                x=width - 120, y=height - 50,
                                anchor_x='center', anchor_y='center')
        self.livesLabel = pyglet.text.Label('Lives',
                                font_name='Times New Roman',
                                font_size=36,
                                x=width - 120, y=height - 90,
                                anchor_x='center', anchor_y='center')
        self.levelLabel = pyglet.text.Label('Level',
                                font_name='Times New Roman',
                                font_size=36,
                                x=width - 120, y=height - 130,
                                anchor_x='center', anchor_y='center')   
        self.gameoverLabel = pyglet.text.Label('Game Over',
                                font_name='Times New Roman',
                                font_size=40,
                                x=width//2, y=550,
                                anchor_x='center', anchor_y='center')

        self.pressspaceLabel = pyglet.text.Label('Press SPACE to play again',
                                        font_name='Times New Roman',
                                        font_size=20,
                                        x=width//2, y=500,
                                        anchor_x='center', anchor_y='center')

        self.highscorelabel = pyglet.text.Label('Highscores',
                                        font_name='Times New Roman',
                                        font_size=20,
                                        x=width//2, y=400,
                                        anchor_x='center', anchor_y='center')
        offset = 50
        yPosition = 350
        for i in range(0, self.highScoresNumber):
            scoreLabel = pyglet.text.Label(f'{i+1}. ',
                                    font_name='Times New Roman',
                                    font_size=20,
                                    x=width//2, y= yPosition - offset*i,
                                    anchor_x='center', anchor_y='center')
            self.scoreLabels.append(scoreLabel)
    
    def update(self):
        self.pointsLabel.text = f'Points: {self.gameManager.points}'
        self.livesLabel.text = f'Lives: {self.gameManager.lives}'
        self.levelLabel.text = f'Level: {self.gameManager.level}'
        self.game = self.gameManager.game
        
    
    def updateHS(self, bestScores):
        for i in range(len(bestScores)):
            self.scoreLabels[i].text = f'{i+1}. {bestScores[i]}'

    def draw(self):
        if self.game:
            self.pointsLabel.draw()
            self.livesLabel.draw()
            self.levelLabel.draw()
        else:
            self.gameoverLabel.draw()
            self.pressspaceLabel.draw()
            self.highscorelabel.draw()
            for a in self.scoreLabels:
                a.draw()
            

            