import pygame
from ui import UI

def main():
    pygame.init()
    ui = UI()
    ui.init_screen(1000, 600)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = ui.draw_title_screen()
                if button.collidepoint(event.pos):
                    print("Game Started!") 
                    
        ui.draw_title_screen()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()