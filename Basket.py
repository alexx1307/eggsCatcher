import pymunk
class Basket(pymunk.shapes.Segment):

    
    def __init__(self, gameManager, space, x, y):
        basketWidth = 100
        basketThickness = 10
        super().__init__(pymunk.Body(1, pymunk.inf), (-basketWidth//2, 0), (basketWidth//2, 0), basketThickness)
        self.maxSpeed = 500
        self.movingLeft = False
        self.movingRight = False
        self.body.velocity = 0,0
        self.body.position = x, y
        self.collision_type = gameManager.collisionTypes["basket"]
        
        basketConstraint = pymunk.GrooveJoint(space.static_body, self.body, (
            basketWidth // 1.5, y), (gameManager.width - basketWidth//1.5, y), (0, 0))
        space.add(self.body, self, basketConstraint)

    def updateVelocity(self):
        vel = 0
        if self.movingLeft:
            vel -= self.maxSpeed
        if self.movingRight:
            vel += self.maxSpeed
        self.body.velocity = vel, 0