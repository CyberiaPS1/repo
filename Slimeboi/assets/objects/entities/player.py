import pygame

class Input:
    def __init__(self):
        self.move = 0
        self.jump = False

        # Pulse is True if the input is available
        self.jump_pulse = True

    def read(self, keys):
        self.move = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        if keys[pygame.K_SPACE]:
            if self.jump_pulse:
                self.jump = True
                self.jump_pulse = False
        elif not keys[pygame.K_SPACE]:
            self.jump_pulse = True
    
    def reset(self):
        self.jump = False




class Player:
    def __init__(self, x = 100, y = 100):
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)

        self.MAX_SPEED = 5
        self.ACCX = 0.5
        self.GRAVITY = 0.4


        self.velocity = pygame.Vector2(0, 0)

        self.input = Input()

        #Character State
        self.on_ground = False
        self.jumps = 0
        self.JUMP_MAX = 3

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def read_inputs(self, keys):
        self.input.read(keys)

    # Commit Character's movement (run after checking for collisions this frame)
    def move_and_collide(self, objects):
        # X Movement
        self.rect.move_ip(self.velocity.x, 0)
        collisions = []
        for obj in objects:
            if self.rect.colliderect(obj):
                collisions.append(obj)
        self.rect.move_ip(-self.velocity.x, 0)
        
        dx = abs(self.velocity.x)
        if len(collisions) > 0:
            for obj in collisions:
                # Right
                if self.velocity.x > 0:
                    dist = obj.left - self.rect.right
                    if dist < dx:
                        dx = dist
                # Left
                if self.velocity.x < 0:
                    dist = self.rect.left - obj.right
                    if dist < dx:
                        dx = dist
        
        if self.velocity.x < 0:
            dx *= -1

        self.position.x += dx
        self.rect.move_ip(dx, 0)

        # Y Movement
        self.rect.move_ip(0, self.velocity.y)
        collisions = []
        for obj in objects:
            if self.rect.colliderect(obj):
                collisions.append(obj)
        self.rect.move_ip(0, -self.velocity.y)

        dy = abs(self.velocity.y)
        if len(collisions) > 0:
            for obj in collisions:
                # Up
                if self.velocity.y < 0:
                    dist = self.rect.top - obj.bottom
                    if dist < dy:
                        dy = dist
                # Down
                if self.velocity.y > 0:
                    dist = obj.top - self.rect.bottom
                    if dist < dy:
                        dy = dist
                    self.on_ground = True
                    self.jumps = self.JUMP_MAX
            if self.velocity.y < 0:
                self.velocity.y /= 2
        else:
            self.on_ground = False
        
        if self.velocity.y < 0:
            dy *= -1
        
        self.position.y += dy
        self.rect.move_ip(0, dy)

    # Determine Character's velocity this frame based on movement intentions
    def move_update(self, dt):
        # Add Friction if player is not moving in a direction that has velocity
        if self.velocity.x > 0 and self.input.move != 1:
            self.velocity.x = max(self.velocity.x - (self.ACCX*2 * dt), 0) # Clamp speed between current (positive) and 0
        if self.velocity.x < 0 and self.input.move != -1:
            self.velocity.x = min(self.velocity.x + (self.ACCX*2 * dt), 0)

        # Add Acceleration in the direction the player is moving
        if self.input.move == 1:
            self.velocity.x = max(min(self.velocity.x + self.ACCX * dt, self.MAX_SPEED), -self.MAX_SPEED) # Clamp speed between -MAX and MAX
        if self.input.move == -1:
            self.velocity.x = min(max(self.velocity.x - self.ACCX * dt, -self.MAX_SPEED), self.MAX_SPEED)
        
        # Simulate Floor
        if self.on_ground:
            self.velocity.y = max(self.velocity.y - self.GRAVITY*4 * dt, 0)

        # Simulate Gravity
        self.velocity.y = min(self.velocity.y + self.GRAVITY * dt, self.MAX_SPEED*2)

    def process(self, dt):
        if self.input.jump and self.jumps > 0:
            self.on_ground = False
            if self.jumps == self.JUMP_MAX:
                self.velocity.y = -12
            else:
                self.velocity.y = -10
            self.jumps -= 1
        
        self.move_update(dt)

        self.input.reset()