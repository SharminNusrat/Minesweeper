import pygame
from pygame import gfxdraw  

class UI:
    def __init__(self):
        self.screen = None
        self.title_font = None
        self.button_font = None
        self.colors = {
            "background": (22, 33, 62),  
            "title": (233, 69, 96),      
            "button": (28, 170, 156),    
            "button_hover": (48, 210, 186)
        }
        
    def init_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.title_font = pygame.font.Font(None, 80)  
        self.button_font = pygame.font.Font(None, 40)
    
    def draw_title_screen(self):
        for y in range(self.screen.get_height()):
            color = (22, 33, min(62 + y//10, 255)) 
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
        
        title = self.title_font.render("MINESWEEPER AI", True, self.colors["title"])
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 150))
        
        for offset, glow_color in [(4, (233, 69, 96, 50)), (8, (233, 69, 96, 20))]:
            glow_surf = pygame.Surface(title.get_size(), pygame.SRCALPHA)
            glow_surf.blit(title, (0, 0))
            glow_surf.fill((*glow_color[:3], 0), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(glow_surf, (title_rect.x - offset//2, title_rect.y - offset//2))
        
        self.screen.blit(title, title_rect)
        
        button_rect = pygame.Rect(0, 0, 300, 70)
        button_rect.center = (self.screen.get_width()//2, 350)
        mouse_pos = pygame.mouse.get_pos()
        
        if button_rect.collidepoint(mouse_pos):
            color = self.colors["button_hover"]
            border = 0
        else:
            color = self.colors["button"]
            border = 3  
        
        pygame.draw.rect(self.screen, color, button_rect, border_radius=25, width=border)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2, border_radius=25)  
        
        text = self.button_font.render("PLAY GAME", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        
        return button_rect