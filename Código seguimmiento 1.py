from machine import Pin # importacion de las librerias 
import time, random

# nombramiento de pines sp32
ledsitos = [
    Pin(2, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(5, Pin.OUT)
]

sonido = Pin(18, Pin.OUT)

# pines para el jugador 1
boti1 = [
    Pin(12, Pin.IN, Pin.PULL_DOWN),
    Pin(13, Pin.IN, Pin.PULL_DOWN),
    Pin(14, Pin.IN, Pin.PULL_DOWN),
    Pin(27, Pin.IN, Pin.PULL_DOWN)
]

# pines para el jugador 2
boti2 = [
    Pin(26, Pin.IN, Pin.PULL_DOWN),
    Pin(25, Pin.IN, Pin.PULL_DOWN),
    Pin(33, Pin.IN, Pin.PULL_DOWN),
    Pin(32, Pin.IN, Pin.PULL_DOWN)
]

 # pines de los botones de inicio, simon dice y final
iniciobot = Pin(15, Pin.IN, Pin.PULL_DOWN)
simonbot = Pin(19, Pin.IN, Pin.PULL_DOWN)
salirbot = Pin(21, Pin.IN, Pin.PULL_DOWN)

#funciones que apoyan que el codigo funcione mejor y que guarde bien la informacion de los botones 
def apagar():
    for l in ledsitos:
        l.off()
    sonido.off()

def anti_rebote(pin):
    if pin.value():
        time.sleep_ms(40)
        return pin.value()
    return 0

def esperar_suelte(pin):
    while pin.value():
        time.sleep_ms(10)

def limpiar_botones():
    while (
        boti1[0].value() or boti1[1].value() or boti1[2].value() or boti1[3].value() or
        boti2[0].value() or boti2[1].value() or boti2[2].value() or boti2[3].value() or
        iniciobot.value() or simonbot.value() or salirbot.value()
    ):
        time.sleep_ms(10)

# esta funcion espera y guarda que boton se presiona cuando se esta jugando 
def reaccion(salida, jugadores):
    inicio = time.ticks_ms()

    while True:

        if anti_rebote(salirbot):
            return -1, False, 0

        for i in range(4):

            if anti_rebote(boti1[i]):
                fin = time.ticks_ms()
                return 1, (i == salida), time.ticks_diff(fin, inicio)

            if jugadores == 2:
                if anti_rebote(boti2[i]):
                    fin = time.ticks_ms()
                    return 2, (i == salida), time.ticks_diff(fin, inicio)

#  esta sirve para hacer que el codigo genere los estimulos osea prenda los leds

def activar_salida(num):
    apagar()
    if num < 3:
        ledsitos[num].on()
    else:
        sonido.on()

#  esta funcion sirve para poner el juego de los reflejos aca esta contenido el codigo de ejecucion
def reflejos(jugadores):

    puntos = [0,0]

    print("\nPresiona INICIO")
    while not anti_rebote(iniciobot):
        pass
    esperar_suelte(iniciobot)

    rondas = 5 

    for r in range(rondas):

        print("\n--- RONDA", r+1, "---")

        espera = random.randint(1,5)
        time.sleep(espera)

        salida = random.randint(0,3)
        activar_salida(salida)

        jugador, correcto, tiempo = reaccion(salida, jugadores)

        if jugador == -1:
            apagar()
            print("Salida manual")
            return

        apagar()

        print("Jugador", jugador, "tiempo:", tiempo, "ms")

        if correcto:
            puntos[jugador-1] += 1
        else:
            puntos[jugador-1] -= 1

        print("Marcador:", puntos)

    print("\n----------------------------")
    print("        FIN DEL JUEGO")
    print("------------------------------")

    if jugadores == 2:

        print("Puntaje final:")
        print("Jugador 1:", puntos[0])
        print("Jugador 2:", puntos[1])

        if puntos[0] > puntos[1]:
            print("\n EL GANADOR ES EL JUGADOR 1")
        elif puntos[1] > puntos[0]:
            print("\n EL GANADOR ES EL JUGADOR 2")
        else:
            print("\ HUBO UN EMPATEE")

    else:
        print("puntuacion:", puntos[0])

    print("---------------------------")
    time.sleep(2)

# en esta funcion se guarda todo lo del juego de simon dice osea ahi esta el codigo para que funcione
def juego_simon():

    print("\n JUEGA SIMON DICE ")
    secuencia = []
    ronda = 0

    time.sleep(0.5)

    while True:

        if anti_rebote(salirbot):
            esperar_suelte(salirbot)
            print("Activaste la salida del simon dice")
            return

        ronda += 1
        secuencia.append(random.randint(0,3))

        print("Ronda:", ronda)

        limpiar_botones()
        time.sleep(0.3)

        for s in secuencia:
            activar_salida(s)
            time.sleep(0.5)
            apagar()
            time.sleep(0.35)

        limpiar_botones()
        time.sleep(0.2)

        for esperado in secuencia:

            jugador, correcto, _ = reaccion(esperado,1)

            if jugador == -1:
                print("Saliste del simon dice")
                return

            if not correcto:
                print("Fallaste", ronda)
                print("Puntuacion de simon dice:", ronda-1)
                return

            time.sleep(0.15)

# en esta parte se escribe lo que se muestra al inicio cuando se corre el codigo osea el menu
while True:

    print("\n--------------------------")
    print("        MENU DE JUEGO")
    print("----------------------------")
    print("Presiona el Boton1 del primer jugador para solo jugar 1")
    print("Presiona el Boton1 del segundo jugador para  jugar 2")
    print("Presiona el segundo boton principal para jugar simon dice")
    print("----------------------------------------------------------")

    while True:

        if anti_rebote(simonbot):
            esperar_suelte(simonbot)
            print("\n Iniciando simon dice...")
            juego_simon()
            break

        if anti_rebote(boti1[0]):
            esperar_suelte(boti1[0])
            print("\nModo 1 jugador seleccionado")
            reflejos(1)
            break

        if anti_rebote(boti2[0]):
            esperar_suelte(boti2[0])
            print("\nModo 2 jugadores seleccionado")
            reflejos(2)
            break