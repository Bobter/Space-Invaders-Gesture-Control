import pygame
import random
import math

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Se inicializa la cámara y pygame
cap = cv2.VideoCapture(0)
pygame.init()

#Se definen las dimensiones de la pantalla y se muestra
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,
                                  screen_height))

#Titulo de la ventana
pygame.display.set_caption("Space Invaders")

#Se define los parámetros del marcador de puntos
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Parámetros para el jugador
playerImage = pygame.image.load('player.png')
player_X = 370
player_Y = 523
player_Xchange = 0

#Parámetros para el enemigo
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 10

#Generar enemigos
for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('enemy.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(0.8) #velocidad en X
    invader_Ychange.append(20) #velocidad en Y

#Parámetros para el proyectil
bulletImage = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 10
bullet_state = "rest"


#Función para detectar colisiones
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) +
                         (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


#Dibujando las imágenes
def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


#Parámetros para el loop del juego
running = True
game_over = True
victory = False

#Se inicializa mediapipe para la detección de gestos con las manos
with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:

    while running:

        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Aqui se obtienen las coordenadas de los puntos clave de la mano

                is_left_pointing = (
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.RING_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.RING_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.PINKY_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.PINKY_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.THUMB_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x < hand_landmarks.landmark[
                            mp_hands.HandLandmark.THUMB_TIP].x
                )

                is_right_pointing = (
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.RING_FINGER_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.RING_FINGER_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.PINKY_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.PINKY_TIP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.THUMB_MCP].x and
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x > hand_landmarks.landmark[
                            mp_hands.HandLandmark.THUMB_TIP].x
                )

                distancia_x = abs(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x - hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x)
                distancia_y = abs(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y - hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y)


                index_distance_y = abs(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y-hand_landmarks.landmark[
                   mp_hands.HandLandmark.INDEX_FINGER_TIP].y)

                middle_distance_y = abs(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y-hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)



                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2)
                )

                #Controles con gestos
                if is_right_pointing:
                    player_Xchange = -1.8

                if is_left_pointing:
                    player_Xchange = 1.8

                if index_distance_y>0.6 and middle_distance_y>0.6:
                    player_Xchange = 0

                if distancia_x <= 0.2 and distancia_y <= 0.2:
                    if bullet_state == "rest":
                        bullet_X = player_X
                        bullet(bullet_X, bullet_Y)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controles con el teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_Xchange = -0.5
                if event.key == pygame.K_RIGHT:
                    player_Xchange = 0.5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "rest":
                        bullet_X = player_X
                        bullet(bullet_X, bullet_Y)

        #Actualizando posición del jugador
        player_X += player_Xchange

        #Condiciones para que el player no pase los límites de la pantalla
        if player_X <= 0:
            player_X = 0
        elif player_X >= screen_width - 64:
            player_X = screen_width - 64

        #Movimiento del proyectil
        if bullet_state == "fire":
            bullet_Y -= bullet_Ychange
            bullet(bullet_X, bullet_Y)

        if bullet_Y <= 0:
            bullet_Y = 500
            bullet_state = "rest"

        #Comprobación de colisiones
        for i in range(no_of_invaders):
            if invader_Y[i] > 460:
                game_over = True
                break

            #Detección de colisiones
            collision = isCollision(invader_X[i], bullet_X, invader_Y[i], bullet_Y)
            if collision:
                bullet_Y = 500
                bullet_state = "rest"
                score_val += 1
                invader_X[i] = random.randint(64, 737)
                invader_Y[i] = random.randint(30, 180)

            invader_X[i] += invader_Xchange[i]
            if invader_X[i] <= 0:
                invader_Xchange[i] = 1.8
                invader_Y[i] += invader_Ychange[i]
            elif invader_X[i] >= screen_width - 64:
                invader_Xchange[i] = -1.8
                invader_Y[i] += invader_Ychange[i]

            invader(invader_X[i], invader_Y[i], i)

        # Check para la condición de victoria
        if score_val == no_of_invaders:
            victory = True

        #Actualización el marcador
        show_score(scoreX, scoreY)

        #Actualización de la posición del jugador
        player(player_X, player_Y)

        #Si has perdido se muestra:
        if game_over:
            screen.fill((0, 0, 0))
            game_over_text = font.render("Has pedido :C", True, (255, 255, 255))
            screen.blit(game_over_text, (screen_width / 2 - 150, screen_height / 2))

        #Si has ganado se muestra:
        if victory:
            screen.fill((0, 0, 0))
            victory_text = font.render("Has Ganadoooo! :D", True, (255, 255, 255))
            screen.blit(victory_text, (screen_width / 2 - 130, screen_height / 2))

        pygame.display.update()

    cap.release()

