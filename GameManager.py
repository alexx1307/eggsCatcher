import pyglet
from pyglet import image
from pyglet.window import key

import pymunk
import pymunk.pyglet_util

import random
from GUI import GUI
from Basket import Basket
import Fogs as fogs
import Eggs
import HighScoresManager
import Explosions
import Bullets

class GameManager(pyglet.window.Window):
    
    drawOptions = pymunk.pyglet_util.DrawOptions()
    pointsToNextLevel = [10,20,40,80,160,320]
    
    
    def __init__(self, width, height):
        super().__init__(width, height)
        self.collisionTypes = {
            "basket": 0,
            "egg": 1,
            "bullet": 2
        }
        self.gui = GUI(self, width, height)
        self.space = pymunk.Space()

        self.initPhysics()
        
        self.eggs = []
        self.fogs = []
        self.resetState()

        self.basket = Basket(self, self.space, width // 2, 20)
        self.gui.update()
    
    def resetState(self):
        self.points = 0
        self.lives = 3
        self.level = 1
        self.ammo = 5
        self.game = True
        self.timeToGenerateEgg = 2
        self.eggProbabilities= {
            Eggs.RegularEgg: 50,
            Eggs.HealerEgg: 5,
            Eggs.BombEgg: 10,
            Eggs.GoldenEgg: 5,
            Eggs.MistyEgg: 10,
            Eggs.ShootingEgg: 50
        }
        
    def reset(self):
        self.resetState()
        self.gui.update()

    def initPhysics(self):
        def eggCaught(arbiter, space, data):
            egg = arbiter.shapes[0]
            egg.whenCaught()
            self.removeEgg(egg)
            return False
        def eggHit(arbiter, space, data):
            egg = arbiter.shapes[0]
            Explosions.addExplosion(egg.body.position)
            self.removeEgg(egg)
            bullet = arbiter.shapes[1]
            Bullets.removeBullet(bullet,self)

            return False
        eggInBasketHandler = self.space.add_collision_handler(self.collisionTypes["egg"], self.collisionTypes["basket"])
        eggInBasketHandler.begin = eggCaught
        eggBullet = self.space.add_collision_handler(self.collisionTypes["egg"], self.collisionTypes["bullet"])
        eggBullet.begin = eggHit
    
    def updateLives(self, n):
        self.lives += n
        if self.lives <= 0:
            self.gameOver()
        self.gui.update()

    def updatePoints(self, pointsToAdd):
        self.points += pointsToAdd
        if self.level < len(GameManager.pointsToNextLevel):
            if self.points > GameManager.pointsToNextLevel[self.level - 1]:
                self.level += 1
        self.gui.update()
    
    def removeEgg(self, eggShape):
        self.eggs.remove(eggShape)
        self.space.remove(eggShape.body, eggShape)

    def gameOver(self):
        self.game = False
        for fog in list(self.fogs):
            self.fogs.remove(fog)
        for egg in list(self.eggs):
            self.removeEgg(egg)
        HighScoresManager.addScore(self.points)
        bestScores = HighScoresManager.getBestScores(5)
        self.gui.updateHS(bestScores)

    def generateEgg(self):
        def randomEggType():
            return random.choices(list(self.eggProbabilities.keys()), weights=self.eggProbabilities.values(), k=1)[0]
        radius = Eggs.Egg.radius
        pos = random.randint(radius, self.width-radius), self.height + radius
        eggType = randomEggType()
        egg = eggType(self, *pos)
        self.eggs.append(egg)
        self.space.add(egg, egg.body)

    def addFog(self):
        self.fogs.append(fogs.Fog(10, random.randint(0, self.width-fogs.fogImg.width),
                random.randint(0, self.height-fogs.fogImg.height)))

    def updateFogs(self, dt):
        for fog in list(self.fogs):
            fog.timeLeft -= dt
            if fog.timeLeft < 0:
                self.fogs.remove(fog)

    def removeFallenEggs(self):
        for egg in self.eggs:
            if egg.body.position[1] < egg.radius:
                self.removeEgg(egg)
                if self.game:
                    egg.whenFallUncaught()

    ############# PYGLET HANLDERS #############
    def on_draw(self):
        self.clear()
        self.gui.draw()
        #self.space.debug_draw(GameManager.drawOptions)
        self.basket.draw()
        for egg in self.eggs:
            egg.draw()
        for fog in self.fogs:
            fog.draw()
        for explosion in Explosions.explosions:
            explosion.draw()
        Bullets.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.basket.movingLeft = True
        if symbol == key.RIGHT:
            self.basket.movingRight = True
        if symbol == key.SPACE and not self.game:
            self.reset()
        if symbol == key.SPACE and self.game and self.ammo > 0:
            Bullets.shoot(self,self.basket.body.position)
            self.ammo -= 1
        self.basket.updateVelocity()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.basket.movingLeft = False
        if symbol == key.RIGHT:
            self.basket.movingRight = False
        self.basket.updateVelocity()


    def startGame(self):  
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        if self.game:
            Bullets.update(self)
            self.timeToGenerateEgg -= dt
            if self.timeToGenerateEgg < 0:
                self.timeToGenerateEgg = self.timeToNextEgg()
                self.generateEgg()
            self.removeFallenEggs()
            self.updateFogs(dt)
        self.space.step(dt)

    def timeToNextEgg(self):
        return 3/self.level + random.uniform(0, 1.0)