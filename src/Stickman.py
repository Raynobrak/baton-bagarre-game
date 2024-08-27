from src.Entity import Entity
from enum import Enum
from enum import IntEnum

import pygame
vec = pygame.math.Vector2  # 2 for two dimensional

class StickmanState(IntEnum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2
    REIGNITE_FIRE = 3
    ATTACKING_FIRE = 4

class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

class Stickman(Entity):
    def __init__(self, position, hitboxSize, movementSpeed):
        super().__init__(position, hitboxSize)
        self.state = StickmanState.IDLE
        self.lookingDirection = Direction.RIGHT
        self.movementSpeed = movementSpeed

        self.update_state(Direction.RIGHT, StickmanState.JUMPING)

    def update_state(self, newDir, newState):
        if self.lookingDirection is not newDir or self.state is not newState:
            self.lookingDirection = newDir
            self.state = newState
            self.on_state_changed()
    
    def on_state_changed(self):
        ...

    def go_left(self):
        self.velocity.x = -self.movementSpeed
        if self.state is StickmanState.IDLE:
            self.update_state(Direction.LEFT, StickmanState.WALKING)
        self.update_state(Direction.LEFT, self.state)

    def go_right(self):
        self.velocity.x = self.movementSpeed
        if self.state is StickmanState.IDLE:
            self.update_state(Direction.RIGHT, StickmanState.WALKING)
        self.update_state(Direction.RIGHT, self.state)

    def go_idle(self):
        self.velocity.x = 0
        if self.state is StickmanState.JUMPING:
            return
        elif self.state is StickmanState.WALKING:
            self.update_state(self.lookingDirection, StickmanState.IDLE)
        elif self.state is StickmanState.IDLE:
            return
        else:
            raise Exception("invalid state")
        
    def try_jump(self):
        if not self.state is StickmanState.JUMPING and self.velocity.y == 0:
            self.accelerate(vec(0, -350))
            self.update_state(self.lookingDirection, StickmanState.JUMPING)

    def reset_jump(self):
        if self.state is StickmanState.JUMPING:
            if self.velocity.x != 0:
                self.update_state(self.lookingDirection, StickmanState.WALKING)
            else:
                self.update_state(self.lookingDirection, StickmanState.IDLE)
            
    def check_collision_with_walls(self, mapSize: vec):
        if self.position.y + self.size.y > mapSize.y:
            self.position.y = mapSize.y - self.size.y
            self.velocity.y = 0
            self.reset_jump()

        if self.position.x + self.size.x > mapSize.x:
            self.position.x = mapSize.x - self.size.x
        elif self.position.x < 0:
            self.position.x = 0