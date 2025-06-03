import pygame
from pygame import gfxdraw  
import os

class UI:
    def __init__(self):
        self.screen = None
        self.title_font = None
        self.button_font = None
        self.small_font = None

        self.game = None
        self.ai = None
        self.revealed = set()
        self.flags = set()
        self.lost = False
        self.won = False
        
        self.colors = {
            "background": (251, 248, 225),      
            "title": (59, 32, 60),              
            "button": (255, 255, 255),          
            "button_border": (70, 80, 110),     
            "button_hover": (90, 100, 130),     
            "button_text": (30, 40, 60),        
            "rules_text": (50, 60, 80),        
            "board_bg": (240, 238, 245),        
            "cell_hidden": (235, 215, 210),     
            "cell_revealed": (255, 255, 255),
            "cell_border": (119, 99, 130),     
            "accent": (60, 80, 140),
            "danger": (170, 50, 70),
            "safe": (50, 130, 90),
            "shadow": (0, 0, 0, 40),
        }

        self.game_started = False
        self.bg_image = None
        self.board_rect = None
        self.bg_alpha = 35
        self.cell_size = 0

        self.flag_img = pygame.image.load("assets/images/flag.png")
        self.mine_img = pygame.image.load("assets/images/Mine.png")
        print(f"Flag img loaded: {self.flag_img is not None}")
        print(f"Mine img loaded: {self.mine_img is not None}")
        
    def init_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.title_font = pygame.font.Font(None, 72)   
        self.button_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)

        self.bg_image = pygame.image.load("assets/images/bg.jpeg").convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (width, height))
        self.bg_image.set_alpha(self.bg_alpha)
        
    def draw_shadow_rect(self, surface, color, rect, border_radius=0, shadow_offset=3):
        """Draw a rectangle with shadow effect"""
        # Shadow
        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        shadow_surface = pygame.Surface((rect.width + shadow_offset, rect.height + shadow_offset), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 35), pygame.Rect(shadow_offset, shadow_offset, rect.width, rect.height), border_radius=border_radius)
        surface.blit(shadow_surface, (rect.x, rect.y))
        
        # Main rectangle
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    
    def draw_title_screen(self):
        # Background
        self.screen.fill(self.colors["background"])
        self.screen.blit(self.bg_image, (0, 0))
        
        # Light overlay for better text visibility
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*self.colors["background"], 100))
        self.screen.blit(overlay, (0, 0))
        
        title_text = "Minesweeper AI"
        
        title = self.title_font.render(title_text, True, self.colors["title"])
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("Smart gameplay with AI assistance", True, self.colors["rules_text"])
        subtitle_rect = subtitle.get_rect(center=(self.screen.get_width()//2, 135))
        self.screen.blit(subtitle, subtitle_rect)
        
        button_rect = pygame.Rect(0, 0, 220, 50)
        button_rect.center = (self.screen.get_width()//2, 200)
        mouse_pos = pygame.mouse.get_pos()
        
        if button_rect.collidepoint(mouse_pos):
            bg_color = self.colors["button_hover"]
            text_color = (255, 255, 255)
            border_color = self.colors["button_hover"]
        else:
            bg_color = self.colors["button"]
            text_color = self.colors["button_text"]
            border_color = self.colors["button_border"]
        
        self.draw_shadow_rect(self.screen, bg_color, button_rect, border_radius=25)
        pygame.draw.rect(self.screen, border_color, button_rect, 2, border_radius=25)
        
        # Button text
        play_text = "START GAME"
        text = self.button_font.render(play_text, True, text_color)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

        self.draw_clean_rules()
        
        return button_rect
    
    def draw_clean_rules(self):
        # Rules container 
        rules_rect = pygame.Rect(0, 0, 400, 180)
        rules_rect.center = (self.screen.get_width()//2, 380)
        
        # Container background
        container_surface = pygame.Surface((rules_rect.width, rules_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(container_surface, (255, 255, 255, 220), pygame.Rect(0, 0, rules_rect.width, rules_rect.height), border_radius=12)
        self.screen.blit(container_surface, rules_rect.topleft)
        pygame.draw.rect(self.screen, self.colors["button_border"], rules_rect, 2, border_radius=12)
        
        # Rules title
        rules_title = self.button_font.render("HOW TO PLAY", True, self.colors["title"])
        title_rect = rules_title.get_rect(center=(rules_rect.centerx, rules_rect.y + 20))
        self.screen.blit(rules_title, title_rect)
        
        rules = [
            ("Left Click:", "Reveal a cell"),
            ("Right Click:", "Place/Remove flag"), 
            ("AI Move:", "Get AI assistance"),
            ("Reset:", "Start new game")
        ]
        
        start_y = rules_rect.y + 45
        for i, (action, description) in enumerate(rules):
            y_pos = start_y + i * 28
            
            action_text = self.small_font.render(action, True, self.colors["button_text"])
            self.screen.blit(action_text, (rules_rect.x + 30, y_pos))
            
            desc_text = self.small_font.render(description, True, self.colors["rules_text"])
            self.screen.blit(desc_text, (rules_rect.x + 140, y_pos))

    def draw_game_screen(self):
        # Background
        self.screen.fill(self.colors["background"])
        self.screen.blit(self.bg_image, (0, 0))
        
        max_board_size = min(450, int(self.screen.get_width() * 0.45))
        self.cell_size = max_board_size // 8
        board_size = self.cell_size * 8
        
        panel_width = 320  
        total_content_width = board_size + 80 + panel_width  
        start_x = (self.screen.get_width() - total_content_width) // 2
        
        self.board_rect = pygame.Rect(
            start_x,
            (self.screen.get_height() - board_size) // 2,
            board_size,
            board_size
        )
        
        container_rect = self.board_rect.inflate(30, 30)
        self.draw_shadow_rect(self.screen, self.colors["board_bg"], container_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.colors["button_border"], container_rect, 3, border_radius=15)
        
        game_title = self.button_font.render("MINESWEEPER", True, self.colors["title"])
        title_rect = game_title.get_rect(center=(container_rect.centerx, container_rect.y - 20))
        self.screen.blit(game_title, title_rect)
        
        # Draw the clean 8x8 minesweeper grid
        self.draw_clean_board()
        
        # Control panel (right side with proper distance)
        self.draw_control_panel()
        
    def draw_clean_board(self):
        """Draw a minesweeper board with uniform, clearly visible cells"""
        if not hasattr(self, 'game'):
            return
        
        for row in range(8):
            for col in range(8):
                cell = (row, col)
                cell_rect = pygame.Rect(
                    self.board_rect.x + col * self.cell_size,
                    self.board_rect.y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                if cell in self.revealed:
                    pygame.draw.rect(self.screen, self.colors["cell_revealed"], cell_rect)
                else:
                    pygame.draw.rect(self.screen, self.colors["cell_hidden"], cell_rect)

                if cell in self.flags:
                    if hasattr(self, 'flag_img') and self.flag_img:
                        self.screen.blit(
                            pygame.transform.scale(self.flag_img, (self.cell_size, self.cell_size)), 
                            cell_rect
                        )
                elif cell in self.revealed:
                    if self.game.is_mine(cell):
                        if hasattr(self, 'mine_img') and self.mine_img:
                            self.screen.blit(
                                pygame.transform.scale(self.mine_img, (self.cell_size, self.cell_size)), 
                                cell_rect
                            )
                    else:
                        count = self.game.nearby_mines(cell)
                        if count > 0:
                            text = self.small_font.render(str(count), True, self.colors["title"])
                            text_rect = text.get_rect(center=cell_rect.center)
                            self.screen.blit(text, text_rect)
                
                pygame.draw.rect(self.screen, self.colors["cell_border"], cell_rect, 2)
    
    def draw_control_panel(self):
        # Control panel positioning
        panel_width = 320  
        panel_gap = 80    
        panel_x = self.board_rect.right + panel_gap
        
        # Adjust if panel goes off screen
        if panel_x + panel_width > self.screen.get_width():
            panel_x = self.screen.get_width() - panel_width - 20
        
        control_panel = pygame.Rect(
            panel_x,
            self.board_rect.y,
            panel_width,
            self.board_rect.height
        )
        
        # Panel background with shadow
        self.draw_shadow_rect(self.screen, (255, 255, 255, 240), control_panel, border_radius=15)
        pygame.draw.rect(self.screen, self.colors["button_border"], control_panel, 3, border_radius=15)
        
        panel_title = self.button_font.render("CONTROLS", True, self.colors["title"])
        title_rect = panel_title.get_rect(center=(control_panel.centerx, control_panel.y + 25))
        self.screen.blit(panel_title, title_rect)
        
        stats_y = control_panel.y + 60

        if hasattr(self, 'start_time'):
            elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
            time_text = f"Time: {elapsed_seconds // 60:02d}:{elapsed_seconds % 60:02d}"
        else:
            time_text = "Time: 00:00"

        if self.lost:
            status_text = "GAME OVER"
            status_color = self.colors["danger"]
        elif self.won:
            status_text = "YOU WON!"
            status_color = self.colors["safe"]
        else:
            status_text = "PLAYING"
            status_color = self.colors["accent"]
            
        
        stats_font = self.small_font
        mines_text = stats_font.render(f"Mines: {len(self.flags)}/10", True, self.colors["danger"])
        self.screen.blit(mines_text, (control_panel.x + 25, stats_y))

        time_surface = stats_font.render(time_text, True, self.colors["button_text"])
        self.screen.blit(time_surface, (control_panel.x + 25, stats_y + 25))
        
        status_surface = stats_font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (control_panel.x + 25, stats_y + 50))
        
        line_y = stats_y + 90
        pygame.draw.line(self.screen, self.colors["cell_border"], 
                        (control_panel.x + 25, line_y), 
                        (control_panel.right - 25, line_y), 2)
        
        button_width = panel_width - 50
        button_height = 45
        
        ai_button = pygame.Rect(
            control_panel.x + 25,
            line_y + 25,
            button_width,
            button_height
        )
        self.draw_clean_button(ai_button, "AI MOVE", self.colors["safe"])
        
        reset_button = pygame.Rect(
            control_panel.x + 25,
            line_y + 85,
            button_width,
            button_height
        )
        self.draw_clean_button(reset_button, "RESET", self.colors["accent"])
        
        quit_button = pygame.Rect(
            control_panel.x + 25,
            line_y + 145,
            button_width,
            button_height
        )
        self.draw_clean_button(quit_button, "MENU", self.colors["danger"])
        
        return [ai_button, reset_button, quit_button]
    
    def draw_clean_button(self, rect, text, accent_color):
        """Draw a button without any icons"""
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        
        if hover:
            bg_color = accent_color
            text_color = (255, 255, 255)
            border_color = accent_color
        else:
            bg_color = self.colors["button"]
            text_color = self.colors["button_text"]
            border_color = self.colors["button_border"]
        
        # Button shadow and main button
        self.draw_shadow_rect(self.screen, bg_color, rect, border_radius=20)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=20)
        
        # Button text
        text_surf = self.small_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return hover