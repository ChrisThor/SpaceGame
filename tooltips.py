import pygame


class Tooltips:
    def __init__(self):
        self.font_height = 20
        font_bold = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-Bold.ttf", self.font_height)
        font_normal = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-Light.ttf", self.font_height)
        font_cursive = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-LightItalic.ttf", self.font_height)
        white = (255, 255, 255)
        grey = (175, 175, 175)
        self.lines = [font_bold.render("Steuerung:", True, white)]
        self.help_line = font_normal.render("Hilfe anzeigen: h", True, white)

        self.lines.append(font_cursive.render("Beschleunigen: Pfeiltasten", True, grey))
        self.lines.append(font_cursive.render("Lenken: Pfeiltasten", True, white))
        self.lines.append(font_cursive.render("Schubstärke: w/s", True, grey))
        self.lines.append(font_cursive.render("Bremsen: g", True, white))
        self.lines.append(font_cursive.render("Spielgeschwindigkeit: q/e", True, grey))
        self.lines.append(font_cursive.render("Pausieren: p", True, white))
        self.lines.append(font_cursive.render("Vektoren zeigen: v", True, grey))
        self.lines.append(font_cursive.render("Feuern: Leertaste", True, white))
        self.lines.append(font_cursive.render("Zoom: F1/F2", True, grey))
        self.lines.append(font_cursive.render("Screenshot: F12", True, white))
        self.lines.append(font_cursive.render("Speichern: F5", True, grey))
        self.lines.append(font_cursive.render("Laden: F9", True, white))
        self.lines.append(font_cursive.render("Hilfe ausblenden: h", True, grey))
        self.lines.append(font_cursive.render("", True, white))
        self.lines.append(font_bold.render("Planetenerzeugung:", True, white))
        self.lines.append(font_cursive.render("Planet erzeugen: Linke Maustaste", True, grey))
        self.lines.append(font_cursive.render("Geschwindigkeit setzen: Rechte Maustaste", True, white))
        self.lines.append(font_cursive.render("Radius/Masse Modus: x", True, grey))
        self.lines.append(font_cursive.render("Statischer Modus: c", True, white))

    def show_tooltips(self, background, show_tooltips):
        if show_tooltips:
            for i in range(len(self.lines)):
                background.blit(self.lines[i], (10, i * self.font_height))
        else:
            background.blit(self.help_line, (10, 0))