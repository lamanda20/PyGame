import os
import pygame
import random
from animation import Animation

class Enemy:
    def __init__(self, x, y, tile_size, game_map):
     self.tile_size = tile_size
     self.game_map = game_map
    
    # Animation system
     self.animations = {
        "Run": self._load_animation("Run", 6, 8),
        "Death": self._load_animation("Death", 8, 12, loop=False)
    }
     self.state = "Run"
     self.current_anim = self.animations[self.state]
    
    # Get sprite dimensions from first frame
     self.sprite_width, self.sprite_height = self.current_anim.current_frame.get_size()
    
    # Create smaller hitbox (60% of sprite size)
     hitbox_width = int(self.sprite_width * 0.6)
     hitbox_height = int(self.sprite_height * 0.6)
    
     self.hitbox = pygame.Rect(
        x + (tile_size - hitbox_width) // 2,
        y + (tile_size - hitbox_height) // 2,
        hitbox_width,
        hitbox_height
    )
    
    # Rest of your initialization...
        
        # Enemy properties
     self.speed = 2
     self.direction = random.choice([-1, 1])  # -1: left, 1: right
     self.health = 1

    def _load_animation(self, anim_type, frame_count, speed, loop=True):
        """Load animation frames with error handling"""
        frames = []
        for i in range(frame_count):
            try:
                frame_path = os.path.join("sprites", "enemy", anim_type, f"{i}.png")
                frame = pygame.image.load(frame_path).convert_alpha()
                frames.append(frame)
            except:
                # Create colored placeholder with frame number
                frame = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
                color = (255, 0, 0) if anim_type == "Run" else (255, 165, 0)
                frame.fill(color)
                font = pygame.font.Font(None, 20)
                text = font.render(f"{anim_type[0]}{i}", True, (255, 255, 255))
                frame.blit(text, (5, 5))
                frames.append(frame)
        return Animation(frames, speed, loop)

    def update(self, player):
        """Update enemy state and handle collisions"""
        if self.state == "Death":
            self.current_anim.update()
            return self.current_anim.done  # Return True when death animation completes
            
        # Movement
        old_x = self.hitbox.x
        self.hitbox.x += self.speed * self.direction
        
        # Wall collision
        if self._check_collision():
            self.hitbox.x = old_x
            self.direction *= -1
        
        # Update animation
        self.current_anim.update()

        # Check bullet collisions
        for bullet in player.bullets[:]:
            if self.hitbox.colliderect(bullet.hitbox):
                player.bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self._die()
                    return True  # Signal enemy death
        return False

    def _die(self):
        """Handle death sequence"""
        self.state = "Death"
        self.current_anim = self.animations["Death"]
        self.current_anim.reset()
        self.speed = 0  # Stop movement

    def draw(self, screen):
        """Draw current animation frame"""
        frame = self.current_anim.current_frame
        if self.direction < 0 and self.state != "Death":  # Flip if moving left
            frame = pygame.transform.flip(frame, True, False)
        
        # Center sprite on hitbox
        draw_x = self.hitbox.centerx - frame.get_width() // 2
        draw_y = self.hitbox.centery - frame.get_height() // 2
        screen.blit(frame, (draw_x, draw_y))

    def _check_collision(self):
        """Check collision with walls"""
        start_x = max(0, self.hitbox.left // self.tile_size - 1)
        end_x = min(len(self.game_map.tiles[0]), (self.hitbox.right // self.tile_size) + 1)
        start_y = max(0, self.hitbox.top // self.tile_size - 1)
        end_y = min(len(self.game_map.tiles), (self.hitbox.bottom // self.tile_size) + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.game_map.tile_kinds[self.game_map.tiles[y][x]].is_solid:
                    wall_rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    if self.hitbox.colliderect(wall_rect):
                        return True
        return False