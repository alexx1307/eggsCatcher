import pymunk
import random 

class Egg(pymunk.Circle):
    radius = 20
    def __init__(self, gameManager, color, x, y):
        super().__init__(pymunk.Body(1, pymunk.inf), Egg.radius)
        self.body.position = x, y
        self.body.velocity = 0, -random.randint(100, 300)
        self.color = color
        self.collision_type = gameManager.collisionTypes["egg"]
        self.gameManager = gameManager
        self.color = color

    def whenCaught(self):
        pass

    def whenFallUncaught(self):
        pass

    def draw(self):
        pass
    
class RegularEgg(Egg):
    def __init__(self, gameManager, x, y):
        super().__init__(gameManager, (50, 255, 50, 255), x, y)

    def whenCaught(self):
        self.gameManager.updatePoints(1)
    
    def whenFallUncaught(self):
        self.gameManager.updateLives(-1)

class HealerEgg(Egg):
    def __init__(self, gameManager, x, y):
        super().__init__(gameManager, (50, 50, 255, 255), x, y)

    def whenCaught(self):
        self.gameManager.updateLives(1)
        
class BombEgg(Egg):
    def __init__(self, gameManager, x, y):
        super().__init__(gameManager, (50, 50, 100, 255), x, y)

    def whenCaught(self):
        self.gameManager.updateLives(-1)

class GoldenEgg(Egg):
    def __init__(self, gameManager, x, y):
        super().__init__(gameManager, (255, 215, 0, 255), x, y)
        self.body.velocity = 0, -random.randint(400, 600)
    def whenCaught(self):
        self.gameManager.updatePoints(5)

    def whenFallUncaught(self):
        self.gameManager.updateLives(-1)

class MistyEgg(Egg):
    def __init__(self, gameManager, x, y):
        super().__init__(gameManager, (155, 150, 250, 255), x, y)

    def whenCaught(self):
        self.gameManager.addFog()