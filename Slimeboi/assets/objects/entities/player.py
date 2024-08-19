import pygame
import math

import config
import input
import statemachine






class Player:
    def __init__(self, x = 100, y = 100):
        self.h = 50
        self.w = 50
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)

        # Movement Values
        self.velocity = pygame.Vector2(0, 0)    # Tracks current speed
        self.MAX_SPEED = 600 * config.TICKTIME
        self.ACCELERATION = 16000 * config.TICKTIME * config.TICKTIME
        self.FRICTION = 8000 * config.TICKTIME * config.TICKTIME
        self.GRAVITY = 5000 * config.TICKTIME * config.TICKTIME
        self.JUMP_STR = -1000 * config.TICKTIME
        self.DBL_JUMP_STR = -800 * config.TICKTIME

        self.face = 1   # [-1] Facing left , [1] Facing right


        # Inputs
        #self.input = Inputs()
        self.inputs = input.Inputs()
        self.inputs.define_input("left", pygame.K_LEFT)
        self.inputs.define_input("right", pygame.K_RIGHT)
        self.inputs.define_impulse("jump", pygame.K_SPACE)
        self.inputs.define_impulse("dash", pygame.K_c)

        # State Machine
        self.fsm = statemachine.StateMachine()
        # States
        self.fsm.define_state("stand", None, self.stand_main, None)
        self.fsm.define_state("move", None, self.move_main, None)
        self.fsm.define_state("dash", self.dash_begin, self.dash_main, None)
        # Triggers - Conditions
        self.fsm.define_trigger("stand", ["move", "dash"])
        self.fsm.define_trigger("move", "dash")
        # Triggers - Slidebacks
        self.fsm.define_trigger("move", "stand", lambda: self.inputs.right - self.inputs.left == 0)

        self.fsm.begin("stand")

        #Character State
        self.on_ground = False
        self.jumps = 0
        self.JUMP_MAX = 3

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        # Draw Hitbox
        if config.DEBUG:
            rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
            pygame.draw.rect(surface, (255, 255, 102), rect, 3)

    def read_inputs(self, keys):
        self.inputs.read(keys)


    # Check for collisions while moving the character by its velocity
    def move_and_collide(self, objects):

        dx = self.position.x + self.velocity.x
        dy = self.position.y + self.velocity.y

        # X Movement
        if abs(self.velocity.x) > 0:
            signx = 1 if self.velocity.x >= 0 else -1
            velx = math.ceil(abs(self.velocity.x))
            self.rect.move_ip(signx * velx, 0)
            collisions = []
            for obj in objects:
                if self.rect.colliderect(obj):
                    collisions.append(obj)
            self.rect.move_ip(-signx * velx, 0)
            
            if len(collisions) > 0:
                for obj in collisions:
                    # Right
                    if signx == 1 and obj.left < dx + self.w:
                        dx = obj.left - self.w
                    # Left
                    if signx == -1 and obj.right > dx:
                        dx = obj.right

        self.position.x = dx
        self.rect.update(self.position.x, self.position.y, self.w, self.h)

        # Y Movement
        if abs(self.velocity.y) > 0:
            signy = 1 if self.velocity.y >= 0 else -1
            vely = math.ceil(abs(self.velocity.y))
            self.rect.move_ip(0, signy * vely)
            collisions = []
            for obj in objects:
                if self.rect.colliderect(obj):
                    collisions.append(obj)
            self.rect.move_ip(0, -signy * vely)

            if len(collisions) > 0:
                for obj in collisions:
                    # Up
                    if signy == -1 and obj.bottom > dy:
                        dy = obj.bottom
                    # Down (Landing on Ground)
                    if signy == 1 and obj.top < dy + self.h:
                        dy = obj.top - self.h
                        self.on_ground = True
                        self.jumps = self.JUMP_MAX
                if signy == -1: # Reduce upwards velocity if hitting head on ceiling
                    self.velocity.y /= 2
            else: # If no y-collisions exist, obj is mid-air
                self.on_ground = False
            
        self.position.y = dy
        self.rect.update(self.position.x, self.position.y, self.w, self.h)

    def apply_physics(self):
        # Add Friction
        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x - self.FRICTION, 0) # Clamp speed between current (positive) and 0
        if self.velocity.x < 0:
            self.velocity.x = min(self.velocity.x + self.FRICTION, 0)

        # Simulate Floor
        if self.on_ground:
            self.velocity.y = max(self.velocity.y - self.GRAVITY*4, 0)

        # Simulate Gravity
        self.velocity.y = min(self.velocity.y + self.GRAVITY, self.MAX_SPEED*2)
        

    # Determine Character's velocity this frame based on movement intentions
    def apply_move(self):
        move = self.inputs.right - self.inputs.left

        # Add Acceleration in the direction the player is moving
        if move == 1:
            self.velocity.x = max(min(self.velocity.x + self.ACCELERATION, self.MAX_SPEED), -self.MAX_SPEED) # Clamp speed between -MAX and MAX
        if move == -1:
            self.velocity.x = min(max(self.velocity.x - self.ACCELERATION, -self.MAX_SPEED), self.MAX_SPEED)
        
        if move == 0 and abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

        

    def process(self):
        if self.inputs.dash:
            self.fsm.trigger("dash")
        elif self.inputs.right or self.inputs.left:
            self.fsm.trigger("move")
        else:
            self.fsm.trigger("stand")

        self.fsm.process()


    def jump(self):
        if self.jumps > 0:
            self.on_ground = False
            if self.jumps == self.JUMP_MAX:
                self.velocity.y = self.JUMP_STR
            else:
                self.velocity.y = self.DBL_JUMP_STR
            self.jumps -= 1


    # States

    def stand_main(self):
        self.apply_physics()

        if self.inputs.jump:
            self.jump()

    def move_main(self):
        self.apply_physics()
        self.apply_move()
        self.face = self.inputs.right - self.inputs.left

        if self.inputs.jump:
            self.jump()

    def dash_begin(self):
        # If changing direction same frame as dashing
        move = self.inputs.right - self.inputs.left
        if move != 0:
            self.face = move

        self.fsm.state.data = {"timer": 0.1 * config.TICKRATE,
                               "sign": self.face}
        self.velocity.x = self.fsm.state.data["sign"] * self.MAX_SPEED * 2.5
        self.velocity.y = 0
        print("begin")

    def dash_main(self):
        self.fsm.state.data["timer"] -= 1
        print("timer: "+str(self.fsm.state.data["timer"]))

        # Out condition
        if self.fsm.state.data["timer"] <= 0:
            self.fsm.begin("move")

    def dash_end(self):
        if abs(self.velocity.x) > self.MAX_SPEED:
            self.velocity.x = self.fsm.state.data["sign"] * self.MAX_SPEED