import pyglet
from pyglet.window import key
import pymunk
import pymunk.pyglet_util
import random

points = 0
lives = 3
width = 800
height = 600
window = pyglet.window.Window(width, height)

space = pymunk.Space()


def removeEgg(eggShape):
    eggs.remove(eggShape)
    space.remove(eggShape.body, eggShape)


def catchHealerEgg(arbiter, space, data):
    global lives
    lives += 1
    removeEgg(arbiter.shapes[0])
    return False


def catchRegularEgg(arbiter, space, data):
    global points
    points += 1
    removeEgg(arbiter.shapes[0])
    return False


collisionTypes = {
    "basket": 0,
    "regularEgg": 1,
    "healerEgg": 2
}

eggTypes = [
    ("regularEgg", (50, 255, 50, 255), 70),
    ("healerEgg", (50, 50, 255, 255), 5)
]


eggInBasketHandler = space.add_collision_handler(
    collisionTypes["regularEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchRegularEgg

eggInBasketHandler = space.add_collision_handler(
    collisionTypes["healerEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchHealerEgg

movingLeft = False
movingRight = False
maxSpeed = 500

eggs = []


def generateEgg():
    def randomEggType():
        return random.choices(eggTypes, weights=[type[2] for type in eggTypes], k=1)[0]
    radius = 20
    eggBody = pymunk.Body(1, pymunk.inf)
    eggBody.position = random.randint(radius, width-radius), height + radius
    eggBody.velocity = 0, -random.randint(100, 300)
    eggType, eggColor, _ = randomEggType()
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


def updateVelocity():
    global basketBody
    vel = 0
    if movingLeft:
        vel -= maxSpeed
    if movingRight:
        vel += maxSpeed
    basketBody.velocity = vel, 0


def removeFallenEggs():
    for eggShape in eggs:
        if eggShape.body.position[1] < eggShape.radius:
            global lives
            lives -= 1
            removeEgg(eggShape)


@window.event
def on_key_press(symbol, modifiers):
    global movingLeft, movingRight
    if symbol == key.LEFT:
        movingLeft = True
    if symbol == key.RIGHT:
        movingRight = True
    updateVelocity()


@window.event
def on_key_release(symbol, modifiers):
    global movingLeft, movingRight
    if symbol == key.LEFT:
        movingLeft = False
    if symbol == key.RIGHT:
        movingRight = False
    updateVelocity()


timeToGenerateEgg = 2
level = 3


def update(dt):
    global timeToGenerateEgg
    timeToGenerateEgg -= dt
    if timeToGenerateEgg < 0:
        timeToGenerateEgg = random.uniform(level-0.5, level+0.5)
        generateEgg()
    removeFallenEggs()
    space.step(dt)


pointsLabel = pyglet.text.Label('Points',
                                font_name='Times New Roman',
                                font_size=36,
                                x=width - 120, y=height - 50,
                                anchor_x='center', anchor_y='center')
livesLabel = pyglet.text.Label('Lives',
                               font_name='Times New Roman',
                               font_size=36,
                               x=width - 120, y=height - 90,
                               anchor_x='center', anchor_y='center')

options = pymunk.pyglet_util.DrawOptions()


@window.event
def on_draw():
    window.clear()
    pointsLabel.text = f'Points: {points}'
    livesLabel.text = f'Lives: {lives}'
    pointsLabel.draw()
    livesLabel.draw()
    space.debug_draw(options)


pyglet.clock.schedule_interval(update, 1/60)

basketBody = createBasket()
pyglet.app.run()
