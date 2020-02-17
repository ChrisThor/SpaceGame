import os
import time
import pygame


def take_screenshot(background):
    try:
        sc_dir = os.listdir("screenshots")
    except FileNotFoundError:
        os.mkdir("screenshots")
        sc_dir = []
    current_time = time.localtime()
    saving = True
    iteration = 0
    while saving:
        if iteration == 0:
            addition = ""
        else:
            addition = f" ({iteration})"
        filename = f"{current_time[0]}-{str(current_time[1]).rjust(2, '0')}-{str(current_time[2]).rjust(2, '0')}_" \
                   f"{str(current_time[3]).rjust(2, '0')}-{str(current_time[4]).rjust(2, '0')}-" \
                   f"{str(current_time[5]).rjust(2, '0')}{addition}"
        if f"{filename}.png" in sc_dir:
            iteration += 1
        else:
            saving = False
            pygame.image.save(background, f"screenshots/{filename}.png")
