import pygame

class Input:
    def __init__(self):
        self.move = 0
        self.jump = False
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
    def __init__(self, x=100, y=100):
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)

        self.MAX_SPEED = 5
        self.ACCX = 0.5
        self.GRAVITY = 0.4

        self.velocity = pygame.Vector2(0, 0)
        self.input = Input()

        # Character State
        self.on_ground = False
        self.jumps = 0
        self.JUMP_MAX = 3

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load('C:/repo/Slimeboi/assets/Char1.png').convert_alpha()
        self.sprite_width = 50  # Width of a single frame
        self.sprite_height = 50  # Height of a single frame
        self.current_frame = 0
        self.total_frames = 2  # Total frames in the sprite sheet
        self.animation_speed = 0.1  # Time between frame changes
        self.last_update_time = pygame.time.get_ticks()

    def update_animation(self, delta_time):
        # Update the animation frame based on delta time
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_speed * 1000:
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.last_update_time = now

    def draw(self, surface):
        # Draw the current frame of the sprite
        frame_rect = pygame.Rect(self.current_frame * self.sprite_width, 0, self.sprite_width, self.sprite_height)
        surface.blit(self.sprite_sheet, self.rect.topleft, frame_rect)

    def read_inputs(self, keys):
        self.input.read(keys)

    def move_and_collide(self, objects):
        # X Movement
        self.rect.move_ip(self.velocity.x, 0)
        collisions = [obj for obj in objects if self.rect.colliderect(obj)]
        self.rect.move_ip(-self.velocity.x, 0)
        
        dx = abs(self.velocity.x)
        if collisions:
            for obj in collisions:
                if self.velocity.x > 0:
                    dist = obj.left - self.rect.right
                    if dist < dx:
                        dx = dist
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
        collisions = [obj for obj in objects if self.rect.colliderect(obj)]
        self.rect.move_ip(0, -self.velocity.y)

        dy = abs(self.velocity.y)
        if collisions:
            for obj in collisions:
                if self.velocity.y < 0:
                    dist = self.rect.top - obj.bottom
                    if dist < dy:
                        dy = dist
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

    def move_update(self):
        if self.velocity.x > 0 and self.input.move != 1:
            self.velocity.x = max(self.velocity.x - (self.ACCX*2), 0)
        if self.velocity.x < 0 and self.input.move != -1:
            self.velocity.x = min(self.velocity.x + (self.ACCX*2), 0)

        if self.input.move == 1:
            self.velocity.x = max(min(self.velocity.x + self.ACCX, self.MAX_SPEED), -self.MAX_SPEED)
        if self.input.move == -1:
            self.velocity.x = min(max(self.velocity.x - self.ACCX, -self.MAX_SPEED), self.MAX_SPEED)
        
        if self.on_ground:
            self.velocity.y = max(self.velocity.y - self.GRAVITY*4, 0)

        self.velocity.y = min(self.velocity.y + self.GRAVITY, self.MAX_SPEED*2)

    def process(self):
        if self.input.jump and self.jumps > 0:
            self.on_ground = False
            if self.jumps == self.JUMP_MAX:
                self.velocity.y = -12
            else:
                self.velocity.y = -10
            self.jumps -= 1
        
        self.move_update()
        self.input.reset()
