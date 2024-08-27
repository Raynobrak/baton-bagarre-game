from enum import Enum

from pygame.locals import *

from src.Animation import *
from src.CooldownVariable import CooldownVariable
from src.Fire import Fire
from src.ImageManager import ImageManager
from src.Stickman import Stickman, StickmanState, Direction

from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional

class Player(Stickman):
    PLAYER_SPRITE_SIZE = vec(50,50)
    PLAYER_HITBOX_SIZE = vec(30,50)

    PLAYER_MOVEMENT_SPEED = 250

    def __init__(self, position, hitboxSize = PLAYER_HITBOX_SIZE):
        self.isPunching = False
        self.isKicking = False

        self.isLevitating = False

        self.punchingTime = CooldownVariable(0.1)
        self.kickingTime = CooldownVariable(0.2)
        self.punchCooldown = CooldownVariable(0.3)
        self.kickCooldown = CooldownVariable(0.5)

        super().__init__(position, hitboxSize, self.PLAYER_MOVEMENT_SPEED)

    
    def on_state_changed(self):
        if not self.isPunching and not self.isKicking:
            match self.state:
                case StickmanState.IDLE:
                    self.set_animation(ANIM_PLAYER_IDLE)
                case StickmanState.WALKING:
                    self.set_animation(ANIM_PLAYER_WALKING)
                case StickmanState.JUMPING:
                    self.set_animation(ANIM_PLAYER_JUMPING)
                case StickmanState.REIGNITE_FIRE:
                    self.set_animation(ANIM_PLAYER_REIGNITE_FIRE)
        
        if self.lookingDirection is Direction.RIGHT:
            self.animation.flip_horizontally()

    def set_animation(self, animInfos):
        pos = self.get_sprite_pos_centered_around_hitbox(self.PLAYER_SPRITE_SIZE)
        self.animation = Animation(animInfos, pos, self.PLAYER_SPRITE_SIZE)
        self.animation.start()

    def update_animation(self, dt: float):
        self.animation.update(dt)

    def handle_events(self):
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_e] and self.is_near_fire(fire):
            self.go_levitate()

        if keysPressed[pygame.K_a]:
            self.go_left()
        elif keysPressed[pygame.K_d]:
            self.go_right()

        if keysPressed[pygame.K_w]:
            self.try_jump()

        if keysPressed[pygame.K_SPACE]:
            self.try_punch()
        elif keysPressed[pygame.K_k]:
            self.try_kick()

        if not keysPressed[pygame.K_a] and not keysPressed[pygame.K_d]:
            self.go_idle()

    def update(self, dt: float):
        self.handle_events()

        if self.isLevitating:
            self.heal_fire(fire)

        self.apply_gravity(dt)

        super().update_position(dt)

        self.update_animation(dt)

        self.update_attack_animations(dt)

    def update_attack_animations(self, dt):
        self.punchCooldown.update_cooldown(dt)
        self.kickCooldown.update_cooldown(dt)
        self.punchingTime.update_cooldown(dt)
        self.kickingTime.update_cooldown(dt)

        if self.isPunching and self.punchingTime.ready():
            self.isPunching = False
            self.on_state_changed()
        if self.isKicking and self.kickingTime.ready():
            self.isKicking = False
            self.on_state_changed()

    def is_attacking(self):
        return self.isPunching or self.isKicking

    # Calling go_idle doesn't change the animation, why? :( Esteban
    def go_levitate(self):
        if not self.isLevitating:
            self.set_animation(ANIM_PLAYER_LEVITATING)
            self.isLevitating = True
            if self.lookingDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()

    def stop_levitate(self):
        if self.isLevitating:
            self.set_animation(ANIM_PLAYER_IDLE)
            if self.lookingDirection == PlayerDirection.RIGHT:
                self.animation.flip_horizontally()
            self.isLevitating = False
            self.healCooldown.reset()

    def heal_fire(self, fire: Fire):
        if self.healCooldown.try_reset() and self.isLevitating:
            print("Healing fire...")
            fire.heal_fire()


    def is_near_fire(self, fire: Fire):
        distance = self.position.distance_to(fire.position)
        return distance < 50

    def try_punch(self):
        if self.is_attacking():
            return
        if self.punchCooldown.try_reset():
            self.punchingTime.reset()
            self.isPunching = True
            self.set_animation(ANIM_PLAYER_PUNCH)
            if self.lookingDirection is Direction.RIGHT:
                self.animation.flip_horizontally()
                
    def try_kick(self):
        if self.is_attacking():
            return
        if self.kickCooldown.try_reset():
            self.kickingTime.reset()
            self.isKicking = True
            self.set_animation(ANIM_PLAYER_KICK)
            if self.lookingDirection is Direction.RIGHT:
                self.animation.flip_horizontally()

    def draw(self, surface):
        sprites_pos = self.get_sprite_pos_centered_around_hitbox(self.PLAYER_SPRITE_SIZE)
        self.animation.set_position(sprites_pos)
        self.animation.draw(surface)
        


