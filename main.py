import pygame
import sys
import random
from kysimused import kysimused

pygame.init()

# ---------------- BAASRESOLUTSIOON ----------------
BAAS_LAIUS = 800
BAAS_KÕRGUS = 600

aken = pygame.display.set_mode((BAAS_LAIUS, BAAS_KÕRGUS), pygame.RESIZABLE)
pygame.display.set_caption("Terminimäng")

ekraan = pygame.Surface((BAAS_LAIUS, BAAS_KÕRGUS))


# ---------------- VÄRVID ----------------
TAUST = pygame.image.load("keyboard.jpg").convert_alpha()
taust = pygame.transform.smoothscale(TAUST, (BAAS_LAIUS, BAAS_KÕRGUS))
TEKSTVÄRV = (255, 255, 255)
NUPP = (95, 160, 210)
NUPP2 = (70, 140, 190)
MUST_TAUST = (0, 0, 0)


# ---------------- FONDID ----------------
font = pygame.font.Font(None, 32)
suur_font = pygame.font.Font(None, 50)


# ---------------- MÄNGU MUUTUJAD ----------------
punktid = 0
praegune = 0
tagasiside = ""
näita_tagasisidet = False
tagasiside_hetk = 0
kell = pygame.time.Clock()


# ---------------- ABIFUNKTSIOONID ----------------
def murra_tekst(tekst, font, max_laius):
    sõnad = tekst.split(" ")
    read = []
    rida = ""

    for sõna in sõnad:
        test = rida + sõna + " "
        if font.size(test)[0] <= max_laius - 20:
            rida = test
        else:
            read.append(rida)
            rida = sõna + " "

    if rida:
        read.append(rida)

    return read


def arvuta_nupu_kõrgus(tekst, font, laius, padding=20):
    read = murra_tekst(tekst, font, laius)
    return len(read) * font.get_height() + (len(read) - 1) * 5 + padding


def joonista_nupp(tekst, rect, hover=False):
    värv = NUPP2 if hover else NUPP
    pygame.draw.rect(ekraan, värv, rect, border_radius=8)

    read = murra_tekst(tekst, font, rect.width)
    kogukõrgus = len(read) * font.get_height() + (len(read) - 1) * 5
    y = rect.y + (rect.height - kogukõrgus) // 2

    for rida in read:
        pind = font.render(rida.strip(), True, TEKSTVÄRV)
        ekraan.blit(pind,(rect.centerx - pind.get_width() // 2, y))
        y += font.get_height() + 5


# ---------------- SEGAB VASTUSED ----------------

random.shuffle(kysimused)

for k in kysimused:
    valikud = list(enumerate(k["valikud"]))
    random.shuffle(valikud)
    k["valikud"] = [v for _, v in valikud]
    k["vastus"] = [i for i, (orig_i, _) in enumerate(valikud)
    if orig_i == k["vastus"]][0]


# ---------------- PEAMINE TSÜKKEL ----------------

while True:

    ekraan.blit(taust, (0, 0))

    # ---- AKNA SUURUS ----
    akna_laius, akna_kõrgus = aken.get_size()

    # ---- ÜHTLANE SKALEERIMINE ----
    scale = min(akna_laius / BAAS_LAIUS,akna_kõrgus / BAAS_KÕRGUS)

    uus_laius = int(BAAS_LAIUS * scale)
    uus_kõrgus = int(BAAS_KÕRGUS * scale)

    offset_x = (akna_laius - uus_laius) // 2
    offset_y = (akna_kõrgus - uus_kõrgus) // 2

    # ---- HIIR BAASKOORDINAATIDES ----
    hiir_x, hiir_y = pygame.mouse.get_pos()
    hiir_x = int((hiir_x - offset_x) / scale)
    hiir_y = int((hiir_y - offset_y) / scale)

    # ---- LÕPP ----
    if praegune >= len(kysimused):
        lõpptekst = suur_font.render(f"Mäng läbi! Punktid: {punktid}/{len(kysimused)}", True, TEKSTVÄRV)
        ekraan.blit(lõpptekst, (BAAS_LAIUS // 2 - lõpptekst.get_width() // 2, BAAS_KÕRGUS // 2))
    else:
        küsimus = kysimused[praegune]

        # Küsimus
        pealkiri = suur_font.render(küsimus["termin"], True, TEKSTVÄRV)
        ekraan.blit(pealkiri, (BAAS_LAIUS // 2 - pealkiri.get_width() // 2, 100))

        # Punktid
        punktid_txt = font.render(f"Punktid: {punktid}", True, TEKSTVÄRV)
        ekraan.blit(punktid_txt, (30, 20))

        # Vastuse nupud
        nupu_laius = int(BAAS_LAIUS * 0.75)
        vahe = 20
        y = 180
        nupud = []

        for valik in küsimus["valikud"]:
            kõrgus = arvuta_nupu_kõrgus(valik, font, nupu_laius)
            x = (BAAS_LAIUS - nupu_laius) // 2
            rect = pygame.Rect(x, y, nupu_laius, kõrgus)

            hover = rect.collidepoint(hiir_x, hiir_y)
            joonista_nupp(valik, rect, hover)

            nupud.append(rect)
            y += kõrgus + vahe

        # Tagasiside
        if näita_tagasisidet:
            tekst = font.render(tagasiside, True, TEKSTVÄRV)
            ekraan.blit(tekst, (BAAS_LAIUS // 2 - tekst.get_width() // 2, BAAS_KÕRGUS - 60))

            if pygame.time.get_ticks() - tagasiside_hetk > 1000:
                näita_tagasisidet = False
                praegune += 1


    # ---- JOONISTAB AKNASSE (LETTERBOX) ----
    skaleeritud = pygame.transform.smoothscale(ekraan, (uus_laius, uus_kõrgus))

    aken.fill(MUST_TAUST)
    aken.blit(skaleeritud, (offset_x, offset_y))
    pygame.display.flip()

    # ---- SÜNDMUSED ----
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if sündmus.type == pygame.MOUSEBUTTONDOWN and not näita_tagasisidet:
            mx = int((sündmus.pos[0] - offset_x) / scale)
            my = int((sündmus.pos[1] - offset_y) / scale)

            for i, rect in enumerate(nupud):
                if rect.collidepoint(mx, my):
                    if i == küsimus["vastus"]:
                        punktid += 1
                        tagasiside = "Õige!"
                    else:
                        tagasiside = "Vale!"
                    näita_tagasisidet = True
                    tagasiside_hetk = pygame.time.get_ticks()

    kell.tick(60)
