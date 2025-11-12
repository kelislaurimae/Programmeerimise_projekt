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
font = pygame.font.Font(None, 32)
suur_font = pygame.font.Font(None, 50)
valge = (255, 255, 255)
must = (0, 0, 0)
hall = (200, 200, 200)

punktid = 0
praegune = 0
tagasiside = ""
kell = pygame.time.Clock()
näita_tagasisidet = False
tagasiside_hetk = 0

def joonista_nupp(tekst, x, y, laius, kõrgus, aktiivne=False):
    värv = hall if not aktiivne else (180, 180, 180)
    pygame.draw.rect(ekraan, värv, (x, y, laius, kõrgus))
    nupp_tekst = font.render(tekst, True, must)
    ekraan.blit(
        nupp_tekst,
        (x + (laius - nupp_tekst.get_width()) // 2,
         y + (kõrgus - nupp_tekst.get_height()) // 2)
    )

# Mängu tsükkel
while True:
    ekraan.fill(valge)

    # Kui küsimused on läbi
    if praegune >= len(kysimused):
        lõpp_tekst = suur_font.render(f"Mäng läbi! Punktid: {punktid}/{len(kysimused)}", True, must)
        ekraan.blit(lõpp_tekst, (laius//2 - lõpp_tekst.get_width()//2, kõrgus//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    küsimus = kysimused[praegune]

    # Kuvame küsimuse
    termin_tekst = suur_font.render(küsimus["termin"], True, must)
    ekraan.blit(termin_tekst, (laius//2 - termin_tekst.get_width()//2, 100))

    # Kuvame punktid
    punktid_tekst = font.render(f"Punktid: {punktid}", True, must)
    ekraan.blit(punktid_tekst, (50, 30))

    # Kuvame valikvastused
    nupu_laius, nupu_kõrgus = 600, 60
    vahe = 20
    alg_y = 250
    nupud = []

    for i, valik in enumerate(küsimus["valikud"]):
        x = (laius - nupu_laius) // 2
        y = alg_y + i * (nupu_kõrgus + vahe)
        joonista_nupp(valik, x, y, nupu_laius, nupu_kõrgus)
        nupud.append(pygame.Rect(x, y, nupu_laius, nupu_kõrgus))

    # Kuvame tagasiside (nt "Õige!" või "Vale!")
    if näita_tagasisidet:
        tagasiside_tekst = font.render(tagasiside, True, must)
        ekraan.blit(tagasiside_tekst, (laius//2 - tagasiside_tekst.get_width()//2, kõrgus - 100))
        # Kui on möödunud 1 sekund, liigume edasi
        if pygame.time.get_ticks() - tagasiside_hetk > 1000:
            näita_tagasisidet = False
            praegune += 1

    pygame.display.flip()

    # Sündmused
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif sündmus.type == pygame.MOUSEBUTTONDOWN and not näita_tagasisidet:
            hiir_x, hiir_y = sündmus.pos
            for i, nupp in enumerate(nupud):
                if nupp.collidepoint(hiir_x, hiir_y):
                    if i == küsimus["vastus"]:
                        punktid += 1
                        tagasiside = "Õige!"
                    else:
                        tagasiside = "Vale!"
                    näita_tagasisidet = True
                    tagasiside_hetk = pygame.time.get_ticks()

    kell.tick(60)