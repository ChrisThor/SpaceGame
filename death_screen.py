import time
import pygame
import global_variables


def show_death_screen(background, source):
    frame_start = time.time()

    text = get_death_message(source)

    death_screen_time = 5
    while death_screen_time > 0:
        background.fill((0, 0, 0))

        font = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-LightItalic.ttf", 20)
        font_text1 = font.render(text, True, (255, 0, 0)).convert_alpha()
        background.blit(font_text1, (100, 150))

        font_text2 = font.render("Cause of death:", True, (255, 255, 255)).convert_alpha()
        background.blit(font_text2, (100, 100))

        global_variables.screen.blit(background, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    death_screen_time = 0

        frame_end = time.time()
        delta_frame = frame_end - frame_start
        frame_start = time.time()

        death_screen_time -= delta_frame


def get_death_message(source):
    sources_dict = {
        "The depths": "The depths of this world have swallowed your soul.",
        "height": "You fell too far"
    }
    return sources_dict.get(source, "You died...")
