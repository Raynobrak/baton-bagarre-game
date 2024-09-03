from src.Animation import *
from src.AudioManager import AudioManager
from src.CooldownVariable import CooldownVariable
from src.Entity import Entity
from src.Stickman import Stickman, StickmanState, Direction
from src.Hit import PunchHit, KickHit
from src.ProgressBar import ProgressBar

vec = pygame.math.Vector2  # 2 for two dimensional


class Player(Stickman):
    PLAYER_SPRITE_SIZE = vec(50, 50)
    PLAYER_HITBOX_SIZE = vec(30, 50)

    PLAYER_MOVEMENT_SPEED = 250

    REIGNITE_FIRE_COOLDOWN = 2

    KICK_PBAR_SIZE = vec(40,5)
    KICK_PBAR_OFFSET = 30
    KICK_PBAR_COLOR_FRONT = (80,88,102)
    KICK_PBAR_COLOR_BACK = (255,255,255)

    def __init__(self, position, hitboxSize=PLAYER_HITBOX_SIZE):
        self.animation = None
        self.isPunching = False
        self.isKicking = False
        self.isLevitating = False

        self.levitatingTime = CooldownVariable(self.REIGNITE_FIRE_COOLDOWN)
        self.reignitProgressBar = ProgressBar(position, vec(hitboxSize.x, hitboxSize.y / 10), (255, 255, 0),
                                              (100, 100, 100))
        
        self.kickProgressBar = ProgressBar(position, self.KICK_PBAR_SIZE, self.KICK_PBAR_COLOR_FRONT, self.KICK_PBAR_COLOR_BACK)

        self.punchingTime = CooldownVariable(0.1)
        self.kickingTime = CooldownVariable(0.2)
        self.punchCooldown = CooldownVariable(0.3)
        self.kickCooldown = CooldownVariable(0.5)

        self.hits = list()

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

        for hit in self.hits:
            hit.update(dt)

        if not self.isLevitating:
            self.handle_events()

        self.apply_gravity(dt)

        super().update_position(dt)

        self.update_animation(dt)

        self.update_attack_animations(dt)

        self.levitatingTime.update_cooldown(dt)

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

    def go_levitate(self):
        if not self.isLevitating:
            self.velocity = vec(0, 0)
            self.isLevitating = True
            self.levitatingTime.reset()

            self.update_state(self.lookingDirection, StickmanState.REIGNITE_FIRE)
            AudioManager().play_sound("Yoga")

    def try_stop_levitate(self) -> bool:
        if self.isLevitating and self.levitatingTime.ready():
            self.stop_levitate()
            return True
        return False

    def stop_levitate(self):
        if self.isLevitating:
            self.isLevitating = False

            self.update_state(self.lookingDirection, StickmanState.IDLE)
            self.on_state_changed()
            AudioManager().stop_sound("Yoga")

    def generate_punch(self):
        self.hits.append(PunchHit(self))
        AudioManager().play_sound_random(["Punch1", "Punch2", "Punch3"])

    def generate_kick(self):
        self.hits.append(KickHit(self))
        AudioManager().play_sound_random(["Kick1", "Kick2", "Kick3"])

    def check_if_entity_is_hit(self, entity: Entity):
        for hit in self.hits:
            if hit.is_active():
                hit.check_for_collision(entity)
            # todo: delete if not active anymore

    def try_punch(self):
        if self.is_attacking():
            return
        if self.punchCooldown.try_reset():
            self.punchingTime.reset()
            self.isPunching = True
            self.set_animation(ANIM_PLAYER_PUNCH)
            self.generate_punch()
            if self.lookingDirection is Direction.RIGHT:
                self.animation.flip_horizontally()

    def try_kick(self):
        if self.is_attacking():
            return
        if self.kickCooldown.try_reset():
            self.kickingTime.reset()
            self.isKicking = True
            self.set_animation(ANIM_PLAYER_KICK)
            self.generate_kick()
            if self.lookingDirection is Direction.RIGHT:
                self.animation.flip_horizontally()

    def draw(self, surface):
        sprites_pos = self.get_sprite_pos_centered_around_hitbox(self.PLAYER_SPRITE_SIZE)
        self.animation.set_position(sprites_pos)
        self.animation.draw(surface)

        if self.isLevitating:
            self.reignitProgressBar.set_position(self.position + vec(0, -self.size.y / 5))
            self.reignitProgressBar.update_value(100 - self.levitatingTime.get_percentage() * 100)
            self.reignitProgressBar.draw(surface)

        if not self.kickCooldown.ready():
            pos = vec(self.position.x + self.size.x / 2, self.position.y)
            self.kickProgressBar.set_center(pos + vec(0, -self.KICK_PBAR_OFFSET))
            self.kickProgressBar.update_value((1 - self.kickCooldown.get_percentage()) * 100)
            self.kickProgressBar.draw(surface)
