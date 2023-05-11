"""
Día 10 - 'Invasión Espacial'
"""
import pygame
import random
import math
import io
from pygame import mixer

# Iniciar Pygame
pygame.init()


# Creando la pantalla
pantalla = pygame.display.set_mode((800, 600))


# Título e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('ovni_icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')

# Música
mixer.music.load('DEJAU - Rauw Alejandro Ft. Dj Playero (Official Audio).mp3')
mixer.music.play(-1)

# Jugador
jugador_icono = pygame.image.load('nave.png')
jugador_x = 368  # la mitad del ancho, menos la mitad del tamaño de mi png
jugador_y = 526  # lo mismo, pero yo le quise dar un poco más de espacio
jugador_x_mov = 0  # movimiento del jugador

# Enemigo
enemigo_icono = []
enemigo_x = []
enemigo_y = []
enemigo_x_mov = []
enemigo_y_mov = []
cantidad_enemigos = 5

# Enemigo
for e in range(cantidad_enemigos):
    enemigo_icono.append(pygame.image.load('ovni.png'))
    enemigo_x.append(random.randint(1, 735))
    enemigo_y.append(random.randint(20, 200))
    enemigo_x_mov.append(0.35)   # movimiento del enemigo
    enemigo_y_mov.append(48)

# Bala
bala_icono = pygame.image.load('bala.png')
bala_x = 0
bala_y = 525
bala_y_mov = 0.8
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('fastest.ttf', 22)
texto_x = 10
texto_y = 10

# Fin del juego
fuente_final = pygame.font.Font('fastest.ttf', 40)


# Función del puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Función del fin del juego
def texto_final():
    mi_fuente_final = fuente_final.render('PERDISTE', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (250, 290))


# Función del jugador
def jugador(x, y):
    pantalla.blit(jugador_icono, (x, y))  # para arrojar a nuestro jugador a la pantalla


# Función del jugador
def enemigo(x, y, ene):
    pantalla.blit(enemigo_icono[ene], (x, y))  # para arrojar a nuestro jugador a la pantalla


# Función disparo
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(bala_icono, (x + 16, y + 10))


# Función colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Cambiando el fondo (RGB)
    # pantalla.fill((205, 144, 228))  # primero se pinta la pantalla
    # Esto ya no lo usamos porque queremos un fondo de imagen
    pantalla.blit(fondo, (0, 0))

    # Iteración de eventos
    for evento in pygame.event.get():
        # Evento: Cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evento: Presión de teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_mov = jugador_x_mov - 1
            if evento.key == pygame.K_RIGHT:
                jugador_x_mov = jugador_x_mov + 1
            if evento.key == pygame.K_SPACE:
                pium = mixer.Sound('disparo.mp3')
                pium.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento: Soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_mov = 0

    # Evento: Modificación de ubicación (JUGADOR)
    jugador_x = jugador_x + jugador_x_mov
    # Limitar a bordes (JUGADOR)
    if jugador_x <= 1:
        jugador_x = 1
    elif jugador_x >= 735:  # el máximo del lado derecho contando los pixeles del png
        jugador_x = 735

    # Evento: Modificación de ubicación (ENEMIGO)
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] = enemigo_x[e] + enemigo_x_mov[e]
    # Limitar a bordes (ENEMIGO)
        if enemigo_x[e] <= 1:
            enemigo_x_mov[e] = 0.35
            enemigo_y[e] = enemigo_y[e] + enemigo_y_mov[e]
        elif enemigo_x[e] >= 735:  # el máximo del lado derecho contando los pixeles del png
            enemigo_x_mov[e] = -0.35
            enemigo_y[e] = enemigo_y[e] + enemigo_y_mov[e]

        enemigo(enemigo_x[e], enemigo_y[e], e)

        # Colisión
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje = puntaje + 10
            enemigo_x[e] = random.randint(1, 735)
            enemigo_y[e] = random.randint(20, 200)

    # Evento: Movimiento de la bala
    if bala_y <= -16:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y = bala_y - bala_y_mov

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
    # Evento: Actualizar
    pygame.display.update()
