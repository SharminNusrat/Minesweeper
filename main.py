import pygame
from ui import UI
from minesweeper import Minesweeper
from ai import MinesweeperAI

def main():
    pygame.init()
    pygame.display.set_caption("Minesweeper AI")
    
    ui = UI()
    ui.init_screen(1200, 700)  

    def init_game():
        ui.game = Minesweeper(height=8, width=8, mines=10)
        ui.ai = MinesweeperAI(height=8, width=8)
        ui.revealed = set()
        ui.flags = set()
        ui.lost = False
        ui.won = False
        ui.start_time = pygame.time.get_ticks()
        if hasattr(ui, 'end_time'):
            del ui.end_time
    
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
                        init_game()
                else:
                    # Game screen 
                    control_buttons = ui.draw_control_panel()
                    if len(control_buttons) >= 3:
                        ai_button, reset_button, quit_button = control_buttons[:3]
                        
                        if ai_button.collidepoint(event.pos) and not ui.lost and not ui.won:
                            print("AI Move")
                            move = ui.ai.make_safe_move()
                            if move and move in ui.flags:
                                ui.flags.remove(move)
                                print(f"AI removed incorrect flag at {move}")
                            if move is None:
                                move = ui.ai.make_random_move()
                                if move is None:
                                    print("No moves left!")
                                    continue
                                print("AI making random move")
                            else:
                                print("AI making safe move")
                            
                            if ui.game.is_mine(move):
                                ui.lost = True
                                ui.end_time = pygame.time.get_ticks()
                                ui.revealed.add(move)
                            else:
                                ui.revealed.add(move)
                                ui.ai.add_knowledge(move, ui.game.nearby_mines(move))
                                if len(ui.revealed) == 8*8 - len(ui.game.mines):
                                    ui.won = True
                                    ui.end_time = pygame.time.get_ticks()
                                    for mine in ui.game.mines:
                                        if mine not in ui.flags:
                                            ui.flags.add(mine)
                                                        
                        elif reset_button.collidepoint(event.pos):
                            print("Game Reset")
                            init_game()
                            
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
                            cell = (row, col)
                            
                            if 0 <= row < 8 and 0 <= col < 8:
                                if event.button == 1:  
                                    print(f"Left clicked cell ({row}, {col})")
                                    if not ui.lost and not ui.won and cell not in ui.flags:
                                        if ui.game.is_mine(cell):
                                            ui.lost = True
                                            ui.end_time = pygame.time.get_ticks()
                                            ui.revealed.add(cell)  
                                        else:
                                            ui.revealed.add(cell)
                                            ui.ai.add_knowledge(cell, ui.game.nearby_mines(cell))
                                            if len(ui.revealed) == 8*8 - len(ui.game.mines):
                                                ui.won = True
                                                ui.end_time = pygame.time.get_ticks()
                                                for mine in ui.game.mines:
                                                    if mine not in ui.flags:
                                                        ui.flags.add(mine)
                                elif event.button == 3:  
                                    print(f"Right clicked cell ({row}, {col})")
                                    if not ui.lost and not ui.won:
                                        if cell in ui.flags:
                                            ui.flags.remove(cell)
                                        elif cell not in ui.revealed:
                                            ui.flags.add(cell)
                    
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