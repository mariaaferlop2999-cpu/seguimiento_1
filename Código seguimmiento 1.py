from machine import Pin, mem32
import time, random

# Definicion de los registros para la esp32
GPIO_OUT_W1TS = 0x3FF44008  # SET bit
GPIO_OUT_W1TC = 0x3FF4400C  # CLEAR bit

# Declaracion inicial de cuales son los pines de los leds para usar la variable
LED1 = 2
LED2 = 4
LED3 = 5
BUZZ = 18

Pin(LED1, Pin.OUT)
Pin(LED2, Pin.OUT)
Pin(LED3, Pin.OUT)
Pin(BUZZ, Pin.OUT)

# declaracion de los botones de los jugadores en que pines va a estar
boti1 = [
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(13, Pin.IN, Pin.PULL_DOWN),
    Pin(14, Pin.IN, Pin.PULL_DOWN),
    Pin(27, Pin.IN, Pin.PULL_DOWN)
]

boti2 = [
    Pin(26, Pin.IN, Pin.PULL_DOWN),
    Pin(25, Pin.IN, Pin.PULL_DOWN),
    Pin(33, Pin.IN, Pin.PULL_DOWN),
    Pin(32, Pin.IN, Pin.PULL_DOWN)
]

iniciobot = Pin(15, Pin.IN, Pin.PULL_DOWN)
simonbot = Pin(19, Pin.IN, Pin.PULL_DOWN)
salirbot = Pin(21, Pin.IN, Pin.PULL_DOWN)

# funciones que apoyan el registro osea a controlar el periferico el led o buzzer

#declaracion de la funcion para que el componente se ponfa en 1 directamente

def set_gpio(pin):
    mem32[GPIO_OUT_W1TS] = (1 << pin)
    
#declaracion de la funcion para que el componente se ponfa en 0 directamente  

def clear_gpio(pin):
    mem32[GPIO_OUT_W1TC] = (1 << pin)  

def apagar():
    clear_gpio(LED1)
    clear_gpio(LED2)
    clear_gpio(LED3)
    clear_gpio(BUZZ)

#funciones que apoyan que el codigo funcione mejor y que guarde bien la informacion de los botones 

def anti_rebote(pin):
    if pin.value():
        time.sleep_ms(40)
        if pin.value():
            return 1
    return 0

def esperar_suelte(pin):
    while pin.value():
        time.sleep_ms(10)

def salir_presionado():
    if anti_rebote(salirbot):
        esperar_suelte(salirbot)
        apagar()
        print("\n--- SALIDA MANUAL ACTIVADA ---")
        return True
    return False

def cambio_a_simon():
    if anti_rebote(simonbot):
        esperar_suelte(simonbot)
        apagar()
        print("\n--- CAMBIO INMEDIATO A SIMON ---")
        juego_simon()
        return True
    return False

#  esta sirve para hacer que el codigo genere los estimulos osea prenda los leds

def activar_salida(num):
    apagar()

    if num == 0:
        set_gpio(LED1)
    elif num == 1:
        set_gpio(LED2)
    elif num == 2:
        set_gpio(LED3)
    else:
        set_gpio(BUZZ)

# esta funcion espera y guarda que boton se presiona cuando se esta jugando 

def reaccion(salida, jugadores):

    inicio = time.ticks_ms()

    while True:

        if salir_presionado():
            return -1, False, 0

        if cambio_a_simon():
            return -1, False, 0

        for i in range(4):

            if anti_rebote(boti1[i]):
                fin = time.ticks_ms()
                return 1, (i == salida), time.ticks_diff(fin, inicio)

            if jugadores == 2:
                if anti_rebote(boti2[i]):
                    fin = time.ticks_ms()
                    return 2, (i == salida), time.ticks_diff(fin, inicio)

#  esta funcion sirve para poner el juego de los reflejos aca esta contenido el codigo de ejecucion

def reflejos(jugadores):

    puntos = [0,0]

    print("\nPresiona INICIO")

    while not anti_rebote(iniciobot):
        if salir_presionado():
            return
        if cambio_a_simon():
            return

    esperar_suelte(iniciobot)

    rondas = 5

    for r in range(rondas):

        if salir_presionado():
            return

        if cambio_a_simon():
            return

        print("\n--- RONDA", r+1, "---")

        espera = random.randint(1,5)

        for _ in range(espera*10):
            time.sleep_ms(100)

            if salir_presionado():
                return

            if cambio_a_simon():
                return

        salida = random.randint(0,3)
        activar_salida(salida)

        jugador, correcto, tiempo = reaccion(salida, jugadores)

        if jugador == -1:
            return

        apagar()

        print("Jugador", jugador, "tiempo:", tiempo, "ms")

        if correcto:
            puntos[jugador-1] += 1
        else:
            puntos[jugador-1] -= 1

        print("Marcador:", puntos)

    print("\ FIN DEL JUEGO")

    if jugadores == 2:
        print("Jugador 1:", puntos[0])
        print("Jugador 2:", puntos[1])
    else:
        print("Puntuacion:", puntos[0])

    time.sleep(2)


# en esta funcion se guarda todo lo del juego de simon dice osea ahi esta el codigo para que funcione
def juego_simon():

    print("\nJUEGA SIMON DICE")

    secuencia = []
    ronda = 0

    time.sleep(0.5)

    while True:

        if salir_presionado():
            return

        ronda += 1
        secuencia.append(random.randint(0,3))

        print("Ronda:", ronda)

        for s in secuencia:

            if salir_presionado():
                return

            activar_salida(s)
            time.sleep(0.5)
            apagar()
            time.sleep(0.3)

        for esperado in secuencia:

            if salir_presionado():
                return

            jugador, correcto, _ = reaccion(esperado,1)

            if jugador == -1:
                return

            if not correcto:
                print("Fallaste en ronda", ronda)
                print("Puntuacion:", ronda-1)
                return

# en esta parte se escribe lo que se muestra al inicio cuando se corre el codigo osea el menu

while True:

    apagar()

    print("\n--------------------------")
    print("        MENU DE JUEGO")
    print("----------------------------")
    print("Presiona el Boton1 del primer jugador para solo jugar 1")
    print("Presiona el Boton1 del segundo jugador para  jugar 2")
    print("Presiona el segundo boton principal para jugar simon dice")
    print("----------------------------------------------------------")

    while True:

        if salir_presionado():
            break

        if anti_rebote(simonbot):
            esperar_suelte(simonbot)
            juego_simon()
            break

        if anti_rebote(boti1[0]):
            esperar_suelte(boti1[0])
            reflejos(1)
            break

        if anti_rebote(boti2[0]):
            esperar_suelte(boti2[0])
            reflejos(2)
            break
