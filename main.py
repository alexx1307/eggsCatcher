import pyglet
from pyglet.window import key
import pymunk
import pymunk.pyglet_util
import random

points = 0

width = 800
height = 600
window = pyglet.window.Window(width, height)
space = pymunk.Space()


def catchTheEgg(arbiter, space, data):
    global points
    points += 1
    eggShape = arbiter.shapes[0]
    eggs.remove(eggShape)
    space.remove(eggShape.body, eggShape)
    return False

collisionTypes = {
    "basket": 0,
    "regularEgg": 1
}
eggInBasketHandler = space.add_collision_handler(collisionTypes["regularEgg"], collisionTypes["basket"])
eggInBasketHandler.begin = catchTheEgg


movingLeft = False
movingRight = False
maxSpeed = 500

def createBasket():
    basketYPos = 20
    basketWidth = 100
    basketThickness = 10
    basketBody = pymunk.Body(1, pymunk.inf)
    basketBody.position = width // 2, basketYPos
    basketShape = pymunk.shapes.Segment(basketBody, (-basketWidth//2, 0), (basketWidth//2, 0), basketThickness)
    basketShape.collision_type = collisionTypes["basket"]
    basketConstraint = pymunk.GrooveJoint(space.static_body, basketBody, (basketWidth // 1.5, basketYPos), (width - basketWidth//1.5, basketYPos), (0,0))
    space.add(basketBody, basketShape, basketConstraint)
    return basketBody

eggs = []
def generateEgg():
    radius = 20
    eggBody = pymunk.Body(1, 1)
    eggBody.position = random.randint(radius, width-radius), height + radius
    eggBody.velocity = 0, -random.randint(100,300)
    eggShape = pymunk.Circle(eggBody, radius)
    eggShape.collision_type = collisionTypes["regularEgg"]
    eggs.append(eggShape)
    space.add(eggBody, eggShape)


options = pymunk.pyglet_util.DrawOptions()
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)


def updateVelocity():
    global basketBody
    vel = 0
    if movingLeft:
        vel -= maxSpeed
    if movingRight:
        vel += maxSpeed
    basketBody.velocity = vel, 0

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
    space.step(dt)

pyglet.clock.schedule_interval(update, 1/60)



basketBody = createBasket()
pyglet.app.run()
