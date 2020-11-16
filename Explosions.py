import pyglet
explosions = []



explosion_sheet = pyglet.image.load('./assets/explosion.png')
image_grid = pyglet.image.ImageGrid(explosion_sheet, rows=2, columns=5)
explosion_anim = pyglet.image.Animation.from_image_sequence(image_grid, duration=0.1, loop = False)

def addExplosion(pos):
    explosions.append(Explosion(pos))

class Explosion(pyglet.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(explosion_anim, x = pos.x, y = pos.y)
        self.scale = 0.2
    def on_animation_end(self):
        explosions.remove(self)
        self.delete()