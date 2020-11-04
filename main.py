import pyglet
from pyglet.window import key
import pymunk
import pymunk.pyglet_util
import random
from pyglet import image

pic = image.load('cloud.png')
points = 0
fogs = []
fog = False
lives = 3
width = 800
height = 600
window = pyglet.window.Window(width, height)
game = True
first_loop = True

space = pymunk.Space()


def removeEgg(eggShape):
    eggs.remove(eggShape)
    space.remove(eggShape.body, eggShape)


def catchHealerEgg(arbiter, space, data):
    global lives
    lives += 1
    removeEgg(arbiter.shapes[0])
    return False

def catchBombEgg(arbiter, space, data):
    global lives
    lives -= 1
    removeEgg(arbiter.shapes[0])
    return False

def catchRegularEgg(arbiter, space, data):
    global points
    points += 1
    removeEgg(arbiter.shapes[0])
    return False


def catchGoldenEgg(arbiter, space, data):
    global points
    points += 5
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


def removeFallenEggs():
    global game
    for eggShape in eggs:
        if eggShape.body.position[1] < eggShape.radius:
            if eggShape.collision_type != collisionTypes["bombEgg"] and game:
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
    if symbol == key.SPACE and not game:
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


timeToGenerateEgg = 2
level = 3


def update(dt):
    global game, first_loop
    if game:
        global timeToGenerateEgg
        timeToGenerateEgg -= dt
        if timeToGenerateEgg < 0:
            timeToGenerateEgg = random.uniform(level-0.5, level+0.5)
            generateEgg()
        removeFallenEggs()
        updateFogs(dt)
    if lives == 0:
        game = False
        [removeEgg(eggShape) for eggShape in eggs]
        [fog.remove() for fog in fogs]
        if first_loop:
            highscore()
        first_loop = False
    space.step(dt)

def highscore():
    global highscorelist, points
    highscorelist = []
    f = open('highscore.txt')
    mylist = list(map(int, f.read().split()))
    if points > mylist[4]:
        mylist.append(points)
        mylist.sort(reverse=True)
        mylist.pop(5)
    poslist = [350, 300, 250, 200, 150]
    for i in range(0, 5):
        scoreLabel = pyglet.text.Label(f'{i+1}. {mylist[i]}',
                                font_name='Times New Roman',
                                font_size=20,
                                x=width//2, y=poslist[i],
                                anchor_x='center', anchor_y='center')
        highscorelist.append(scoreLabel)
    f = open('highscore.txt', 'w')
    f.write(' '.join(list(map(str, mylist))))

def reset():
    global lives, points, game, first_loop
    lives = 3
    points = 0
    game = True
    first_loop = True

gameoverLabel = pyglet.text.Label('Game Over',
                                font_name='Times New Roman',
                                font_size=40,
                                x=width//2, y=550,
                                anchor_x='center', anchor_y='center')

pressspaceLabel = pyglet.text.Label('Press SPACE to play again',
                                font_name='Times New Roman',
                                font_size=20,
                                x=width//2, y=500,
                                anchor_x='center', anchor_y='center')

highscorelabel = pyglet.text.Label('Highscores',
                                font_name='Times New Roman',
                                font_size=20,
                                x=width//2, y=400,
                                anchor_x='center', anchor_y='center')

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
    if game:
        pointsLabel.draw()
        livesLabel.draw()
    space.debug_draw(options)
    for _, x, y in fogs:
        pic.blit(x, y, 0)
    if not game:
        gameoverLabel.draw()
        pressspaceLabel.draw()
        highscorelabel.draw()
        global highscorelist
        for a in highscorelist:
            a.draw()


pyglet.clock.schedule_interval(update, 1/60)

basketBody = createBasket()
pyglet.app.run()
