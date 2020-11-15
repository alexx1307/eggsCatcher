import pyglet
from pyglet.window import key
import pymunk
import pymunk.pyglet_util
import random
from pyglet import image
import HighScoresManager as hsm
from GUI import GUI

width = 800
height = 600
window = pyglet.window.Window(width, height)
gui = GUI(width, height)

pointsToNextLevel = [10,20,40,80,160,320]
class GameState:
    def __init__(self):
        self.points = 0
        self.lives = 3
        self.level = 1
        self.game = True
    
    def updateLives(self, n):
        self.lives += n
        if self.lives <= 0:
            gameOver()
        gui.update(self)

    def addPoints(self,pointsToAdd):
        self.points += pointsToAdd
        if self.level < len(pointsToNextLevel):
            if self.points > pointsToNextLevel[self.level - 1]:
                self.level += 1
        gui.update(self)

state = GameState()

def gameOver():
    state.game = False
    [removeEgg(eggShape) for eggShape in eggs]
    [fog.remove() for fog in fogs]
    hsm.addScore(state.points)
    bestScores = hsm.getBestScores(5)
    gui.updateHS(bestScores)



pic = image.load('./assets/cloud.png')
fogs = []


space = pymunk.Space()


def removeEgg(eggShape):
    eggs.remove(eggShape)
    space.remove(eggShape.body, eggShape)


def catchHealerEgg(arbiter, space, data):
    removeEgg(arbiter.shapes[0])
    return False

def catchBombEgg(arbiter, space, data):
    state.updateLives(-1)
    removeEgg(arbiter.shapes[0])
    return False

def catchRegularEgg(arbiter, space, data):
    state.addPoints(1)
    removeEgg(arbiter.shapes[0])
    return False


def catchGoldenEgg(arbiter, space, data):
    state.addPoints(5)
    removeEgg(arbiter.shapes[0])
    return False

def catchMistyEgg(arbiter, space, data):
    fogs.append([10, random.randint(0, width-pic.width),
                random.randint(0, height-pic.height)])
    removeEgg(arbiter.shapes[0])
    return False


collisionTypes = {
    "basket": 0,
    "regularEgg": 1,
    "healerEgg": 2,
    "goldenEgg": 3,
    "mistyEgg": 4,
    "bombEgg": 5
}

eggTypes = [
    ("regularEgg", (50, 255, 50, 255), 70),
    ("healerEgg", (50, 50, 255, 255), 5),
    ("goldenEgg", (255, 215, 0, 255), 20),
    ("mistyEgg", (155, 150, 250, 100), 10),
    ("bombEgg", (50, 50, 100, 255), 5)
]


eggInBasketHandler = space.add_collision_handler(
    collisionTypes["regularEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchRegularEgg

eggInBasketHandler = space.add_collision_handler(
    collisionTypes["healerEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchHealerEgg

eggInBasketHandler = space.add_collision_handler(
    collisionTypes["goldenEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchGoldenEgg

eggInBasketHandler = space.add_collision_handler(
    collisionTypes["mistyEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchMistyEgg

eggInBasketHandler = space.add_collision_handler(
    collisionTypes["bombEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchBombEgg



eggs = []
def generateEgg():
    def randomEggType():
        return random.choices(eggTypes, weights=[type[2] for type in eggTypes], k=1)[0]
    radius = 20
    eggBody = pymunk.Body(1, pymunk.inf)
    eggBody.position = random.randint(radius, width-radius), height + radius
    eggType, eggColor, _ = randomEggType()
    if eggType == "goldenEgg":
        eggBody.velocity = 0, -random.randint(400, 600)
    else:
        eggBody.velocity = 0, -random.randint(100, 300)
    eggShape = pymunk.Circle(eggBody, radius)
    eggShape.color = eggColor
    eggShape.collision_type = collisionTypes[eggType]
    eggs.append(eggShape)
    space.add(eggBody, eggShape)


def createBasket():
    basketYPos = 20
    basketWidth = 100
    basketThickness = 10
    basketBody = pymunk.Body(1, pymunk.inf)
    basketBody.position = width // 2, basketYPos
    basketShape = pymunk.shapes.Segment(
        basketBody, (-basketWidth//2, 0), (basketWidth//2, 0), basketThickness)
    basketShape.collision_type = collisionTypes["basket"]
    basketConstraint = pymunk.GrooveJoint(space.static_body, basketBody, (
        basketWidth // 1.5, basketYPos), (width - basketWidth//1.5, basketYPos), (0, 0))
    space.add(basketBody, basketShape, basketConstraint)
    return basketBody


basketBody = createBasket()

def updateFogs(dt):
    for x in fogs:
        x[0] -= dt
        if x[0] < 0:
            fogs.remove(x)


def updateVelocity():
    global basketBody
    vel = 0
    if movingLeft:
        vel -= maxSpeed
    if movingRight:
        vel += maxSpeed
    basketBody.velocity = vel, 0

collisionTypesToAvoid = [collisionTypes["bombEgg"], collisionTypes["goldenEgg"]]
def removeFallenEggs():
    for eggShape in eggs:
        if eggShape.body.position[1] < eggShape.radius:
            removeEgg(eggShape)
            if eggShape.collision_type not in collisionTypesToAvoid and state.game:
                state.updateLives(-1)


movingLeft = False
movingRight = False
maxSpeed = 500

@window.event
def on_key_press(symbol, modifiers):
    global movingLeft, movingRight
    if symbol == key.LEFT:
        movingLeft = True
    if symbol == key.RIGHT:
        movingRight = True
    if symbol == key.SPACE and not state.game:
        reset()
    updateVelocity()


@window.event
def on_key_release(symbol, modifiers):
    global movingLeft, movingRight
    if symbol == key.LEFT:
        movingLeft = False
    if symbol == key.RIGHT:
        movingRight = False
    updateVelocity()

def reset():
    global state
    state = GameState()
    gui.update(state)

timeToGenerateEgg = 2

def timeToNextEgg():
    return 3/state.level + random.uniform(0, 1.0)

def update(dt):
    if state.game:
        global timeToGenerateEgg
        timeToGenerateEgg -= dt
        if timeToGenerateEgg < 0:
            timeToGenerateEgg = timeToNextEgg()
            generateEgg()
        removeFallenEggs()
        updateFogs(dt)
    space.step(dt)

### WYŚWIETLANIE
options = pymunk.pyglet_util.DrawOptions()

@window.event
def on_draw():
    window.clear()
    gui.draw()
    space.debug_draw(options)
    for _, x, y in fogs:
        pic.blit(x, y, 0)

gui.update(state)
pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()

