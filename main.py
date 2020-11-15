import pyglet
import HighScoresManager as hsm
from GameManager import GameManager

width = 800
height = 600

gameManager = GameManager(width, height)
gameManager.startGame()

pyglet.app.run()

