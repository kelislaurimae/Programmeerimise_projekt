import pygame
import sys
from kysimused import kysimused 

# Initsialiseerime Pygame
pygame.init()

# Ekraani seaded
laius, kõrgus = 800, 600
ekraan = pygame.display.set_mode((laius, kõrgus))
pygame.display.set_caption("Terminimäng")

# Fondid ja värvid
font = pygame.font.Font(None, 50)
valge = (255, 255, 255)
must = (0, 0, 0)

punktid = 0
praegune = 0
sisestus = ""

# Mängu tsükkel
while True:
    ekraan.fill(valge)

    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif sündmus.type == pygame.KEYDOWN:
            if sündmus.key == pygame.K_RETURN:
                # Kontrollime vastust
                if sisestus.lower().strip() == kysimused[praegune]['valikud'][kysimused[praegune]['vastus']].lower().strip():
                    punktid += 1
                sisestus = ""
                praegune += 1
                if praegune >= len(kysimused):
                    # Mäng läbi
                    ekraan.fill(valge)
                    lõpp_tekst = font.render(f"Mäng läbi! Punktid: {punktid}", True, must)
                    ekraan.blit(lõpp_tekst, (laius//2 - lõpp_tekst.get_width()//2, kõrgus//2))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()
            elif sündmus.key == pygame.K_BACKSPACE:
                sisestus = sisestus[:-1]
            else:
                sisestus += sündmus.unicode

    # Kuvame küsimuse ja sisestuse
    küsimus_tekst = font.render(kysimused[praegune]['termin'], True, must)
    ekraan.blit(küsimus_tekst, (50, 100))

    sisestus_tekst = font.render(sisestus, True, must)
    ekraan.blit(sisestus_tekst, (50, 200))

    punktid_tekst = font.render(f"Punktid: {punktid}", True, must)
    ekraan.blit(punktid_tekst, (50, 50))

    pygame.display.flip()