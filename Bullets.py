import pymunk
import pyglet

bullet_pic = pyglet.image.load('./assets/bullet_pic.png')
bullet_pic.anchor_x = bullet_pic.width // 2
bullet_pic.anchor_y = bullet_pic.height // 2

bullets = []

class Bullet(pymunk.shapes.Circle):
    def __init__(self,position,gameManager):
        super().__init__(pymunk.Body(1, pymunk.inf),3)
        self.body.velocity = 0,100
        self.body.position = position.x,position.y + 10
        self.collision_type = gameManager.collisionTypes["bullet"]
        self.sprite = pyglet.sprite.Sprite(bullet_pic, *self.body.position)
        gameManager.space.add(self,self.body)
    
    def draw(self):
        self.sprite.x = self.body.position.x
        self.sprite.y = self.body.position.y
        self.sprite.draw()




def draw():
    for bullet in bullets:
        bullet.draw()


def update(gameManager):
    for bullet in list(bullets):
        if bullet.body.position.y > 600:
            removeBullet(bullet,gameManager)

def shoot(gameManager,position):
    bullets.append(Bullet(position,gameManager))

def removeBullet(bullet,gameManager):
    bullets.remove(bullet)
    gameManager.space.remove(bullet.body,bullet)

