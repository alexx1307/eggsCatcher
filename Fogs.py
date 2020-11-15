import pyglet

fogImg = pyglet.image.load('./assets/newFog.png')
class Fog(pyglet.sprite.Sprite):
    def __init__(self, timeLeft, x, y):
        super().__init__(fogImg, x, y)
        self.timeLeft = timeLeft

        
    

