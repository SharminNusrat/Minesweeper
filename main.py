import pygame
from ui import UI

def main():
    pygame.init()
    pygame.display.set_caption("Minesweeper AI")
    
    ui = UI()
    ui.init_screen(1200, 700)  
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.VIDEORESIZE:
                ui.init_screen(event.w, event.h)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ui.game_started:
                    button = ui.draw_title_screen()
                    if button.collidepoint(event.pos):
                        print("Game Started!")
                        ui.game_started = True
                else:
                    # Game screen 
                    control_buttons = ui.draw_control_panel()
                    if len(control_buttons) >= 3:
                        ai_button, reset_button, quit_button = control_buttons[:3]
                        
                        if ai_button.collidepoint(event.pos):
                            print("AI Move")
                            # AI logic 
                                                        
                        elif reset_button.collidepoint(event.pos):
                            print("Game Reset")
                            # Reset logic 
                            
                        elif quit_button.collidepoint(event.pos):
                            print("Returning to menu...")
                            ui.game_started = False
                    
                    # Handle board clicks
                    if hasattr(ui, 'board_rect') and ui.board_rect and ui.board_rect.collidepoint(event.pos):
                        # Calculate which cell was clicked
                        rel_x = event.pos[0] - ui.board_rect.x
                        rel_y = event.pos[1] - ui.board_rect.y
                        
                        if ui.cell_size > 0:
                            col = rel_x // ui.cell_size
                            row = rel_y // ui.cell_size
                            
                            if 0 <= row < 8 and 0 <= col < 8:
                                if event.button == 1:  
                                    print(f"Left clicked cell ({row}, {col})")
                                    # Reveal logic 
                                elif event.button == 3:  
                                    print(f"Right clicked cell ({row}, {col})")
                                    # Flag logic 
                    
        # Draw current screen
        if not ui.game_started:
            ui.draw_title_screen()
        else:
            ui.draw_game_screen()
            
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()